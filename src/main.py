from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
import boto3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tom's Cocktail API",
    description="""
    A REST API and web application for managing cocktail recipes.

    Built using:
    - FastAPI
    - DynamoDB
    - AWS
    - Python

    Part of my Cloud & AI Engineering learning project.
    """,
        version="0.2.0"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

def render_page(title: str, content: str) -> HTMLResponse:
    return HTMLResponse(f"""
    <html>
    <head>
        <title>{title}</title>
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

class Cocktail(BaseModel):
    id: int
    name: str
    spirit: str
    ingredients: list[str]

dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-southeast-2"
)

table = dynamodb.Table("Cocktails")

logger.info("Cocktail API starting")
logger.info("Connected to DynamoDB table 'Cocktails'")

@app.get("/", response_class=HTMLResponse)
def root():

    logger.info("[HTML] Rendering home page")
    response = table.scan()
    cocktails = response["Items"]
    cocktail_count = len(cocktails)
    logger.info(f"[HTML] Rendered home page with {len(cocktails)} cocktails")

    cocktail_list = ""

    for cocktail in cocktails:
        cocktail_list += f"""
        <li>
            <a href="/cocktails/html/{cocktail['id']}">
                {cocktail['name']}
            </a>
        </li>
        """

    content = f"""
    <h1>🍸 Tom's Cocktail API</h1>

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
        Running locally on FastAPI 🚀
    </p>
    """

    return render_page("Tom's Cocktail API", content)

@app.get("/cocktails")
def get_cocktails():

    logger.info("[API] Retrieving cocktail collection")

    response = table.scan()
    cocktails = response["Items"]

    logger.info(
        f"[API] Returned {len(cocktails)} cocktails"
    )

    return cocktails

@app.get("/cocktails/html", response_class=HTMLResponse)
def cocktails_html():

    logger.info("[HTML] Rendering cocktail library")

    response = table.scan()

    logger.info(
        f"[HTML] Rendered cocktail library with {len(response['Items'])} cocktails"
    )

    rows = ""

    for cocktail in response["Items"]:
        rows += f"""
        <tr>
            <td>{cocktail["id"]}</td>
            <td>
                <a href="/cocktails/html/{cocktail["id"]}">
                    {cocktail["name"]}
                </a>
            </td>
            <td>{cocktail["spirit"]}</td>
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
def cocktail_html(cocktail_id: int):

    logger.info(f"HTML - Loading cocktail page {cocktail_id}")

    response = table.get_item(
        Key={"id": cocktail_id}
    )

    item = response.get("Item")

    if not item:
        logger.warning(f"HTML - Cocktail {cocktail_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Cocktail not found"            
        )
    
    logger.info(
        f"HTML - Displaying '{item['name']}' (ID {cocktail_id})"
    )

    ingredients = ""

    for ingredient in item["ingredients"]:
        ingredients += f"<li>{ingredient}</li>"

    content = f"""
    <h1>🍸 {item["name"]}</h1>

    <p>
        <strong>Spirit:</strong> {item["spirit"]}
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

    return render_page(item["name"], content)

@app.get("/cocktails/{cocktail_id}")
def get_cocktail(cocktail_id: int):

    logger.info(
        f"[API] Retrieving cocktail (ID {cocktail_id})"
    )

    response = table.get_item(
        Key={
            "id": cocktail_id
        }
    )

    item = response.get("Item")

    if not item:
        logger.warning(f"Cocktail {cocktail_id} not found")
        raise HTTPException(
            status_code=404,
            detail="Cocktail not found"
        )
    
    logger.info(
        f"[API] Served cocktail '{item['name']}' (ID {cocktail_id})"
    )

    return item

@app.post("/cocktails")
def create_cocktail(cocktail: Cocktail):

    logger.info(
        f"[API] Creating cocktail '{cocktail.name}' (ID {cocktail.id})"
    )

    table.put_item(
        Item={
            "id": cocktail.id,
            "name": cocktail.name,
            "spirit": cocktail.spirit,
            "ingredients": cocktail.ingredients
        }
    )

    logger.info(
        f"[API] Created cocktail '{cocktail.name}'"
    )

    return {
        "message": "Cocktail added successfully"
    }

@app.delete("/cocktails/{cocktail_id}")
def delete_cocktail(cocktail_id: int):

    logger.info(
        f"[API] Deleting cocktail ID {cocktail_id}"
    )

    response = table.get_item(
        Key={"id": cocktail_id}
    )

    item = response.get("Item")

    if not item:
        logger.warning(
            f"[API] Delete failed - cocktail ID {cocktail_id} not found"
        )
        raise HTTPException(
            status_code=404,
            detail="Cocktail not found"
        )

    table.delete_item(
        Key={"id": cocktail_id}
    )

    logger.info(
        f"[API] Deleted cocktail '{item['name']}'"
    )

    return {
        "message": f"Cocktail {cocktail_id} deleted"
    }

@app.put("/cocktails/{cocktail_id}")
def update_cocktail(
    cocktail_id: int,
    cocktail: Cocktail
):

    logger.info(
        f"[API] Updating cocktail ID {cocktail_id}"
    )

    response = table.get_item(
        Key={"id": cocktail_id}
    )

    if "Item" not in response:
        logger.warning(
            f"[API] Update failed - cocktail ID {cocktail_id} not found"
        )
        raise HTTPException(
            status_code=404,
            detail="Cocktail not found"
        )

    updated_cocktail = {
        "id": cocktail_id,
        "name": cocktail.name,
        "spirit": cocktail.spirit,
        "ingredients": cocktail.ingredients
    }

    table.put_item(Item=updated_cocktail)

    logger.info(
        f"[API] Updated cocktail '{cocktail.name}'"
    )

    return updated_cocktail