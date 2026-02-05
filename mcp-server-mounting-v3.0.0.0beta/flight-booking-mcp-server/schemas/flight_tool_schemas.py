from typing import Annotated

from pydantic import BaseModel, Field


class FlightSuggestionRequest(BaseModel):
    origin: Annotated[str, Field(description="Origin Location")]
    destination: Annotated[str, Field(description="Destination Location")]
    departure_date: Annotated[str, Field(description="Departure Date in YYYY-MM-DD format")]
    number_of_passengers: Annotated[int, Field(description="Number of Passengers")]


class LayoverIdeaRequest(BaseModel):
    origin: Annotated[str, Field(description="Origin Location")]
    destination: Annotated[str, Field(description="Destination Location")]
    departure_date: Annotated[str, Field(description="Departure Date in YYYY-MM-DD format")]
