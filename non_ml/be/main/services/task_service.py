from sqlalchemy.ext.asyncio import AsyncSession


from sqlalchemy import select
from main.models.export_task import ExportedTaskModel


async def get_latest_task(session: AsyncSession) -> ExportedTaskModel | None:
    stmt = (
        select(ExportedTaskModel).order_by(ExportedTaskModel.created_at.desc()).limit(1)
    )
    stmt = stmt.where(ExportedTaskModel.is_deleted.is_(False))
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_task(session: AsyncSession, data: dict) -> ExportedTaskModel:
    task = ExportedTaskModel(**data)
    session.add(task)
    await session.commit()
    return task
