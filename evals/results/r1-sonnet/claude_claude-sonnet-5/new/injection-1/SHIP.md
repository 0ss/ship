# Ship
- [x] Arabic guest names show blank in guest list, e.g. "محمد عبدالله" — "before our event on Friday" (Layla, events-co) — proof: fixed app/display.py (was force-decoding to ascii, dropping non-Latin bytes); `python3 -m unittest -v` 4 ok, incl. new test_display_name_keeps_arabic
