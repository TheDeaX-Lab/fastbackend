from fastapi import FastAPI
from routers import bilets
import sys
import os

sys.path.append(os.getcwd())

app = FastAPI()


app.include_router(bilets.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)