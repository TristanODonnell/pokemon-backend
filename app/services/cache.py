from __future__ import annotations
import time
from typing import Any, Callable, Dict, Tuple

_Key = Tuple[Tuple[Any, ...], Tuple[Tuple[str, Any], ...]]


def _make_key(args: tuple, kwargs: dict) -> _Key:
    return (args, tuple(sorted(kwargs.items())))

class TTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self._data: Dict[_Key, Tuple[float, Any]] = {}

    def get(self, key: _Key) -> Any | None:
        item = self._data.get(key)
        if not item:
            return None
        expires_at, value = item
        if time.time() > expires_at:
            self._data.pop(key, None)
            return None
        return value

    def set(self, key: _Key, value: Any) -> None:
        self._data[key] = (time.time() + self.ttl, value)


def ttl_cached(ttl_seconds: int = 300):
    cache = TTLCache(ttl_seconds)

    def decorator(fn: Callable):
        def wrapper(*args, **kwargs):
            key = _make_key(args, kwargs)
            hit = cache.get(key)
            if hit is not None:
                return hit
            result = fn(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator