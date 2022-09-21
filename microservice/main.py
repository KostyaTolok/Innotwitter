from fastapi import FastAPI

from consumer import consume_message

app = FastAPI()


@app.get("/")
async def root():
    return "hello"


@app.on_event("startup")
async def startup():
    await consume_message()
