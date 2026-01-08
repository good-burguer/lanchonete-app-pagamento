from app.api import check


def test_health_check_returns_ok():
    assert check.health_check() == {"status": "ok"}


def test_health_db_check_accepts_db_param():
    class DummyDB:
        pass

    assert check.health_db_check(db=DummyDB()) == {"status": "connected"}
