from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router

app = FastAPI()

app.mount("/ui", StaticFiles(directory="ui"), name="ui")
app.include_router(router)

@app.get("/")
async def root():
    return {"status": "Engine is running"}
