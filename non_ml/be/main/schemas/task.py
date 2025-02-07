from pydantic import BaseModel


class StatusProgress(BaseModel):
    status: str
    progress: float
