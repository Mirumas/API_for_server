from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import public.users_methods
from public.db import *
from datetime import datetime

app = FastAPI()
create_tables()
populate_classes_table()
f_bilder()

app.include_router(public.users_methods.users_router)
app.include_router(public.users_methods.classes_router)


@app.on_event("startup")
def on_startup():
    open("log.txt", mode="a").write(f"{datetime.utcnow()}: Begin\n")


@app.on_event("shutdown")
def on_shutdown():
    open("log.txt", mode="a").write(f"{datetime.utcnow()}: End\n")


@app.get("/", response_class=PlainTextResponse)
def f_indexH():
    return "<b> Hello User! </b>"
