from fastapi import FastAPI
from app.db.database import init_database
from app.api.auth import router as auth_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_database()

app.include_router(auth_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)