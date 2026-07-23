from pydantic import BaseModel


class Cocktail(BaseModel):
    id: int
    name: str
    spirit: str
    ingredients: list[str]
