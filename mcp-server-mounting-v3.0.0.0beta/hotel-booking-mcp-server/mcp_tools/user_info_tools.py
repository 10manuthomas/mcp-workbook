from fastmcp.server.dependencies import get_http_headers
from fastmcp.tools import tool


class UserInfoTools:

    @tool(name="GetUserInfo-HotelBookingServer",
          tags={"v1"})
    async def get_user_info_tool(self) -> dict:
        """Returns information about the authenticated Azure user."""
        from fastmcp.server.dependencies import get_access_token

        token = get_access_token()
        print("token:::", token)
        # print({
        #     "client_id": token.client_id,
        #     "scopes": token.scopes,
        #     "claims": token.claims,
        # })
        headers = get_http_headers()
        print("headers::", headers)

        return {
            "client_id": token.client_id,
            "scopes": token.scopes,
            "claims": token.claims,
            "http_headers": headers,
            "server": "Hotel Booking Server"
        }
