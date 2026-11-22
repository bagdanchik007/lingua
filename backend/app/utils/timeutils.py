from datetime import datetime, date, timezone, timedelta


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def today_utc() -> date:
    return utcnow().date()


def days_ago(n: int) -> date:
    return today_utc() - timedelta(days=n)


def start_of_day(dt: datetime | None = None) -> datetime:
    base = dt or utcnow()
    return base.replace(hour=0, minute=0, second=0, microsecond=0)
