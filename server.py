from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from db import *

DATABASE = "url_shortener.db"
create(DATABASE)
app = FastAPI()

@app.post("/create_url")
async def create_url(request: Request):
    try: 
        urljson = await request.json()
        insert(DATABASE, urljson['url'], urljson['alias'])
        print("inserted successfully")
        return {"url":urljson['url'], "alias":urljson['alias']}
    except Exception as e:
        print("could not insert")
        return {"message": "Failed to create URL"}

@app.get("/list_all")
def list_all():
    try:
        return list_urls(DATABASE)
    except Exception as e:
        return {"message": "Failed to list urls"}

@app.get("/find/{alias}")
def find(alias):
    try: 
        result = retrieve(DATABASE, alias)
        print("url found successfully")
        print(result)
        return RedirectResponse(url=result, status_code=308)

    except Exception as e:
        print("url not found")
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/delete/{alias}")
def delete(alias: str):
    try: 
        delete_url(DATABASE, alias)
        print("alias deleted successfully")
        return {"message": "alias deleted successfully"}
    except Exception as e:
        print("alias not deleted")
        return {"message": "alias not found"}


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)

