from app.utils.timeutils import utcnow, today_utc, days_ago


def test_utcnow_timezone():
    now = utcnow()
    assert now.tzinfo is not None


def test_today_and_days_ago():
    t = today_utc()
    past = days_ago(1)
    assert past < t
