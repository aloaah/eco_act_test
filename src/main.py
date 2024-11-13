from dotenv import load_dotenv

load_dotenv(override=True)

# from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html


from src.database.db import Base, engine
from src.routers.elements.routes import elements_router

Base.metadata.create_all(bind=engine)


app = FastAPI(root_path="/api", docs_url=None, redoc_url=None, title="emission_data")


@app.get("/docs", include_in_schema=False)
def overreding_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json", title=f"{app.title} documentation"
    )


@app.get("/redoc", include_in_schema=False)
def overriding_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json", title=f"{app.title} documentation"
    )


app.include_router(elements_router, prefix="/rest")
