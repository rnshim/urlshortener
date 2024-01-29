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
from metrics import *
import prometheus_client

args = get_args()
metrics_handler=MetricsHandler.instance()
DATABASE = args.db_name
create(DATABASE)
app = FastAPI()

@app.post("/create_url")
async def create_url(request: Request):
    try:
        with metrics_handler.query_response_time.labels("create").time():
            urljson = await request.json()
            logging.debug(f"create_url requested with {urljson['url']}")
            if 'alias' in urljson:
                logging.debug(f"create_url requested with {urljson['url']} and {urljson['alias']}")
                if urljson['alias'].isalnum():
                    insert(DATABASE, urljson['url'], urljson['alias'])
                    metrics_handler.URL_COUNT.inc()
                    logging.info("inserted successfully")
                    return {"url":urljson['url'], "alias":urljson['alias']}
                else:
                    raise ValueError("Alias must be alphanumeric")
            if args.disable_random_alias:
                raise KeyError("Alias must be provided")
            alias = generate_hash(urljson['url'], str(datetime.now()))
            insert(DATABASE, urljson['url'], alias)
            metrics_handler.url_count.inc()
            logging.info("inserted successfully")
            return {"url":urljson['url'], "alias":alias}
    
    except ValueError as e:
        logging.error(str(e))
        metrics_handler.http_error_count.labels("INVALID").inc()
        raise HTTPException(status_code=Response.INVALID.code, detail=str(e))
    
    except KeyError as e:
        logging.error(str(e))
        metrics_handler.http_error_count.labels("BAD REQUEST").inc()
        raise HTTPException(status_code=Response.BAD_REQUEST.code, detail=str(e))
    
    except Exception as e:
        logging.error(str(e))
        metrics_handler.http_error_count.labels("INTERNAL SERVER ERROR").inc()
        raise HTTPException(status_code=Response.INTERNAL_SERVER_ERROR.code, detail=str(e))

@app.get("/list_all")
def list_all():
    try:
        with metrics_handler.query_response_time.labels("list").time():
            logging.debug(f"listing all urls in {DATABASE}")
            return list_urls(DATABASE)
    except Exception as e:
        logging.error("Failed to list urls")
        return {"message": "Failed to list urls"}

@app.get("/find/{alias}")
def find(alias):
    try: 
        with metrics_handler.query_response_time.labels("find").time():
            logging.debug(f"find requested url with alias: {alias}")
            result = retrieve(DATABASE, alias)
            logging.info("url found successfully: "+ result)
            return RedirectResponse(url=result, status_code=308)

    except Exception as e:
        metrics_handler.http_error_count.labels("NOT FOUND").inc()
        logging.error("url not found")
        raise HTTPException(status_code=Response.NOT_FOUND.code, detail="Item not found")

@app.delete("/delete/{alias}")
def delete(alias: str):
    try: 
        with metrics_handler.query_response_time.labels("delete").time():
            logging.debug(f"delete requested url with alias: {alias}")
            result = retrieve(DATABASE, alias)
            if result is not None:
                delete_url(DATABASE, alias)
                metrics_handler.url_count.dec()
                logging.info("alias deleted successfully")
                return {"message": "alias deleted successfully"}
            else:
                logging.error("alias not found")
                raise HTTPException(status_code=Response.NOT_FOUND.code, detail="Item not found")
    except Exception:
        metrics_handler.http_error_count.labels("NOT FOUND").inc()
        logging.error("error during deletion")
        raise HTTPException(status_code=Response.NOT_FOUND.code, detail="Item not found")
    
@app.exception_handler(HTTPException)
async def http_exception_handler(request, ex):
    enu = http_to_enum.get(ex.status_code, Response.INTERNAL_SERVER_ERROR)
    return HTMLResponse(content=enu.message, status_code=enu.code)

@app.get('/metrics')
def get_metrics():
    return HTMLResponse(
        media_type="text/plain",
        content=prometheus_client.generate_latest(),
    )

logging.Formatter.converter = time.gmtime

logging.basicConfig(
    format="%(asctime)s.%(msecs)03dZ %(levelname)s:%(name)s:%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.ERROR-args.verbose*10,
)

if __name__ == "__main__":
    uvicorn.run("server:app", host=args.host, port=args.port, reload=True)

if __name__ == "server":
    initial_url_count = get_number_of_entries(DATABASE)
    MetricsHandler.url_count.inc(initial_url_count)

#python -m uvicorn server:app --reload
#python server.py --db-name my.db
    
