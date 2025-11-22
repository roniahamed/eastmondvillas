
# notifications/utils.py
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notification

User = get_user_model()


def create_notification_for_user(user, title: str, data=None, ):
    """
    Create one notification for a specific user and send WebSocket event.
    """
    if not user:
        return None

    data = data or {}

    # 1) Save in DB
    notif = Notification.objects.create(
        user=user,
        title=title,
        data=data,
    )

    # 2) Real-time push via Channels
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user.id}",                 # must match consumer group_name
        {
            "type": "notify",              # calls async def notify(self, event)
            "payload": {
                "id": notif.id,
                "title": notif.title,
                "data": notif.data,
                "is_read": notif.is_read,
                "created_at": notif.created_at.isoformat(),
            },
        },
    )

    return notif


def notify_admins_and_managers(title: str, data=None):
    """
    Create notifications & send WebSocket messages
    to all users with role 'admin' or 'manager'.
    """
    data = data or {}

    # 🔴 OPTION A: if your User model has a `role` field:
    users = User.objects.filter(role__in=["admin", "manager", "agent"])

    # 🟡 OPTION B: if you don't have `role` and only want staff:
    # users = User.objects.filter(is_staff=True)

    channel_layer = get_channel_layer()

    for user in users:
        notif = Notification.objects.create(
            user=user,
            title=title,
            data=data,
        )

        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "notify",
                "payload": {
                    "id": notif.id,
                    "title": notif.title,
                    "data": notif.data,
                    "is_read": notif.is_read,
                    "created_at": notif.created_at.isoformat(),
                },
            },
        )
