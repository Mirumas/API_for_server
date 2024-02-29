from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from public.users_methods import users_router, info_router
from public.db import create_tables
from datetime import datetime

app = FastAPI()
create_tables()

app.include_router(users_router)
app.include_router(info_router)


@app.on_event("startup")
def on_startup():
    open("log_p.txt", mode="a").write(f'{datetime.utcnow()}: Begin\n')


@app.on_event("shutdown")
def on_shutdown():
    open("log_p.txt", mode="a").write(f'{datetime.utcnow()}: End\n')


@app.get('/', response_class=PlainTextResponse)
def f_indexH():
    return "<b> Hello User! </b>"
