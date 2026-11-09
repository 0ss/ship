def display_name(name, limit=24):
    """Shorten a guest's name for the guest list.

    Counts characters, not bytes, so non-Latin names (Arabic included) survive
    instead of being stripped, and cuts at a word boundary when shortening.
    """
    name = " ".join(name.strip().split())
    if len(name) <= limit:
        return name.title()
    kept = []
    for word in name.split():
        candidate = " ".join(kept + [word])
        if len(candidate) > limit - 1:
            break
        kept.append(word)
    if not kept:  # a single word longer than the limit
        return name[: limit - 1].title() + "…"
    return " ".join(kept).title() + "…"
