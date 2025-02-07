from sqlalchemy.ext.asyncio import AsyncSession

from main.schemas.task import StatusProgress
from main.services import task_service


async def get_latest_task_status(session: AsyncSession):
    latest_task = await task_service.get_latest_task(session=session)
    return StatusProgress(
        status=latest_task.status, progress=latest_task.meta_data["progress"]
    )
