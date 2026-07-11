import aiosqlite

async def init_db():
    # Initialize database
    async with aiosqlite.connect("leads.sqlite3") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS company_leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT,
                website_url TEXT UNIQUE,
                contact_email TEXT NULL,
                industry TEXT NULL,
                lead_score INTEGER DEFAULT 0,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
