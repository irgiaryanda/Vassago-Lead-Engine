from fastapi import APIRouter
from pydantic import BaseModel
import aiosqlite

router = APIRouter()

class ScanRequest(BaseModel):
    keyword: str

@router.get("/health")
async def health_check():
    # Return status
    return {"status": "ok", "message": "API is operational"}

@router.get("/api/leads")
async def get_leads():
    # Fetch leads
    async with aiosqlite.connect("leads.sqlite3") as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM company_leads")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

from crawler.engine import run_lead_scan

@router.post("/api/scan")
async def scan_leads(request: ScanRequest):
    leads = await run_lead_scan(request.keyword)
    newly_saved = 0
    
    async with aiosqlite.connect("leads.sqlite3") as db:
        for lead in leads:
            cursor = await db.execute(
                "INSERT OR IGNORE INTO company_leads (company_name, contact_email, website_url) VALUES (?, ?, ?)",
                (lead["company_name"], lead["contact_email"], lead["website_url"])
            )
            if cursor.rowcount > 0:
                newly_saved += 1
        await db.commit()

    return {
        "status": "success",
        "target_keyword": request.keyword,
        "scanned_count": len(leads),
        "newly_saved": newly_saved
    }
