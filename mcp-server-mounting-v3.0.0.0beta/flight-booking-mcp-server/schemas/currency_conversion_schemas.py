from typing import Annotated

from pydantic import BaseModel, Field


class CurrencyConversionRequest(BaseModel):
    from_currency: Annotated[str, Field(description="From currency unit the conversion needs to get initiated")]
    to_currency: Annotated[str, Field(description="To currency Unit or the destination unit")]
    amount: Annotated[float, Field(description="Amount of currency")]


class CurrencyConversionResponse(BaseModel):
    converted_value: Annotated[float, Field(description="Converted value")]
    input: Annotated[CurrencyConversionRequest, Field(description="Input CurrencyConversionRequest")]
