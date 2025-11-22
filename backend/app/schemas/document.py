from pydantic import BaseModel

class DocumentRead(BaseModel):
    id: int
    filename: str
    path: str
    mime_type: str | None = None
    ocr_text: str | None = None
    ocr_confidence: float | None = None
    class Config:
        from_attributes = True
