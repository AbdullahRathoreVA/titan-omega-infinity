"""Guest-demo visitor tracking — so Abdullah can see when his AI gets opened.

Everything here is intentionally GET-only: guest mode blocks non-GET requests,
and a visit beacon must work for anonymous visitors. We store no IP address and
no personal data — only a coarse browser/OS label and a timestamp.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Query, Request

from ..store import STORE, now
from .. import persistence

router = APIRouter(prefix="/api/demo", tags=["demo"])

_MAX = 5000


def _classify(ua: str) -> tuple[str, str]:
    ua = (ua or "").lower()
    browser = (
        "Edge" if "edg" in ua else
        "Chrome" if "chrome" in ua and "chromium" not in ua else
        "Safari" if "safari" in ua and "chrome" not in ua else
        "Firefox" if "firefox" in ua else
        "Other"
    )
    system = (
        "Android" if "android" in ua else
        "iPhone" if "iphone" in ua or "ipad" in ua else
        "Windows" if "windows" in ua else
        "Mac" if "mac os" in ua or "macintosh" in ua else
        "Linux" if "linux" in ua else
        "Other"
    )
    return browser, system


@router.get("/visit")
def record_visit(request: Request, ref: str = Query(default=""), session: str = Query(default="")) -> dict:
    """Beacon fired once per browser session by the demo front end."""
    browser, system = _classify(request.headers.get("user-agent", ""))
    STORE.demo_visits.append({
        "ts": now().isoformat(),
        "browser": browser,
        "os": system,
        "ref": (ref or "direct")[:120],
        "session": (session or "")[:40],
    })
    if len(STORE.demo_visits) > _MAX:
        STORE.demo_visits = STORE.demo_visits[-_MAX:]
    persistence.save(STORE)
    return {"ok": True}


@router.get("/stats")
def visit_stats() -> dict:
    """Human-readable summary Abdullah can open in a browser anytime:
    https://<demo-space>.hf.space/api/demo/stats"""
    visits = STORE.demo_visits
    now_utc = datetime.now(timezone.utc)

    def _within(hrs: int) -> int:
        cut = now_utc - timedelta(hours=hrs)
        n = 0
        for v in visits:
            try:
                if datetime.fromisoformat(v["ts"]) >= cut:
                    n += 1
            except Exception:
                continue
        return n

    # unique-ish sessions (distinct session ids, ignoring blanks)
    sessions = {v.get("session") for v in visits if v.get("session")}
    by_browser: dict[str, int] = {}
    by_os: dict[str, int] = {}
    for v in visits:
        by_browser[v.get("browser", "Other")] = by_browser.get(v.get("browser", "Other"), 0) + 1
        by_os[v.get("os", "Other")] = by_os.get(v.get("os", "Other"), 0) + 1

    return {
        "total_opens": len(visits),
        "unique_sessions": len(sessions),
        "last_24h": _within(24),
        "last_7d": _within(24 * 7),
        "by_browser": by_browser,
        "by_os": by_os,
        "recent": list(reversed(visits[-25:])),
    }
