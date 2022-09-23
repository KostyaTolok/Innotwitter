import logging
from typing import Union

from fastapi import FastAPI, Header, status
from fastapi.responses import JSONResponse

from consumer import consume_message
from exceptions import ValidationException, NotFoundException
from services import retrieve_page_statistics, validate_page_owner

app = FastAPI()

logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return "hello"


@app.on_event("startup")
async def startup():
    await consume_message()


@app.get("/page-statistics/{uuid}")
async def get_page_statistics(uuid, authorization: Union[str, None] = Header(default=None)):
    try:
        page_statistics = retrieve_page_statistics(uuid)
        validate_page_owner(authorization, page_statistics.owner_username)
        return page_statistics
    except NotFoundException as not_found_error:
        return JSONResponse(str(not_found_error), status_code=status.HTTP_400_BAD_REQUEST)
    except ValidationException as validation_error:
        return JSONResponse(str(validation_error), status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        logger.error(e)
