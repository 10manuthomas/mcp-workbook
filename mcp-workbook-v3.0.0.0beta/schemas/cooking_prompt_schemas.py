from typing import Annotated

from pydantic import BaseModel, Field


class CookingPromptUserDataRequest(BaseModel):
    first_name: Annotated[str, Field(description="First Name")]
    country: Annotated[str, Field(description="Country")]