from fastapi import FastAPI
import uvicorn
import random

app = FastAPI()

@app.get("/")
def root():
    return {"message":"hello world"}

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)

