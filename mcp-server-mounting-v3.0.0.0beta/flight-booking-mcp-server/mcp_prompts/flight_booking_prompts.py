from fastmcp import Context
from fastmcp.prompts import prompt

from schemas.flight_booking_prompt_schemas import FlightBookingIdeaPromptRequest


class FlightBookingPrompts:

    @prompt(name="FlightBookingIdeas", tags={"v1"})
    async def get_flight_booking_idea_prompt(self, user_name: str, ctx: Context) -> str:
        """Prompt to get flight booking ideas after collecting user information."""

        # self.serialize_ctx("pycharm")

        result = await ctx.elicit(f"Hi {user_name}... Well I will need your travel details to proceed, "
                                  f"do you approve this operation ?",
                                  response_type=None)

        if result.action == "accept":
            pass
        else:
            raise ValueError("Action rejected")

        """Collect user information through interactive prompts."""
        result = await ctx.elicit(
            message="Please provide your information",
            response_type=FlightBookingIdeaPromptRequest
        )

        if result.action == "accept":
            user_data = result.data
            return (f"I am travelling from {user_data.origin} "
                    f"to {user_data.destination} on {user_data.departure_date} with {user_data.number_of_passengers} number of people,"
                    f" prepare amazing flight booking idea for me !!!")
        elif result.action == "decline":
            return "Information not provided"
        else:  # cancel
            return "Operation cancelled"
