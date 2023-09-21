from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def initial_route():
    return {"status": 200}