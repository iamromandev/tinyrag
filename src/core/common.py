import uuid
from datetime import date, datetime, time
from enum import Enum
from typing import Any

import toml
from pydantic import BaseModel, SecretStr


def get_app_version() -> str:
    try:
        with open("pyproject.toml") as f:
            data = toml.load(f)
            return data["project"]["version"]
    except FileNotFoundError:
        return "Version information not found"
    except KeyError:
        return "Version key not found in pyproject.toml"


def serialize(
    obj: Any,
    instructions: dict[type, type] | None = None,
) -> Any:
    if instructions:
        for key, value in instructions.items():
            if isinstance(obj, key):
                return value(obj)

    if isinstance(obj, BaseModel):
        return serialize(obj.model_dump())

    if isinstance(obj, dict):
        return {key: serialize(value) for key, value in obj.items()}

    if isinstance(obj, list | tuple | set):
        return [serialize(item) for item in obj]

    if isinstance(obj, Enum):
        return obj.value

    if isinstance(obj, datetime | date | time):
        return obj.isoformat()

    if isinstance(obj, uuid.UUID):
        return str(obj)

    if isinstance(obj, SecretStr):
        return obj.get_secret_value()

    if isinstance(obj, int | float | bool | str) or obj is None:
        return obj

    if hasattr(obj, "__dict__"):
        return serialize(obj.__dict__)

    raise TypeError(f"Object of type {type(obj)} is not serializable")
