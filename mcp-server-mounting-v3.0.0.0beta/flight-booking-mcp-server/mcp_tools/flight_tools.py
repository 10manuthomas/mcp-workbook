from fastmcp import Context
from fastmcp.tools import tool

from schemas.flight_tool_schemas import FlightSuggestionRequest, LayoverIdeaRequest


class FlightTools:

    @tool(
        name="FlightSuggestions",
        tags={"v1"}
    )
    async def get_flight_suggestions_tool(self, flight_suggestion_request: FlightSuggestionRequest,
                                          ctx: Context) -> str:
        """Generate Flight suggestions with the provided content."""
        result = await ctx.elicit("Hey, To complete this operation,"
                                  " I will need to use external API .. Do you Approve this action?",
                                  response_type=None)
        if result.action == "accept":
            print("Accepted")
        elif result.action == "decline":
            print("Rejected")
            raise ValueError("Action decline")
        elif result.action == "cancel":
            print("User canceled the operation")
            # raise ValueError("Action cancel")
        return (f"Oh So you can fly from {flight_suggestion_request.origin} to {flight_suggestion_request.destination} "
                f"on {flight_suggestion_request.departure_date} with BlueSkies Airlines, Qatar Airways and Japan Airways !!!")

    @tool(
        name="LayoverIdeas",
        tags={"v1"}
    )
    async def get_layover_ideas_tool(self, layover_idea_request: LayoverIdeaRequest,
                                     ctx: Context) -> str:
        """Get Layover ideas with the provided content, to make the most of your layover."""
        result = await ctx.elicit("Hey, To complete this operation,"
                                  " I will need to use your LLM .. Do you Approve this action?",
                                  response_type=None)
        if result.action == "accept":
            print("Accepted")
        elif result.action == "decline":
            print("Rejected")
            raise ValueError("Action decline")
        elif result.action == "cancel":
            print("User canceled the operation")
            # raise ValueError("Action cancel")

        result = await ctx.sample(f"Please generate a layover suggestion suggestion for a flight from from "
                                  f"{layover_idea_request.origin} "
                                  f"to {layover_idea_request.destination} "
                                  f"on {layover_idea_request.departure_date}")
        return f"Here is your amazing layover idea, this will help you make the most of your travel :: {result.text}"
