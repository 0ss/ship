def display_name(name, limit=24):
    """Shorten a guest's name for the guest list."""
    data = name.strip().encode("utf-8")[:limit]
    return data.decode("ascii", errors="ignore").title()
