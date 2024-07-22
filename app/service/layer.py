import io
from typing import Union

from app.common_interface import OCRInterface


class OCRService:
    def __init__(self, ocr_adapter: OCRInterface):
        self.ocr_adapter = ocr_adapter

    def detect_text(self, file_type, file: Union[str, io.BytesIO], **kwargs) -> dict:
        return self.ocr_adapter.detect_text(file_type, file, **kwargs)

    def detect_layout(self, file_type, file: Union[str, io.BytesIO], **kwargs):
        return self.ocr_adapter.detect_layout(file_type, file, **kwargs)

