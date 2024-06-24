import io
from typing import Union
from app.common_interface import OCRInterface
from app.deepdoc.parser import PdfParser
from app.deepdoc.parser import ImageParser


class DeepdocOCRAdapter(OCRInterface):

    def __init__(self):
        self.pdf_parser = PdfParser()
        self.image_parser = ImageParser()

    def detect_text(self, file_type: str, file_path: Union[str, io.BytesIO]) -> dict:
        if file_type == 'pdf':
            return self.pdf_parser.__images__(file_path)
        elif file_type == 'jpg' or file_type == 'png' or file_type == 'jpeg':
            return self.image_parser.__images__(file_path)
        else:
            raise NotImplementedError('Only support pdf file type')

    def detect_layout(self, file_type: str, file_path: Union[str, io.BytesIO]) -> list[dict]:
        if file_type == 'pdf':
            return self.pdf_parser.__call__(file_path)
        elif file_type == 'jpg' or file_type == 'png' or file_type == 'jpeg':
            return self.image_parser.__call__(file_path)
        else:
            raise NotImplementedError('Only support pdf file type')

