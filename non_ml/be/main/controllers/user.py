from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from main._db import get_db_session
from main.libs import user_lib

from main.schemas.user.user import AllUserResponse, UserDetail

router: APIRouter = APIRouter()


@router.get("/users", response_model=AllUserResponse)
async def get_users(
    session: AsyncSession = Depends(get_db_session),
    # _=Depends(get_principal),
    page: int = Query(1, ge=1),
    per_page: int = Query(1000, ge=1),
    # params: TransactionQueryParams = Depends(),
):
    users: AllUserResponse = await user_lib.get_users(
        session=session, per_page=per_page, page=page
    )
    return users


@router.get("/users/{user_id}", response_model=UserDetail)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    # _=Depends(get_principal),
):
    user = await user_lib.get_user_details(session=session, user_id=user_id)
    return user
