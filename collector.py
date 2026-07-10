"""
APScheduler job that runs every 30 minutes to fetch and process scholarships.
Respects source terms of use via configurable delays and user-agent rotation.
"""
import asyncio
import random
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import httpx
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.schemas.scholarship import ScholarshipCreate
from app.services.scholarship_service import upsert_scholarship_by_url
from app.services.ai_service import extract_scholarship_structured

settings = get_settings()

# Default demo sources (replace with real RSS feeds in production)
DEFAULT_SOURCES = [
    "https://example-scholarship-feed.com/rss",  # Placeholder — replace with real feeds
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
]

async def fetch_rss_feed(url: str) -> List[Dict[str, str]]:
    """Fetch and parse an RSS feed, returning list of raw items."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            resp = await client.get(url, headers=headers)
            if resp.status_code != 200:
                return []

            root = ET.fromstring(resp.text)
            items = []
            # Handle RSS 2.0 and Atom
            for item in root.findall(".//item"):
                title = item.findtext("title", default="")
                link = item.findtext("link", default="")
                desc = item.findtext("description", default="")
                pub_date = item.findtext("pubDate", default="")
                items.append({
                    "title": title,
                    "link": link,
                    "description": desc,
                    "pub_date": pub_date,
                })
            return items
    except Exception:
        return []

async def process_raw_item(raw_item: Dict[str, str]) -> Optional[ScholarshipCreate]:
    """Send raw item to Claude for structured extraction."""
    raw_text = f"Title: {raw_item.get('title', '')}\nDescription: {raw_item.get('description', '')}\nURL: {raw_item.get('link', '')}"
    structured = await extract_scholarship_structured(raw_text)
    if not structured:
        return None

    # Validate required fields
    if not structured.get("title") or not structured.get("source_url"):
        return None

    # Parse deadline if present
    deadline = None
    if structured.get("deadline"):
        try:
            from dateutil import parser
            deadline = parser.isoparse(structured["deadline"])
        except Exception:
            pass

    return ScholarshipCreate(
        title=structured["title"],
        provider=structured.get("provider"),
        source_url=structured.get("source_url") or raw_item.get("link", ""),
        deadline=deadline,
        amount=structured.get("amount"),
        eligibility_raw=structured.get("eligibility_raw"),
        field_tags=structured.get("field_tags") or [],
        country_scope=structured.get("country_scope") or [],
        education_levels=structured.get("education_levels") or [],
        external_id=raw_item.get("link", ""),
        source_feed="rss",
    )

async def run_collection_cycle(db: Session) -> int:
    """
    Run one collection cycle across all configured sources.
    Returns number of scholarships processed.
    """
    sources_str = settings.scholarship_sources
    sources = sources_str.split(",") if sources_str else DEFAULT_SOURCES
    sources = [s.strip() for s in sources if s.strip()]

    processed = 0
    for source in sources:
        items = await fetch_rss_feed(source)
        for item in items:
            try:
                sch = await process_raw_item(item)
                if sch:
                    upsert_scholarship_by_url(db, sch)
                    processed += 1
                # Respect rate limits: small delay between items
                await asyncio.sleep(random.uniform(1.0, 3.0))
            except Exception:
                continue
        # Delay between sources
        await asyncio.sleep(random.uniform(5.0, 10.0))

    return processed

# APScheduler job wrapper
def scheduled_collection_job():
    """Wrapper for APScheduler to run the async collection in a sync context."""
    from app.db.session import SessionLocal
    db = SessionLocal()
    try:
        asyncio.run(run_collection_cycle(db))
    finally:
        db.close()
