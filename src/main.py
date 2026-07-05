from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
import boto3

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

@app.get("/", response_class=HTMLResponse)
def root():

    response = table.scan()
    cocktails = response["Items"]
    cocktail_count = len(cocktails)

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

    response = table.scan()

    return response["Items"]

@app.get("/cocktails/html", response_class=HTMLResponse)
def cocktails_html():

    response = table.scan()

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

    response = table.get_item(
        Key={"id": cocktail_id}
    )

    item = response.get("Item")

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Cocktail not found"
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

    response = table.get_item(
        Key={
            "id": cocktail_id
        }
    )

    item = response.get("Item")

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Cocktail not found"
        )

    return item

@app.post("/cocktails")
def create_cocktail(cocktail: Cocktail):

    table.put_item(
        Item={
            "id": cocktail.id,
            "name": cocktail.name,
            "spirit": cocktail.spirit,
            "ingredients": cocktail.ingredients
        }
    )

    return {
        "message": "Cocktail added successfully"
    }

@app.delete("/cocktails/{cocktail_id}")
def delete_cocktail(cocktail_id: int):

    response = table.get_item(
        Key={"id": cocktail_id}
    )

    item = response.get("Item")

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Cocktail not found"
        )

    table.delete_item(
        Key={"id": cocktail_id}
    )

    return {
        "message": f"Cocktail {cocktail_id} deleted"
    }

@app.put("/cocktails/{cocktail_id}")
def update_cocktail(
    cocktail_id: int,
    cocktail: Cocktail
):

    response = table.get_item(
        Key={"id": cocktail_id}
    )

    if "Item" not in response:
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

    return updated_cocktail