from __future__ import annotations

import json
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


USER_AGENT = "biosci-radar/0.1 (local research assistant)"


def get_text(url: str, params: dict[str, str | int] | None = None, timeout: int = 45) -> str:
    if params:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}{urlencode(params)}"
    request = Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urlopen(request, timeout=timeout) as response:
                return response.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError, TimeoutError) as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed for {url}: {last_error}")


def get_json(url: str, params: dict[str, str | int] | None = None, timeout: int = 45):
    return json.loads(get_text(url, params=params, timeout=timeout))
