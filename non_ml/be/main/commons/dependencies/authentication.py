import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from main import config
from main._db import get_db_session
from main.misc.exceptions import Forbidden, ErrorCode
from main.schemas.user.principal import Principal

jwt_header = HTTPBearer(auto_error=False)


async def get_principal(
    creds: HTTPAuthorizationCredentials = Depends(jwt_header),
    session: AsyncSession = Depends(get_db_session),
    roles: list[str] | None = None,
) -> Principal:
    credentials_exception = Forbidden(
        error_message="Invalid credentials",
        error_code=ErrorCode.FORBIDDEN,
    )

    if creds is None:
        raise credentials_exception

    token = creds.credentials
    try:
        data = jwt.decode(
            jwt=token,
            key=config.SECRET_KEY,
            algorithms=config.ALGORITHM,
            options={"verify_signature": True},
        )
    except jwt.DecodeError:
        raise credentials_exception

    # account = await user_service.get_user(session=session, user_id=int(data["uid"]))
    # if account is None:
    #     raise credentials_exception

    # account_roles = await account_service.get_account_roles_by_id(session=session, id=user.id)
    # role_names = [role.name for role in account_roles]
    #
    # if roles and not (set(role_names) & set(roles)):
    #     raise credentials_exception

    # return Principal(account)
