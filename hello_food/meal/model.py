from typing import TypedDict


class Meal(TypedDict):
    id: int
    cuisine: str
    recipe: str
    price: float
