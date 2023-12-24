from fastapi import FastAPI
import uvicorn
import random
from db import *

DATABASE = "url_shortener.db"
create(DATABASE)
app = FastAPI()

@app.get("/create_url")
def create_url(url: str, alias: str):
    if insert(DATABASE, url, alias):
        return {"url":url, "alias":alias}
    return {"message": "Failed to create URL"}

@app.get("/list_all")
def list_all():
    urls = list_(DATABASE)
    return [{"url": url} for url in urls]

@app.get("/find/{alias}")
def find(alias):
    result = retrieve(DATABASE, alias)
    return {"url": result} if result else {"message": "Alias not found"}

@app.get("/delete/{alias}")
def delete(alias):
    if delete_url(DATABASE, alias):
        return "alias deleted successfully"
    return "alias not found"


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)

