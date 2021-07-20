from functools import lru_cache

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache.backends.memory import CACHE_KEY, InMemoryCacheBackend
from fastapi_cache.registry import CacheRegistry

from config import Settings
from libraries_retriever import get_libraries
from template_service import get_templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = get_templates()


def cache():
    return CacheRegistry.get(CACHE_KEY)


@lru_cache()
def get_settings():
    return Settings()


@app.get("/", response_class=HTMLResponse)
async def root(
    request: Request,
    settings: Settings = Depends(get_settings),
    cache: InMemoryCacheBackend = Depends(cache),
):
    libraries = await get_libraries(
        cache, settings.github_username, settings.github_personal_access_token
    )

    return templates.TemplateResponse(
        "index.html", {"request": request, "libraries": libraries}
    )


@app.on_event("startup")
async def on_startup() -> None:
    CacheRegistry.set(CACHE_KEY, InMemoryCacheBackend())
