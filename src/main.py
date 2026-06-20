from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class Cocktail(BaseModel):
    id: int
    name: str
    spirit: str
    ingredients: list[str]

cocktails =    [
        {
            "id": 1,
            "name": "Old Fashioned",
            "spirit": "Bourbon",
            "ingredients": [
                "60ml Bourbon",
                "1 Sugar Cube",
                "2 Dashes Angostura Bitters"
            ]
        },
        {
            "id": 2,
            "name": "Negroni",
            "spirit": "Gin",
            "ingredients": [
                "30ml Gin",
                "30ml Campari",
                "30ml Sweet Vermouth"
            ]
        },
        {
            "id": 3,
            "name": "Margarita",
            "spirit": "Tequila",
            "ingredients": [
                "50ml Tequila",
                "25ml Triple Sec",
                "25ml Lime Juice"
            ]
        }
    ]

@app.get("/", response_class=HTMLResponse)
def root():
    cocktail_count = len(cocktails)
    return f"""
    <html>
    <head>
        <title>Tom's Cocktail API</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
            }}

            h1 {{
                color: #8B0000;
            }}

            .card {{
                background: white;
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
            <h2>Available Endpoints</h2>

            <ul>
                <li><a href="/cocktails">GET /cocktails</a></li>
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
    return cocktails

@app.get("/cocktails/{cocktail_id}")
def get_cocktail(cocktail_id: int):

    for cocktail in cocktails:
        if cocktail["id"] == cocktail_id:
            return cocktail

    return {"error": "Cocktail not found"}

@app.post("/cocktails")
def create_cocktail(cocktail: Cocktail):

    cocktails.append(cocktail.dict())

    return {
        "message": "Cocktail added successfully",
        "cocktail": cocktail
    }