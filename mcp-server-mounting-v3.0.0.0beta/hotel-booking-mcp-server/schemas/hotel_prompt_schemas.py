from typing import Annotated

from pydantic import BaseModel, Field


class HotelBookingIdeaPromptRequest(BaseModel):
    place_of_visit: Annotated[str, Field(description="Destination Location")]
    from_date: Annotated[str, Field(description="Stay Start Date in YYYY-MM-DD format")]
    to_date: Annotated[str, Field(description="Stay Till Date in YYYY-MM-DD format")]
    number_of_people: Annotated[int, Field(description="Number of people staying")]
