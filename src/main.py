from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi import HTTPException
import boto3

app = FastAPI()

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
            <a href="/cocktails/{cocktail['id']}">
                {cocktail['name']}
            </a>
        </li>
        """
    return f"""
    <html>
    <head>
        <title>Tom's Cocktail API</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: auto;
                padding: 40px;
                background-color: #f5f5f5;
            }}

            .card {{
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #8B0000;
            }}

            a {{
                text-decoration: none;
                color: #0066cc;
            }}

            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🍸 Tom's Cocktail API</h1>

            <p>
                A simple REST API built with Python and FastAPI.
            </p>
            <p>
                Currently serving {cocktail_count} cocktails.
            </p>
            <h2>Available Cocktails</h2>
            <ul>
                {cocktail_list}
            </ul>
            <h2>Useful Links</h2>

            <ul>
                <li><a href="/cocktails">View All Cocktails (JSON)</a></li>
                <li><a href="/docs">Swagger Documentation</a></li>
            </ul>

            <p>
                Running locally on FastAPI 🚀
            </p>
        </div>
    </body>
    </html>
    """

@app.get("/cocktails")
def get_cocktails():

    response = table.scan()

    return response["Items"]

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