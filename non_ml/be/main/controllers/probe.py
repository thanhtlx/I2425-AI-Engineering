from fastapi import APIRouter


router = APIRouter()


@router.get("/pings")
async def ping():
    return {}


@router.get("/ready")
async def is_ready():
    return {}


@router.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
