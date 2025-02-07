# mypy: ignore-errors

from fastapi import APIRouter

from . import probe, transaction, user, merchant, task

router = APIRouter(prefix="/api")

router.include_router(probe.router, tags=["probe"])
router.include_router(transaction.router, tags=["transaction"])
router.include_router(user.router, tags=["user"])
router.include_router(merchant.router, tags=["merchant"])
router.include_router(task.router, tags=["task"])
