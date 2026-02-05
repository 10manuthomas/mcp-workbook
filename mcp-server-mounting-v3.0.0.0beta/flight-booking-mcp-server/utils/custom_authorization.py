from typing import Any

import jwt
from fastmcp.server.auth import AuthContext, AccessToken
from fastmcp.server.dependencies import get_http_headers


# def is_authorized(required_role: str) -> Any:
#     """
#     Check if the user has the required role for authorization.
#     :param required_role: user role required for access.
#     :return:
#     """
#
#     def verify_role(ctx: AuthContext) -> bool:
#         """
#         Verify if the user has the required role.
#
#         :param ctx:  ctx (AuthContext): The context containing user information.
#         :return: bool: True if the user has the required role, False otherwise.
#         """
#         if ctx.token is None:
#             return False
#
#         return required_role in ctx.token.claims["roles"]
#     return verify_role


def is_authorized(required_role: str) -> Any:
    """
    Check if the user has the required role for authorization.
    :param required_role: user role required for access.
    :return:
    """
    def verify_role(ctx: AuthContext) -> bool:
        headers = get_http_headers()
        if headers:
            access_token = headers["access_token"]
            claims = jwt.decode(access_token,
                                options={"verify_signature": False}
                                )
            return  required_role in claims.get("roles", [])
        else:
            return False

    return verify_role

