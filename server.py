from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from db import *
from datetime import datetime
from hash import *
from args import *
import enum

args = get_args()

DATABASE = args.db_name
create(DATABASE)
app = FastAPI()

@app.post("/create_url")
async def create_url(request: Request):
    try: 
        urljson = await request.json()
        if 'alias' in urljson:
            if urljson['alias'].isalnum():
                insert(DATABASE, urljson['url'], urljson['alias'])
                print("inserted successfully")
                return {"url":urljson['url'], "alias":urljson['alias']}
            else:
                raise ValueError("Alias must be alphanumeric")
        if args.disable_random_alias:
            raise KeyError("Alias must be provided")
        alias = generate_hash(urljson['url'], str(datetime.now()))
        insert(DATABASE, urljson['url'], alias)
        print("inserted successfully")
        return {"url":urljson['url'], "alias":alias}
    except ValueError as e:
        raise HTTPException(status_code=Response.INVALID.status_code, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=Response.BAD_REQUEST.status_code, detail=str(e))
    except HTTPException as e:
        print("could not insert")
        return {"message": e.detail}
    except Exception as e:
        print("could not insert")
        return {"message": str(e)}

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
        raise HTTPException(status_code=Response.NOT_FOUND.status_code, detail="Item not found")
    
    except HTTPException as e:
        print("could not find")
        return {"message": e.detail}

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
    uvicorn.run("server:app", host=args.host, port=args.port, reload=True)

#python -m uvicorn server:app --reload
    

class Response(enum.Enum):
    OK = (200, "success")
    NOT_FOUND = (404, "not found")
    INVALID = (422, "invalid input")
    BAD_REQUEST = (400, "bad request")
    CONFLICT = (409, "conflict")
    INTERNAL_SERVER_ERROR = (500, "internal server error")

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

http_to_enum = {
    200: Response.OK,
    404: Response.NOT_FOUND,
    422: Response.INVALID,
    400: Response.BAD_REQUEST,
    409: Response.CONFLICT,
    500: Response.INTERNAL_SERVER_ERROR
}