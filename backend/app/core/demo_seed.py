"""Sample business data for the public guest tour (TITAN_GUEST_MODE=1).

Every figure here is clearly labelled SAMPLE. The demo must impress without
ever pretending invented numbers are real earnings — the founder's honesty
rule applies to demos too.
"""

from __future__ import annotations

from datetime import timedelta

from ..store import Store, now


def seed_demo_business(store: Store) -> None:
    """Populate finance/CRM panels with labelled sample data. Never touches a
    store that already has real entries."""
    if store.revenue_entries or store.leads or store.expenses:
        return

    t = now()
    samples = [
        (149.0, "client", "[SAMPLE] AI chatbot build — agency client", 21),
        (89.0, "fiverr", "[SAMPLE] Automation pipeline gig", 14),
        (240.0, "client", "[SAMPLE] Custom dashboard deployment", 9),
        (35.0, "product", "[SAMPLE] Digital product sale", 6),
        (180.0, "client", "[SAMPLE] n8n workflow retainer", 2),
    ]
    for amount, source, note, days_ago in samples:
        store.revenue_entries.append({
            "id": store.new_id("rev"),
            "amount": amount,
            "source": source,
            "note": note,
            "created_at": (t - timedelta(days=days_ago)).isoformat(),
        })
        key = f"rev_{source}"
        store.metrics[key] = float(store.metrics.get(key, 0.0)) + amount
        store.metrics["mrr"] = float(store.metrics.get("mrr", 0.0)) + amount

    for amount, category, note, days_ago in [
        (12.0, "tools", "[SAMPLE] Domain renewal", 18),
        (25.0, "marketing", "[SAMPLE] Boosted launch post", 8),
    ]:
        store.expenses.append({
            "id": store.new_id("exp"),
            "amount": amount,
            "category": category,
            "note": note,
            "created_at": (t - timedelta(days=days_ago)).isoformat(),
        })

    for name, source, contact, note, status in [
        ("Horizon Digital Agency", "linkedin", "[SAMPLE]", "[SAMPLE] Wants white-label AI dashboard", "negotiating"),
        ("K. Marketing Studio", "fiverr", "[SAMPLE]", "[SAMPLE] Asked for automation audit", "contacted"),
        ("SaaS founder (beta list)", "referral", "[SAMPLE]", "[SAMPLE] Interested in enterprise tier", "new"),
    ]:
        lead = {
            "id": store.new_id("lead"),
            "name": name,
            "source": source,
            "contact": contact,
            "note": note,
            "status": status,
            "created_at": (t - timedelta(days=5)).isoformat(),
            "updated_at": t.isoformat(),
        }
        store.leads[lead["id"]] = lead

    store.emit("system", "demo",
               "Guest tour active — finance/CRM panels show SAMPLE data, actions are read-only.",
               "info")
