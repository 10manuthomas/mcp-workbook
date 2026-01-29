from typing import Annotated

from pydantic import BaseModel, Field


class UnitConversionRequest(BaseModel):
    from_unit: Annotated[str, Field(description="From unit the conversion needs to get initiated")]
    to_unit: Annotated[str, Field(description="To Unit or the destination unit")]
    quantity: Annotated[float, Field(description="Quantity of unit")]


class UnitConversionResponse(BaseModel):
    converted_value: Annotated[float, Field(description="Converted value")]
    input: Annotated[UnitConversionRequest, Field(description="Input UnitConversionRequest")]