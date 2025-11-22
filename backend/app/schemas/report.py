from pydantic import BaseModel

class ReportRead(BaseModel):
    id: int
    filename: str
    path: str
    class Config:
        from_attributes = True

