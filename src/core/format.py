from __future__ import annotations

from datetime import UTC, datetime


def utc_iso_timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
