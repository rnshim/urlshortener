import enum

class Response(enum.Enum):
    OK = (200, "<h1>success</h1>")
    NOT_FOUND = (404, "<h1>URL not found</h1>")
    INVALID = (422, "<h1>invalid input</h1>")
    BAD_REQUEST = (400, "<h1>bad request</h1>")
    CONFLICT = (409, "<h1>conflict</h1>")
    INTERNAL_SERVER_ERROR = (500, "<h1>internal server error</h1>")

    def __init__(self, code, message):
        self.code = code
        self.message = message

http_to_enum = {
    200: Response.OK,
    404: Response.NOT_FOUND,
    422: Response.INVALID,
    400: Response.BAD_REQUEST,
    409: Response.CONFLICT,
    500: Response.INTERNAL_SERVER_ERROR
}