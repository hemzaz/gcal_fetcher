import datetime
import pickle
import os.path
import pytz

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)


def find_free_slots(events, start_of_day, end_of_day):
    free_slots = []
    current_start = start_of_day

    for event in events:
        event_start = datetime.datetime.fromisoformat(
            event["start"].get("dateTime") or event["start"].get("date")
        )
        event_end = datetime.datetime.fromisoformat(
            event["end"].get("dateTime") or event["end"].get("date")
        )

        if event_start > current_start:
            free_slots.append((current_start, event_start))

        current_start = max(current_start, event_end)

    if current_start < end_of_day:
        free_slots.append((current_start, end_of_day))

    return free_slots


def main():
    service = get_calendar_service()

    # Define your timezone
    tz = pytz.timezone("Asia/Jerusalem")

    today = datetime.date.today()
    start_of_next_week = today + datetime.timedelta((7 - today.weekday()) % 7)
    dates = [
        start_of_next_week + datetime.timedelta(days=i)
        for i in range(7)
        if (start_of_next_week + datetime.timedelta(days=i)).weekday() not in [4, 5]
    ]

    for date in dates:
        start_of_day = datetime.datetime.combine(date, datetime.time(9, 0)).replace(
            tzinfo=tz
        )
        end_of_day = datetime.datetime.combine(date, datetime.time(17, 0)).replace(
            tzinfo=tz
        )

        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=start_of_day.isoformat(),
                timeMax=end_of_day.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        free_slots = find_free_slots(events, start_of_day, end_of_day)

        for slot in free_slots:
            start_time = slot[0].astimezone(tz).strftime("%H:%M")
            end_time = slot[1].astimezone(tz).strftime("%H:%M")
            print(f"{date.strftime('%a %d.%m')} {start_time}-{end_time} IST")


if __name__ == "__main__":
    main()
