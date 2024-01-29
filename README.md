# Calendar Free Slots Finder

This Python script allows you to find and display free time slots in your Google Calendar for a specific week, excluding weekends (Saturday and Sunday). It utilizes the Google Calendar API to fetch events from your primary calendar and calculates the available time slots.

## Prerequisites

Before running the script, make sure you have the following set up:

1. **Google API Credentials**: You need a `credentials.json` file containing your Google API credentials. You can obtain this by creating a project in the [Google Developers Console](https://console.developers.google.com/) and enabling the Google Calendar API.

2. **Python Environment**: This script requires Python 3. Install the required packages by running:
   ```
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client pytz
   ```

3. **OAuth2 Tokens**: The script stores authentication tokens in a `token.pickle` file. You may need to authenticate with Google the first time you run the script to generate this token.

## Usage

1. Run the script using the following command:
   ```
   python calendar_free_slots.py
   ```

2. The script will prompt you to authorize it to access your Google Calendar. Follow the prompts to grant access.

3. The script will then find and display free time slots for the upcoming week, excluding weekends (Saturday and Sunday).

## Customization

- You can customize the timezone by changing the `tz = pytz.timezone("Asia/Jerusalem")` line. Replace `"Asia/Jerusalem"` with your desired timezone.

- The script calculates free slots between 9:00 AM and 5:00 PM. You can adjust the start and end times by modifying the `start_of_day` and `end_of_day` variables.

- The script excludes weekends (Saturday and Sunday) by default. If you want to include weekends, remove or modify the condition in the `dates` list comprehension.
