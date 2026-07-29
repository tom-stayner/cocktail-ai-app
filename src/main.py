# =====================================================
# Imports
# =====================================================

from html import escape
from urllib.parse import quote

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src import health_service
from src.config import settings
from src.logging_config import logger
from src.models import Cocktail
from src.services import cocktail_service

# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title=settings.app_name,
    description="""
    A REST API and web application for managing cocktail recipes.

    Built using:
    - FastAPI
    - DynamoDB
    - AWS
    - Python

    Part of my Cloud & AI Engineering learning project.
    """,
    version=settings.app_version,
)

# =====================================================
# Static Files
# =====================================================

app.mount("/static", StaticFiles(directory="static"), name="static")

# =====================================================
# Helper Functions
# =====================================================

MUTATIONS_DISABLED_DETAIL = "Cocktail mutations are disabled"


def render_page(title: str, content: str) -> HTMLResponse:
    safe_title = escape(title)

    return HTMLResponse(f"""
    <html>
    <head>
        <title>{safe_title}</title>
        <link rel="icon" href="/favicon.ico" type="image/svg+xml">
        <link rel="stylesheet" href="/static/main.css">
    </head>

    <body>
        <nav style="margin-bottom:20px;">
            <a href="/">🏠 Home</a> |
            <a href="/cocktails/html">🍸 Cocktails</a> |
            <a href="/docs">📚 API Docs</a>
        </nav>
        <div class="card">
            {content}
            <hr>
            <p style="font-size:0.9em;color:gray;">
                Cocktail AI Project • Built with FastAPI • © 2026 Tom Stayner
            </p>
        </div>
    </body>
    </html>
    """)


def cocktail_html_url(cocktail_id: object) -> str:
    path = f"/cocktails/html/{quote(str(cocktail_id), safe='')}"
    return escape(path, quote=True)


def require_mutations_enabled() -> None:
    if not settings.allow_mutations:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=MUTATIONS_DISABLED_DETAIL,
        )


# =====================================================
# API Health and HTML Routes
# =====================================================


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> FileResponse:
    """Serve the application favicon at the conventional browser URL."""

    return FileResponse("static/favicon.svg", media_type="image/svg+xml")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/live")
def liveness_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": app.title,
        "version": app.version,
    }


@app.get("/health/ready", response_model=None)
def readiness_check() -> dict[str, object] | JSONResponse:
    ready = health_service.is_dynamodb_ready()
    dependency_status = "healthy" if ready else "unhealthy"
    response = {
        "status": dependency_status,
        "service": app.title,
        "version": app.version,
        "dependencies": {
            "dynamodb": {
                "status": dependency_status,
            }
        },
    }

    if not ready:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=response,
        )

    return response


@app.get("/", response_class=HTMLResponse)
def root() -> HTMLResponse:
    cocktails = cocktail_service.get_all_cocktails()
    cocktail_count = len(cocktails)
    logger.debug(
        "[HTML] Rendered home page (cocktail_count=%s)",
        cocktail_count,
    )

    cocktail_list = ""

    for cocktail in cocktails:
        cocktail_url = cocktail_html_url(cocktail["id"])
        cocktail_name = escape(str(cocktail["name"]))
        cocktail_list += f"""
        <li>
            <a href="{cocktail_url}">
                {cocktail_name}
            </a>
        </li>
        """

    safe_app_title = escape(app.title)
    content = f"""
    <h1>🍸 {safe_app_title}</h1>

    <p>
        A simple REST API built with Python and FastAPI.
    </p>

    <p>
        Currently serving <strong>{cocktail_count}</strong> cocktails.
    </p>

    <h2>Available Cocktails</h2>

    <ul>
        {cocktail_list}
    </ul>

    <h2>Useful Links</h2>

    <ul>
        <li><a href="/cocktails">View All Cocktails (JSON)</a></li>
        <li><a href="/cocktails/html">View All Cocktails (HTML)</a></li>
        <li><a href="/docs">Swagger Documentation</a></li>
    </ul>

    <p>
        Served by Tom's Cocktail API
    </p>
    """

    return render_page(app.title, content)


@app.get("/cocktails/html", response_class=HTMLResponse)
def cocktails_html() -> HTMLResponse:
    cocktails = cocktail_service.get_all_cocktails()
    cocktail_count = len(cocktails)

    logger.debug(
        "[HTML] Rendered cocktail library (cocktail_count=%s)",
        cocktail_count,
    )

    rows = ""

    for cocktail in cocktails:
        cocktail_id = escape(str(cocktail["id"]))
        cocktail_url = cocktail_html_url(cocktail["id"])
        cocktail_name = escape(str(cocktail["name"]))
        cocktail_spirit = escape(str(cocktail["spirit"]))
        rows += f"""
        <tr>
            <td>{cocktail_id}</td>
            <td>
                <a href="{cocktail_url}">
                    {cocktail_name}
                </a>
            </td>
            <td>{cocktail_spirit}</td>
        </tr>
        """

    content = f"""
    <h1>🍸 Cocktail Library</h1>

    <table>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Spirit</th>
        </tr>

        {rows}

    </table>

    <br>

    <a class="button" href="/">Home</a>
    """

    return render_page("Cocktails", content)


@app.get("/cocktails/html/{cocktail_id}", response_class=HTMLResponse)
def cocktail_html(cocktail_id: int) -> HTMLResponse:
    item = cocktail_service.get_cocktail(cocktail_id)

    logger.debug(
        "[HTML] Rendered cocktail page (ID %s)",
        cocktail_id,
    )

    ingredients = ""

    for ingredient in item["ingredients"]:
        ingredients += f"<li>{escape(str(ingredient))}</li>"

    cocktail_name = escape(str(item["name"]))
    cocktail_spirit = escape(str(item["spirit"]))

    content = f"""
    <h1>🍸 {cocktail_name}</h1>

    <p>
        <strong>Spirit:</strong> {cocktail_spirit}
    </p>

    <h2>Ingredients</h2>

    <ul>
        {ingredients}
    </ul>

    <br>

    <a class="button" href="/cocktails/html">
        ← Back to Cocktail Library
    </a>
    """

    return render_page(str(item["name"]), content)


# =====================================================
# JSON API Routes
# =====================================================


@app.get("/cocktails")
def get_cocktails() -> list:
    return cocktail_service.get_all_cocktails()


@app.get("/cocktails/{cocktail_id}")
def get_cocktail(cocktail_id: int) -> dict:
    return cocktail_service.get_cocktail(cocktail_id)


@app.post(
    "/cocktails",
    dependencies=[Depends(require_mutations_enabled)],
    include_in_schema=settings.allow_mutations,
)
def create_cocktail(cocktail: Cocktail) -> dict:
    return cocktail_service.create_cocktail(cocktail)


@app.delete(
    "/cocktails/{cocktail_id}",
    dependencies=[Depends(require_mutations_enabled)],
    include_in_schema=settings.allow_mutations,
)
def delete_cocktail(cocktail_id: int) -> dict:
    return cocktail_service.delete_cocktail(cocktail_id)


@app.put(
    "/cocktails/{cocktail_id}",
    dependencies=[Depends(require_mutations_enabled)],
    include_in_schema=settings.allow_mutations,
)
def update_cocktail(cocktail_id: int, cocktail: Cocktail) -> dict:
    return cocktail_service.update_cocktail(cocktail_id, cocktail)
