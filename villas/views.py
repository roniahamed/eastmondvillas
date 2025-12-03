from django.db import transaction
import json
from rest_framework import viewsets, status, serializers, filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from datetime import datetime, timedelta, date
from calendar import monthrange
from django.db.models import Exists, OuterRef, F, Count, Avg, Sum, Q

from .utils import update_daily_analytics, validate_date_range

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from auditlog.registry import auditlog

from .models import Property, Media, Booking, PropertyImage, BedroomImage, Review, ReviewImage, Favorite, DailyAnalytics, PropertyVideo
from .serializers import PropertySerializer , BookingSerializer, MediaSerializer, PropertyImageSerializer, BedroomImageSerializer, ReviewSerializer, ReviewImageSerializer, FavoriteSerializer, ReadReviewSerializer


from accounts.permissions import IsAdminOrManager, IsAgentWithFullAccess, IsAgent, IsOwnerOrAdminOrManager
from rest_framework.permissions import IsAdminUser


from rest_framework.pagination import PageNumberPagination

from django.utils.timezone import now
from list_vila.models import ContectUs
from django.db.models.functions import TruncMonth, TruncDay
from django.db.models import Value, BooleanField

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


from .filters import PropertyFilter
from datetime import datetime

from rest_framework.views import APIView

from django.contrib.auth import get_user_model
User = get_user_model()


# Property ViewSet

class PropertyViewSet(viewsets.ModelViewSet):

    serializer_class = PropertySerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['^title', '^city', '^description', '^interior_amenities', '^outdoor_amenities']
    ordering_fields = ['price', 'created_at', 'bedrooms', 'bathrooms']
    

    def get_queryset(self):
        
        user = self.request.user

        queryset = Property.objects.annotate(total_reviews=Count("reviews"),avg_rating=Avg("reviews__rating")).prefetch_related("media_images", "bedrooms_images")

        if user.is_authenticated:
            queryset = queryset.annotate(is_favorited=Exists(Favorite.objects.filter(property=OuterRef('pk'), user=user))).prefetch_related('favorited_by')
        else:
            queryset = queryset.annotate(is_favorited=Value(False, output_field=BooleanField()))

        if not user.is_authenticated:
            return queryset.filter(status=Property.StatusType.PUBLISHED).order_by('-created_at')
        
        if user.role in ['admin', 'manager']:
            return queryset.all().order_by('-created_at')
        if user.role == 'agent':
            return queryset.filter(assigned_agent=user).order_by('-created_at')
        
        
        
        return queryset.filter(status=Property.StatusType.PUBLISHED).order_by('-created_at')
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Update daily analytics for views
        update_daily_analytics(instance, "views")

        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAdminOrManager]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAdminOrManager | IsAgentWithFullAccess]
        elif self.action == 'destroy':
            self.permission_classes = [IsAdminOrManager]
        else:
            self.permission_classes = [IsAuthenticated]
            
        return super().get_permissions()
    
    def perform_create(self, serializer):
        property_instance = serializer.save(created_by=self.request.user)
        try:
            property_instance.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):

        try:
            with transaction.atomic():
                property_serializer = self.get_serializer(data=request.data)
                property_serializer.is_valid(raise_exception=True)
                self.perform_create(property_serializer)
                property_instance = property_serializer.instance

                videos = request.FILES.getlist('videos')

                for vid in videos:
                    if not vid:
                        continue
                    if hasattr(vid, 'name') and getattr(vid, 'size', None) and vid.size > 0:
                        PropertyVideo.objects.create(property=property_instance, video=vid)

                media_images = request.FILES.getlist('media_images')
            

                if not media_images:
                    return Response({"error": "At least one media image is required."}, status=status.HTTP_400_BAD_REQUEST)

                # Only save images that are not empty to avoid validation errors
                for img in media_images:
                    if not img:
                        continue
                    if hasattr(img, 'name') and getattr(img, 'size', None) and img.size > 0:
                        PropertyImage.objects.create(property=property_instance, image=img)

                bedrooms_images = request.FILES.getlist('bedrooms_images')
                row_meta = request.data.get('bedrooms_meta', '[]')

                if bedrooms_images and not row_meta:
                    return Response({"error": "Bedroom metadata is required when uploading bedroom images."}, status=status.HTTP_400_BAD_REQUEST)
                if row_meta and not bedrooms_images:
                    return Response({"error": "At least one bedroom image is required when providing bedroom metadata."}, status=status.HTTP_400_BAD_REQUEST)

                bedrooms_meta = []

                if row_meta:
                    try:
                        bedrooms_meta = json.loads(row_meta) 
                    except json.JSONDecodeError:
                        return Response({"error": "Invalid JSON format for bedrooms_meta."}, status=status.HTTP_400_BAD_REQUEST)
                if len(bedrooms_meta) != len(bedrooms_images):
                    return Response({"error": f"The number of bedroom images: {len(bedrooms_images)} and metadata: {len(bedrooms_meta)} entries must match."}, status=status.HTTP_400_BAD_REQUEST)

                for meta in bedrooms_meta:
                    if 'index' not in meta or 'name' not in meta:
                        return Response({"error": "Each bedroom metadata entry must contain 'index' and 'name'."}, status=status.HTTP_400_BAD_REQUEST)
                
                meta_indexes = sorted(m.get('index') for m in bedrooms_meta)

                if meta_indexes != list(range(len(bedrooms_meta))):
                    return Response({"error": "Bedroom metadata 'index' values must be sequential starting from 0."}, status=status.HTTP_400_BAD_REQUEST)
                
                meta_map = {m["index"]: m for m in bedrooms_meta}

                for idx, img in enumerate(bedrooms_images):
                    if not img or getattr(img, "size", 0) <= 0:
                        return Response(
                            {"error": f"Invalid or empty bedroom image at index {idx}."},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    meta = meta_map[idx]
                    BedroomImage.objects.create(
                        property=property_instance,
                        image=img,
                        name=meta.get("name"),
                        description=meta.get("description")
                    )


                
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        property_instance.refresh_from_db()
        final_serializer = self.get_serializer(property_instance)
        headers = self.get_success_headers(final_serializer.data)
        return Response(final_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def property_downloaded(request, pk):
    try:
        prop = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    update_daily_analytics(prop, "downloads")
    return Response({"detail": "Download recorded."}, status=status.HTTP_200_OK)

class BookingViewSet(viewsets.ModelViewSet):
   
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'property__id', 'user__id']
    search_fields = ['property__title', 'user__username', 'user__email']
    ordering_fields = ['check_in', 'check_out', 'created_at', 'status']
    pagination_class = StandardResultsSetPagination


    # optional: you can leave this out; we override filter_queryset anyway
    # filter_backends = []

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            queryset = Booking.objects.none()
        elif getattr(user, "role", None) in ["admin", "manager"]:
            queryset = Booking.objects.all().select_related("property", "user")
        else:
            queryset = Booking.objects.filter(user=user).select_related("property", "user")

        return queryset

    def filter_queryset(self, queryset):
        """
        Completely bypass DRF's DEFAULT_FILTER_BACKENDS (SearchFilter, etc.)
        and implement our own ?search= logic.
        """
        search = self.request.query_params.get("search")
        if not search:
            return queryset

        # Try to parse search as date YYYY-MM-DD
        date_value = None
        try:
            date_value = datetime.strptime(search, "%Y-%m-%d").date()
        except ValueError:
            pass

        # Text search
        q = (
            Q(full_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

        # If looks like a date, include check_in / check_out
        if date_value:
            q |= Q(check_in=date_value) | Q(check_out=date_value)

        return queryset.filter(q)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsOwnerOrAdminOrManager]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrManager]
        else:  # list action
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status=Booking.STATUS.Pending)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        new_status = request.data.get('status')

        if not new_status:
            return Response({"error": "Status required"}, status=400)

        if new_status != booking.status:

            if new_status == 'approved':
                if validate_date_range(booking.property, booking.check_in, booking.check_out):
                    return Response(
                        {"error": "The selected date range overlaps with existing bookings or is invalid."},
                        status=400
                    )
                booking.status = new_status
                update_daily_analytics(booking.property, "bookings")

            elif new_status in ['cancelled', 'rejected', 'completed', 'pending']:
                booking.status = new_status
            else:
                return Response({"error": "Invalid status"}, status=400)
            booking.save()

        # return updated instance ONLY
        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=200)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def get_property_availability(request, property_pk):
    try:
        prop = Property.objects.get(pk=property_pk)
    except Property.DoesNotExist:
        return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        month = int(request.query_params.get('month', datetime.now().month))
        year = int(request.query_params.get('year', datetime.now().year))
    except (ValueError, TypeError):
        return Response({"error": "Invalid month or year parameter."}, status=status.HTTP_400_BAD_REQUEST)

    start_of_month = date(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_of_month = date(year, month, last_day)

    bookings = Booking.objects.filter(
        property=prop,
        status__in=['approved'],
        check_in__lte=end_of_month,
        check_out__gte=start_of_month
    )

    booked_dates = []
    for booking in bookings:
        start = max(booking.check_in, start_of_month)
        end = min(booking.check_out, end_of_month)

        booked_dates.append({
            "start": start.strftime('%Y-%m-%d'),
            "end": end.strftime('%Y-%m-%d')
        })

    return Response(booked_dates, status=status.HTTP_200_OK)

from .models import ReviewStatus
class ReviewViewSet(viewsets.ModelViewSet):
    # serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['property__id', 'rating', 'user__id', 'status']
    search_fields = ['comment', 'property__title', 'user__username']
    ordering_fields = ['rating', 'created_at', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Review.objects.all().select_related('property', 'user')
        return Review.objects.select_related('property', 'user').filter(status=ReviewStatus.APPROVED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReadReviewSerializer
        return ReviewSerializer

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                review_instance = serializer.save(user=request.user)

                images = request.FILES.getlist('images')
                if len(images) > 5:
                    return Response({"error": "You can upload a maximum of 5 images."}, status=status.HTTP_400_BAD_REQUEST)

                for img in images:
                    if img and getattr(img, 'size', 0) > 0:
                        ReviewImage.objects.create(review=review_instance, image=img)
                
                final_serializer = self.get_serializer(review_instance).data
                return Response(final_serializer, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['property__id']
    search_fields = ['property__title', 'property__city']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('property').prefetch_related(
        'property__media_images',
        'property__bedrooms_images'
    )

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        property_id = request.data.get("property")

        if not property_id:
            return Response({"detail": "property is required"}, status=400)

        user = request.user

        favorite = Favorite.objects.filter(user=user, property_id=property_id).first()

        if favorite:
            favorite.delete()
            return Response(
                {"detail": "Removed from favorites", "is_favorited": False},
                status=200
            )

        new_fav = Favorite.objects.create(user=user, property_id=property_id)
        return Response(
            {
                "detail": "Added to favorites",
                "is_favorited": True,
                "data": FavoriteSerializer(new_fav).data
            },
            status=201
        )




class DeshboardViewApi(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        properties = Property.objects.all().count()
        properties_active = Property.objects.filter(status='active').count()
        reviews = Review.objects.all().count()
        users = User.objects.filter(role='agent').count()

        return Response({
            "properties": properties,
            "properties_active": properties_active,
            "reviews": reviews,
            "users": users
        },status=status.HTTP_200_OK)
        



class AnalyticsSummaryView(APIView):

    def get(self, request):

        today = now().date()

        # --- RANGE OR CUSTOM DATE ---
        start_param = request.GET.get("start")
        end_param = request.GET.get("end")
        range_type = request.GET.get("range", "7d")

        if start_param and end_param:
            start_date = date.fromisoformat(start_param)
            end_date = date.fromisoformat(end_param)
        else:
            if range_type == "7d":
                start_date = today - timedelta(days=7)
            elif range_type == "30d":
                start_date = today - timedelta(days=30)
            elif range_type == "90d":
                start_date = today - timedelta(days=90)
            elif range_type == "month":
                start_date = today.replace(day=1)
            elif range_type == "6m":
                start_date = today - timedelta(days=180)
            elif range_type in ["1y", "year"]:
                start_date = today - timedelta(days=365)
            elif range_type.isdigit():
                start_date = today - timedelta(days=int(range_type))
            else:
                start_date = today - timedelta(days=7)

            end_date = today

        range_days = (end_date - start_date).days

        # Grouping logic => ≤60 days = daily, otherwise monthly
        is_monthly = range_days > 60

        # --- BASE QS ---
        analytics_qs = DailyAnalytics.objects.filter(
            date__gte=start_date, date__lte=end_date
        )

        # --- TOTALS ---
        totals = analytics_qs.aggregate(
            total_views=Sum("views"),
            total_downloads=Sum("downloads"),
            total_bookings=Sum("bookings"),
        )

        total_inquiries = ContectUs.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
        ).count()

        # --- PERFORMANCE (Daily or Monthly) ---
        if not is_monthly:
            # DAY-WISE
            performance = (
                analytics_qs
                .annotate(day=TruncDay("date"))
                .values("day")
                .annotate(
                    total_views=Sum("views"),
                    total_downloads=Sum("downloads"),
                    total_bookings=Sum("bookings"),
                )
                .order_by("day")
            )

            # inquiries daily
            inquiry_qs = (
                ContectUs.objects.filter(
                    created_at__date__gte=start_date,
                    created_at__date__lte=end_date,
                )
                .annotate(day=TruncDay("created_at"))
                .values("day")
                .annotate(inquiries=Count("id"))
            )

            inquiry_map = {i["day"]: i["inquiries"] for i in inquiry_qs}

            performance_list = []
            for p in performance:
                day_name = p["day"].strftime("%a")  # Mon, Tue, Wed
                performance_list.append({
                    "name": day_name,
                    "views": p["total_views"] or 0,
                    "downloads": p["total_downloads"] or 0,
                    "bookings": p["total_bookings"] or 0,
                    "inquiries": inquiry_map.get(p["day"], 0),
                })

        else:
            # MONTH-WISE
            performance = (
                analytics_qs
                .annotate(month=TruncMonth("date"))
                .values("month")
                .annotate(
                    total_views=Sum("views"),
                    total_downloads=Sum("downloads"),
                    total_bookings=Sum("bookings")
                )
                .order_by("month")
            )

            # inquiries month-wise
            inquiry_qs = (
                ContectUs.objects.filter(
                    created_at__date__gte=start_date,
                    created_at__date__lte=end_date
                )
                .annotate(month=TruncMonth("created_at"))
                .values("month")
                .annotate(inquiries=Count("id"))
            )

            inquiry_map = {i["month"]: i["inquiries"] for i in inquiry_qs}

            performance_list = []
            for p in performance:
                label = p["month"].strftime("%b")  # Jan, Feb, Mar
                performance_list.append({
                    "name": label,
                    "views": p["total_views"] or 0,
                    "downloads": p["total_downloads"] or 0,
                    "bookings": p["total_bookings"] or 0,
                    "inquiries": inquiry_map.get(p["month"], 0),
                })

        # --- AGENT ANALYTICS ---
        agents = (
            User.objects.filter(role="agent")
            .annotate(
                total_properties=Count("assigned_villas"),
                total_views=Sum("assigned_villas__daily_analytics__views"),
                total_downloads=Sum("assigned_villas__daily_analytics__downloads"),
                total_bookings=Sum("assigned_villas__daily_analytics__bookings"),
            )
            .values(
                "id", "name", "total_properties",
                "total_views", "total_downloads", "total_bookings"
            )
        )

        return Response({
            "range": range_type,
            "start_date": start_date,
            "end_date": end_date,

            "totals": {
                "views": totals["total_views"] or 0,
                "downloads": totals["total_downloads"] or 0,
                "bookings": totals["total_bookings"] or 0,
                "inquiries": total_inquiries,
            },

            "performance": performance_list,
            "agents": list(agents),
        })

from django.db.models import Subquery
from rest_framework import generics
from .serializers import AgentOptimizedSerializer


class AgentSummaryListView(generics.ListAPIView):
    serializer_class = AgentOptimizedSerializer
    permission_classes = [IsAgent]


    def get_queryset(self):
        today = timezone.now().date()
        first_day = today.replace(day=1)

        user_email = self.request.user.email

        monthly_downloads = DailyAnalytics.objects.filter(
            property__assigned_agent=OuterRef("pk"),
            date__gte=first_day,
        ).values('property__assigned_agent') \
         .annotate(total=Sum('downloads')) \
         .values('total')

        return (
            User.objects.filter(role="agent", email=user_email)
            .annotate(
                assigned_properties=Count('assigned_villas', distinct=True),
                active_listings=Count(
                    'assigned_villas',
                    filter=Q(assigned_villas__status="published"),
                    distinct=True,
                ),
                downloads_this_month=Subquery(monthly_downloads[:1]),
            )
            .prefetch_related("assigned_villas")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            empty_data = {
                "id": request.user.id, 
                "name": request.user.name,
                "email": request.user.email,
                "date_joined": request.user.date_joined,
                "assigned_properties": 0,
                "active_listings": 0,
                "downloads_this_month": 0,
                "scheduled_viewings": 0,
            }
            return Response(empty_data)

        # Normal response with serializer
        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
from datetime import datetime


def validate_month_year(month, year):
    """ Strong validation for month & year """
    try:
        month = int(month)
        year = int(year)
    except:
        return False, "month and year must be integers"

    if month < 1 or month > 12:
        return False, "month must be between 1 and 12"

    current_year = datetime.now().year
    if year < 1900 or year > current_year:
        return False, f"year must be between 1900 and {current_year}"

    return True, (month, year)



class AgentMonthlyBookingView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # -------- extract query params --------
        raw_month = request.query_params.get("month")
        raw_year = request.query_params.get("year")

        if not raw_month or not raw_year:
            return Response(
                {"error": "month & year required. Example: ?month=11&year=2025"},
                status=400
            )

        # -------- strong month & year validation --------
        is_valid, result = validate_month_year(raw_month, raw_year)
        if not is_valid:
            return Response({"error": result}, status=400)

        month, year = result

        # -------- prefetch monthly bookings (N+1 fixed) --------
        monthly_bookings = Booking.objects.filter(
            check_in__year=year,
            check_in__month=month,
             status=Booking.STATUS.Approved
        ).order_by("-check_in")

        properties = (
            Property.objects
            .filter(assigned_agent=user)
            .select_related("assigned_agent")
            .prefetch_related(
                Prefetch("bookings", queryset=monthly_bookings, to_attr="monthly_bookings")
            )
        )

        # -------- prepare response --------
        data = []
        for prop in properties:

            booking_list = [
                {
                    "booking_id": b.id,
                    "full_name": b.full_name,
                    "check_in": b.check_in,
                    "check_out": b.check_out,
                    "status": b.status,
                    "total_price": b.total_price,
                }
                for b in prop.monthly_bookings
            ]

            data.append({
                "property_id": prop.id,
                "property_title": prop.title,
                "city": prop.city,
                "total_bookings_this_month": len(prop.monthly_bookings),
                "bookings": booking_list,
            })

        return Response({
            "agent": user.id,
            "month": month,
            "year": year,
            "properties_count": properties.count(),
            "data": data
        })


from .serializers import PropertyAssignmentSerializer

class AssignPropertyView(APIView):
    permission_classes = [IsAdminOrManager]

    def post(self, request):
        serializer = PropertyAssignmentSerializer(data=request.data)
        if serializer.is_valid():
            prop = serializer.validated_data['property_instance']
            agent = serializer.validated_data['agent_instance']

            prop.assigned_agent = agent
            prop.save()

            action = "assigned to" if agent else "removed from"
            agent_name = agent.name if agent else "None"

            return Response(
                {
                    "message": f"Property '{prop.title}' successfully {action} agent {agent_name}",
                    "property_id": prop.id,
                    "assigned_agent": agent.id if agent else None
                }, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


auditlog.register(Property)
auditlog.register(Media)
auditlog.register(Booking)
auditlog.register(PropertyImage)
auditlog.register(BedroomImage)
auditlog.register(Review)
auditlog.register(ReviewImage)
auditlog.register(Favorite)