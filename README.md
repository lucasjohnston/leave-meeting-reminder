# leave-meeting-reminder ⏰

I'm late to everything. It's not a great trait, and I'm trying to get better at it, so I put together this simple Python/AppleScript file to send me notifications 5mins before the end of a meeting, 2mins before the end of a meeting, and at the end of a meeting.
It uses the native Apple Calendar app, which I've connected to my Google Calendar (and set to sync every 1min in Apple Calendar preferences).

### How does it work?

- It checks every 5mins if an event is occuring in your calendar
- If an event occurs, it'll check to see if you've RSVP'd yes + whether there's a Google Meet/Zoom link in the event description
- If both of those are true, it'll schedule notifications for 5mins before the end of the meeting, 2mins before the end of the meeting, and at the end of the meeting
- After you've been notified, it'll go back to the start to check for the next event

### How can I install this?

1. Open `event.scpt` in Script Editor and change the "Calendar Name" and "Email" variables to your own.
2. Open `com.lujstn.leave-meeting-reminder.plist` and change the absolute path to wherever this directory is located on your computer.
3. Move the launchd plist file to `/Library/LaunchAgents`
4. Set the correct permissions on the plist file:

```
  sudo chown root:wheel /Library/LaunchAgents/com.lujstn.leave-meeting-reminder.plist
  sudo chmod 644 /Library/LaunchAgents/com.lujstn.leave-meeting-reminder.plist
```

5. Run `launchctl load /Library/LaunchAgents/com.lujstn.leave-meeting-reminder.plist` in your terminal
6. Verify that the script is running by running `launchctl list | grep com.lujstn.leave-meeting-reminder` in your terminal

### Notes

- If you want to check it's running properly, refer to the `/tmp/com.lujstn.leave-meeting-reminder.out` and `/tmp/com.lujstn.leave-meeting-reminder.err` files.
- If you're changing the Python script between reboots, make sure to run `launchctl unload /Library/LaunchAgents/com.lujstn.leave-meeting-reminder.plist` and then `launchctl load /Library/LaunchAgents/com.lujstn.leave-meeting-reminder.plist` to reload the script.
