from typing import List, Annotated

from pydantic import BaseModel, Field


class RecipeSuggestionRequest(BaseModel):
    ingredients: Annotated[List[str], Field(description="Ingredients list")]
