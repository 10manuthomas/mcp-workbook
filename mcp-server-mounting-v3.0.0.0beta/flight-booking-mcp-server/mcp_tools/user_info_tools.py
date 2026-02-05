from fastmcp.tools import tool


class UserInfoTools:

    @tool(name="GetUserInfo-FlightBookingServer",
          tags={"v1"})
    async def get_user_info_tool(self) -> dict:
        """Returns information about the authenticated Azure user."""
        from fastmcp.server.dependencies import get_access_token

        token = get_access_token()
        print("token:::", token)
        print({
            "client_id": token.client_id,
            "scopes": token.scopes,
            "claims": token.claims,
        })
        return {
            "client_id": token.client_id,
            "scopes": token.scopes,
            "claims": token.claims,
            "server": "Flight Booking Server"
        }
