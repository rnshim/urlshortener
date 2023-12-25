from fastapi import FastAPI
import uvicorn
import random
from db import *

DATABASE = "url_shortener.db"
create(DATABASE)
app = FastAPI()

@app.get("/create_url")
def create_url(url: str, alias: str):
    try: 
        insert(DATABASE, url, alias)
        print("inserted successfully")
        return {"url":url, "alias":alias}
    except Exception as e:
        print("could not insert")
        return {"message": "Failed to create URL"}

@app.get("/list_all")
def list_all():
    try:
        urls = list_(DATABASE)
        return [{"url": url} for url in urls]
    except Exception as e:
        return {"message": "Failed to list urls"}

@app.get("/find/{alias}")
def find(alias):
    try: 
        result = retrieve(DATABASE, alias)
        print("url found successfully")
        return {"url": result}
    except Exception as e:
        print("url not found")
        return {"message": "url not found"}

@app.get("/delete/{alias}")
def delete(alias):
    try: 
        delete_url(DATABASE, alias)
        print("alias deleted successfully")
        return {"message": "alias deleted successfully"}
    except Exception as e:
        print("alias not deleted")
        return {"message": "alias not found"}


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)

