from typing import Annotated

from pydantic import BaseModel, Field


class TimeConversionRequest(BaseModel):
    from_timezone: Annotated[str, Field(description="From timezone unit the conversion needs to get initiated")]
    to_timezone: Annotated[str, Field(description="To timezone Unit or the destination unit")]
    time: Annotated[float, Field(description="Time")]


class TimeConversionResponse(BaseModel):
    converted_value: Annotated[float, Field(description="Converted value")]
    input: Annotated[TimeConversionRequest, Field(description="Input TimeConversionRequest")]
