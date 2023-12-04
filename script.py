#!/usr/bin/env python3
import subprocess
import time
from datetime import datetime, timedelta
import re
import os
import sys

def parse_date(date_str):
    # Updated to handle the full format including preceding text
    match = re.search(r"date \w+, (\d{1,2}) (\w+) (\d{4}) at (\d{2}:\d{2}:\d{2})", date_str)
    if match:
        day, month, year, time_str = match.groups()
        date_formatted = f"{day} {month} {year} {time_str}"
        return datetime.strptime(date_formatted, "%d %B %Y %H:%M:%S")
    else:
        raise ValueError(f"Invalid date format: {date_str}")

def get_next_event():
    current_working_directory = os.path.dirname(sys.modules['__main__'].__file__)
    script = f'osascript {current_working_directory}/event.scpt'
    try:
        output = subprocess.check_output(script, shell=True).decode('utf-8').strip()
        print(f"AppleScript Output: {output}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing AppleScript: {e}")
        return None, None, None

    if output == "No upcoming events" or not output:
        return None, None, None
    try:
        # Splitting the output into parts and extracting date strings
        parts = output.split(", date ")
        title = parts[0].split(",")[0]
        start = parse_date("date " + parts[1])
        end = parse_date("date " + parts[2])
    except Exception as e:
        print(f"Error parsing AppleScript output: {e}")
        return None, None, None

    return title, start, end

def send_notification(message, title):
    message = message.replace('"', '\\"')  # Escape double quotes
    script = f'display notification "{message}" with title "{title}"'
    try:
        subprocess.call(['osascript', '-e', script])
    except subprocess.CalledProcessError as e:
        print(f"Error sending notification: {e}")

def schedule_notifications(title, start, end):
    notification_times = [end - timedelta(minutes=5), end - timedelta(minutes=2), end]

    for notify_time in notification_times:
        print(f"Scheduled notification at {notify_time.strftime('%Y-%m-%d %H:%M:%S')} for event '{title}'")
        current_time = datetime.now()
        if current_time < notify_time:
            time_to_wait = (notify_time - current_time).total_seconds()
            time.sleep(time_to_wait)
            if notify_time == end:
                send_notification(f"If you aren't already on the move, you're running late!", f"⛔ Your meeting is over ⛔")
            else:
                time_left = int((end - notify_time).total_seconds() / 60)
                if (time_left == 2):
                    send_notification(f"You have {time_left} minutes to get to your next meeting 🏃", f"🚨 '{title}' has ended")
                else:
                    send_notification(f"Start wrapping things up – '{title}' ends soon 🧘", f"⏰ {time_left} minutes left")

def main():
    while True:
        title, start, end = get_next_event()

        if title is None:
            print("No upcoming events or unable to fetch events. Checking again in 5 minutes.")
            time.sleep(300)  # Wait for 5 minutes before re-checking
            continue

        current_time = datetime.now()
        if current_time >= start:
            # If the event has already started, begin scheduling notifications
            schedule_notifications(title, start, end)
        else:
            # If the event has not started, wait 5 minutes before re-checking
            print(f"Next event '{title}' starts at {start}. Waiting 5 minutes before re-checking.")
            time.sleep(300)

if __name__ == "__main__":
    main()