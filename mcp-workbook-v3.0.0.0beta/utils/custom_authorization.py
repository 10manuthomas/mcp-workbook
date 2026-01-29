from typing import Any

from fastmcp.server.auth import AuthContext


def is_authorized(required_role: str) -> Any:
    """
    Check if the user has the required role for authorization.
    :param required_role: user role required for access.
    :return:
    """

    def verify_role(ctx: AuthContext) -> bool:
        """
        Verify if the user has the required role.

        :param ctx:  ctx (AuthContext): The context containing user information.
        :return: bool: True if the user has the required role, False otherwise.
        """
        if ctx.token is None:
            return False
        return required_role in ctx.token.claims["roles"]

    return verify_role
