from app.infrastructure.db.database import _redact_mongodb_uri


def test_redact_empty_uri_returns_empty():
    assert _redact_mongodb_uri("") == ""


def test_redact_uri_with_credentials():
    uri = "mongodb://user:pass@host:27017/db"
    redacted = _redact_mongodb_uri(uri)
    assert "***@" in redacted


def test_redact_uri_without_credentials():
    uri = "mongodb://host:27017/db"
    assert _redact_mongodb_uri(uri) == "<redacted-uri>"
