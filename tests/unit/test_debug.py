import pytest
from fastapi import HTTPException

from app.adapters.utils.debug import var_dump_die


def test_var_dump_die_raises_http_exception():
    with pytest.raises(HTTPException) as exc_info:
        var_dump_die({"key": "value"})

    exc = exc_info.value
    assert exc.status_code == 400
    # detail is the debug payload dict
    assert isinstance(exc.detail, dict)
    assert exc.detail.get("debug") is True
    assert "location" in exc.detail
    assert "data" in exc.detail
