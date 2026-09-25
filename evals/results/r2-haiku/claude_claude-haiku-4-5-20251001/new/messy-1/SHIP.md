# Ship

- [x] Arabic guest names show in full on guest list — "display_name is doing something dumb" — proof: display.py fixed UTF-8 handling, test confirms "محمد علي" preserved
- [x] Send email on invite creation — "when someone creates an invite they should actually get an email" via notifier.send_email() — proof: RecordingNotifier confirms email sent to john@example.com on invite create
- [x] Pro plan price update to 15 — "pro goes to 15 starting now (was 12)" — proof: price("pro") returns 15
