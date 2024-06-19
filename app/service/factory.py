from app.service.layer import OCRService
from app.adapter.deepdoc_adapter import DeepdocOCRAdapter


class ServiceFactory:
    @staticmethod
    def get_ocr_service(ocr_type: str) -> OCRService:
        if ocr_type == "deepdoc":
            return OCRService(DeepdocOCRAdapter())
        else:
            raise ValueError(f"Unsupported OCR type: {ocr_type}")
