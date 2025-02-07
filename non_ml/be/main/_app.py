from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.triggers.cron import CronTrigger

from .libs.cron_libs import cron_transaction_lib


import sentry_sdk
from ._config import config
from .commons.middlewares import AccessLogMiddleware, DBSessionMiddleware

api_docs_enabled = config.ENVIRONMENT in ["local", "dev"]

# Sentry
sentry_sdk.init(
    dsn=config.SENTRY_DSN,
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=config.SENTRY_SAMPLE_RATE,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)

# Cron scheduler
scheduler = AsyncIOScheduler()
trigger = CronTrigger(hour=0, minute=0)
# trigger = CronTrigger(minute='*')
scheduler.add_job(
    cron_transaction_lib.update_fraud_prediction_transactions,
    trigger=trigger,
    kwargs={"ml_model_path": config.ML_MODEL_PATH},
)
scheduler.start()

# App init
app = FastAPI(
    redoc_url=None,
    docs_url="/docs" if api_docs_enabled else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(DBSessionMiddleware)
app.add_middleware(AccessLogMiddleware)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()
