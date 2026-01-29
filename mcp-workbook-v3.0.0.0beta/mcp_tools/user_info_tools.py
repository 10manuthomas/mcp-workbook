from fastmcp.tools import tool


class UserInfoTools:

    @tool(name="GetUserInfo",
          tags={"v1"})
    async def get_user_info_tool(self) -> dict:
        """Returns information about the authenticated Azure user."""
        from fastmcp.server.dependencies import get_access_token

        token = get_access_token()

        return {
            "azure_id": token.claims.get("sub"),
            "email": token.claims.get("email"),
            "name": token.claims.get("name"),
            "job_title": token.claims.get("job_title"),
            "office_location": token.claims.get("office_location")
        }
