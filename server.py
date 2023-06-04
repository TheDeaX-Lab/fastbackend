from fastapi import FastAPI
from routers import bilets, users, worker, films, seances
import sys
import os

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
]
sys.path.append(os.getcwd())
app = FastAPI()

app.include_router(bilets.router)
app.include_router(users.router)
app.include_router(worker.router)
app.include_router(films.router)
app.include_router(seances.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)