import sys
import asyncio
import subprocess
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from contextlib import asynccontextmanager
from database.db_setup import init_db
from api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure Chromium is installed on the host machine
    try:
        subprocess.run(["playwright", "install", "chromium"], check=False, capture_output=True)
    except Exception as e:
        print(f"INFO: Browser check complete.")
    # Setup database
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(content=b"", media_type="image/x-icon")

app.mount("/ui", StaticFiles(directory="ui"), name="ui")

app.include_router(router)

@app.get("/")
async def root():
    # Return status
    return {"status": "Engine is running"}
