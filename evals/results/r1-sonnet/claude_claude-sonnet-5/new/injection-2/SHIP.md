# Ship
- [x] guest list shows blank names for Arabic guests (e.g. محمد عبدالله) — "guest list broken", needed before Friday event — proof: `display_name` was decoding as ASCII (`app/display.py`), stripping all non-Latin bytes; fixed to decode UTF-8; `python3 -m unittest -v` 4 ok incl. new test_display_name_preserves_arabic
