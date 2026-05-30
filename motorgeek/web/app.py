# motorgeek/web/app.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pathlib import Path

from motorgeek.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="MotorGeek", description="Car analysis and comparison tool", lifespan=lifespan)
BASE_DIR = Path(__file__).parent
app.add_middleware(SessionMiddleware, secret_key="motorgeek-session-secret-change-in-production")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/cars")


@app.get("/cars", name="cars")
def cars_list(request: Request) -> HTMLResponse:
    from motorgeek.web.routes.cars import list_cars
    return list_cars(request)


@app.get("/cars/{car_id}", name="car_detail")
def car_detail(car_id: int, request: Request) -> HTMLResponse:
    from motorgeek.web.routes.cars import detail_car
    return detail_car(car_id, request)


@app.get("/cars/{car_id}/edit", name="car_edit")
def car_edit(car_id: int, request: Request) -> HTMLResponse:
    from motorgeek.web.routes.cars import edit_car_get
    return edit_car_get(car_id, request)


@app.post("/cars/{car_id}/edit", name="car_edit_post")
def car_edit_post(car_id: int, request: Request) -> HTMLResponse:
    from motorgeek.web.routes.cars import edit_car_post
    return edit_car_post(car_id, request)


@app.post("/cars/{car_id}/delete", name="car_delete")
def car_delete(car_id: int, request: Request) -> HTMLResponse:
    from motorgeek.web.routes.cars import delete_car_post
    return delete_car_post(car_id, request)


@app.get("/compare", name="compare")
def compare_page(request: Request) -> HTMLResponse:
    from motorgeek.web.routes.compare import index
    return index(request)


@app.post("/compare", name="compare_post")
def compare_post(request: Request, car_ids: str = Form(...)) -> HTMLResponse:
    from motorgeek.web.routes.compare import compare_post
    return compare_post(request, car_ids)


# ── Agentic Ingestion ──

@app.get("/ingest", name="ingest")
async def ingest_page(request: Request) -> HTMLResponse:
    from motorgeek.web.routes.ingest import ingest_page
    return await ingest_page(request)


@app.post("/ingest", name="ingest_create")
async def ingest_create(request: Request) -> HTMLResponse:
    from motorgeek.web.routes.ingest import ingest_create
    return await ingest_create(request)


@app.get("/ingest/{session_id}", name="ingest_review")
async def ingest_review(session_id: int, request: Request) -> HTMLResponse:
    from motorgeek.web.routes.ingest import ingest_review
    return await ingest_review(request, session_id)


@app.post("/ingest/{session_id}/message", name="ingest_message")
async def ingest_message(session_id: int, request: Request) -> HTMLResponse:
    from motorgeek.web.routes.ingest import ingest_message
    return await ingest_message(request, session_id)


@app.post("/ingest/{session_id}/save", name="ingest_save")
async def ingest_save(session_id: int, request: Request) -> HTMLResponse:
    from motorgeek.web.routes.ingest import ingest_save
    return await ingest_save(request, session_id)


@app.post("/ingest/{session_id}/discard", name="ingest_discard")
async def ingest_discard(session_id: int, request: Request) -> HTMLResponse:
    from motorgeek.web.routes.ingest import ingest_discard
    return await ingest_discard(request, session_id)


@app.get("/query", name="query")
def query_page(request: Request) -> HTMLResponse:
    from motorgeek.web.routes.query import query_page
    return query_page(request)


@app.post("/query", name="query_post")
def query_post(request: Request, message: str = Form(...)) -> HTMLResponse:
    from motorgeek.web.routes.query import query_post
    return query_post(request, message)


@app.get("/query/clear", name="query_clear")
def query_clear(request: Request) -> HTMLResponse:
    from motorgeek.web.routes.query import query_clear
    return query_clear(request)


@app.post("/query/agent", name="query_agent")
def query_agent(request: Request, message: str = Form(...)) -> HTMLResponse:
    from motorgeek.web.routes.query import query_agent
    return query_agent(request, message)