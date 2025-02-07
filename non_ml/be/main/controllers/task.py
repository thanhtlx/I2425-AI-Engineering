from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from main._db import get_db_session
from main.libs import task_lib
from main.schemas.task import StatusProgress

router: APIRouter = APIRouter()


@router.get("/latest-export-task", response_model=StatusProgress)
async def get_latest_task_status(
    session: AsyncSession = Depends(get_db_session),
    # _=Depends(get_principal),
):

    return await task_lib.get_latest_task_status(session=session)
