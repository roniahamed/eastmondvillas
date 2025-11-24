from django.utils import timezone
from .models import DailyAnalytics

def update_daily_analytics(property, field):
    today = timezone.now().date()

    analytics, created = DailyAnalytics.objects.get_or_create(
        property=property,
        date=today
    )

    # increment field
    if field == "views":
        analytics.views += 1
    elif field == "inquiries":
        analytics.inquiries += 1
    elif field == "bookings":
        analytics.bookings += 1
    elif field == "downloads":
        analytics.downloads += 1

    analytics.save()
    return analytics
