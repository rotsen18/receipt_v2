from typing import Optional

from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str
    description: Optional[str] = None
