import io
from overrides import overrides
from typing import Union

from app.common_interface import OCRInterface


class OCRService:
    def __init__(self, ocr_adapter: OCRInterface):
        self.ocr_adapter = ocr_adapter

    def detect_text(self, file_type, file_path: Union[str, io.BytesIO]) -> dict:
        return self.ocr_adapter.detect_text(file_type, file_path)

    def detect_layout(self, file_type, file_path: Union[str, io.BytesIO]):
        return self.ocr_adapter.detect_layout(file_type, file_path)

