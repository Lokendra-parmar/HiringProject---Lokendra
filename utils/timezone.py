from datetime import timezone
from zoneinfo import ZoneInfo


IST = ZoneInfo("Asia/Kolkata")


def to_ist(dt):
    if not dt:
        return None

    # Database timestamps are currently naive UTC timestamps.
    # Treat them as UTC before converting.
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.astimezone(IST)