from fastapi import FastAPI, Request, HTTPException
import uvicorn
from fastapi.responses import RedirectResponse, HTMLResponse
from db import *
from datetime import datetime
from hash import *
from args import *
from response import *
import logging
import time

args = get_args()

DATABASE = args.db_name
create(DATABASE)
app = FastAPI()

@app.post("/create_url")
async def create_url(request: Request):
    try: 
        urljson = await request.json()
        logging.debug(f"create_url requested with {urljson['url']}")
        if 'alias' in urljson:
            logging.debug(f"create_url requested with {urljson['url']} and {urljson['alias']}")
            if urljson['alias'].isalnum():
                insert(DATABASE, urljson['url'], urljson['alias'])
                #print("inserted successfully")
                logging.info("inserted successfully")
                return {"url":urljson['url'], "alias":urljson['alias']}
            else:
                raise ValueError("Alias must be alphanumeric")
        if args.disable_random_alias:
            raise KeyError("Alias must be provided")
        alias = generate_hash(urljson['url'], str(datetime.now()))
        insert(DATABASE, urljson['url'], alias)
        #print("inserted successfully")
        logging.info("inserted successfully")
        return {"url":urljson['url'], "alias":alias}
    except ValueError as e:
        logging.error(str(e))
        raise HTTPException(status_code=Response.INVALID.code, detail=str(e))
    except KeyError as e:
        logging.error(str(e))
        raise HTTPException(status_code=Response.BAD_REQUEST.code, detail=str(e))
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=Response.INTERNAL_SERVER_ERROR.code, detail=str(e))

@app.get("/list_all")
def list_all():
    try:
        logging.debug(f"listing all urls in {DATABASE}")
        return list_urls(DATABASE)
    except Exception as e:
        logging.error("Failed to list urls")
        return {"message": "Failed to list urls"}

@app.get("/find/{alias}")
def find(alias):
    try: 
        logging.debug(f"find requested url with alias: {alias}")
        result = retrieve(DATABASE, alias)
        #print("url found successfully")
        #print(result)
        logging.info("url found successfully: "+ result)
        return RedirectResponse(url=result, status_code=308)

    except Exception as e:
        #print("url not found")
        logging.error("url not found")
        raise HTTPException(status_code=Response.NOT_FOUND.code, detail="Item not found")

@app.delete("/delete/{alias}")
def delete(alias: str):
    try: 
        logging.debug(f"delete requested url with alias: {alias}")
        result = retrieve(DATABASE, alias)
        if result is not None:
            delete_url(DATABASE, alias)
            #print("alias deleted successfully")
            logging.info("alias deleted successfully")
            return {"message": "alias deleted successfully"}
        else:
            #print("alias not found")
            logging.error("alias not found")
            raise HTTPException(status_code=Response.NOT_FOUND.code, detail="Item not found")
    except Exception:
        #print("error during deletion")
        logging.error("error during deletion")
        raise HTTPException(status_code=Response.NOT_FOUND.code, detail="Item not found")
    
@app.exception_handler(HTTPException)
async def http_exception_handler(request, ex):
    enu = http_to_enum.get(ex.status_code, Response.INTERNAL_SERVER_ERROR)
    return HTMLResponse(content=enu.message, status_code=enu.code)

logging.Formatter.converter = time.gmtime

logging.basicConfig(
    format="%(asctime)s.%(msecs)03dZ %(levelname)s:%(name)s:%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=40-args.v*10,
)

if __name__ == "__main__":
    uvicorn.run("server:app", host=args.host, port=args.port, reload=True)

#python -m uvicorn server:app --reload
#python server.py --db-name my.db
    
