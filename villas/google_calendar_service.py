import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'eastmond-villas-google-service.json')

SCOPES = ['https://www.googleapis.com/auth/calendar']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=creds)

def create_calendar_for_property(property_title):
    calendar_body = {
        'summary': f'Eastmond Villas - {property_title}',
        'timeZone': 'UTC'
    }

    created_calendar = service.calendars().insert(body=calendar_body).execute()

    rule = {
        'scope': {
            'type': 'default',
        },
        'role': 'reader'
    }

    service.acl().insert(calendarId=created_calendar['id'], body=rule).execute()
    return created_calendar['id']

def check_availability(calendar_id, start_time, end_time):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time.isoformat() + 'Z',
        timeMax=end_time.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])
    return not events

def create_event_for_booking(calendar_id, booking):
    event_body = {
        'summary': f'Booked: {booking.property.title} by {booking.full_name}',
        'description': f'Guest: {booking.full_name}\nEmail: {booking.email}\nPhone: {booking.phone}',
        'start': {
            'date': booking.check_in.strftime('%Y-%m-%d'),
            'timeZone': 'Asia/Dhaka',
        },
        'end': {
            'date': (booking.check_out + timedelta(days=1)).strftime('%Y-%m-%d'),
            'timeZone': 'Asia/Dhaka',
        },
    }
    event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
    return event.get('id')

def delete_event_for_booking(calendar_id, event_id):
    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return True
    except Exception:
        return False