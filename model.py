from pydantic import BaseModel
from datetime import datetime
class Task(BaseModel):
    id : int
    task: str
    due: datetime

