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

@router.post("/api/scan")
async def scan_leads(request: ScanRequest):
    # Process scan
    return {"status": "processing", "target_keyword": request.keyword}
