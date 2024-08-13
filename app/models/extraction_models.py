from pydantic import BaseModel
from typing import List, Optional
from datetime import timedelta

class ExtractedContent(BaseModel):
    text: str
    page_number: Optional[int] = None


class ExtractionResponse(BaseModel):
    filename: str
    file_type: str
    extraction_time: timedelta
    word_count: int
    content: List[ExtractedContent]