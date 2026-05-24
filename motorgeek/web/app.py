# motorgeek/web/app.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from motorgeek.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="MotorGeek", description="Car analysis and comparison tool", lifespan=lifespan)

BASE_DIR = Path(__file__).parent
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


@app.get("/compare", name="compare")
def compare_page(request: Request) -> HTMLResponse:
    from motorgeek.web.routes.compare import index
    return index(request)


@app.post("/compare", name="compare_post")
def compare_post(request: Request, car_ids: str = Form(...)) -> HTMLResponse:
    from motorgeek.web.routes.compare import compare_post
    return compare_post(request, car_ids)