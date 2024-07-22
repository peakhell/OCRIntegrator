import io
import time
from app.config.logger import logger
from typing import Union
from app.common_interface import OCRInterface
from app.deepdoc.parser import PdfParser
from app.deepdoc.parser import ImageParser
from app.constants import OCR_BATCH_SIZE


class DeepdocOCRAdapter(OCRInterface):

    def __init__(self):
        self.pdf_parser = PdfParser()
        self.image_parser = ImageParser()

    def detect_text(self, file_type: str, file_path: Union[str, io.BytesIO], **kwargs) -> dict:
        start = time.time()
        if file_type == 'pdf':
            zoomin = kwargs.get("zoomin", 3)
            start_idx = 0
            has_next = True
            result = []
            while has_next:
                has_next, data = self.pdf_parser.ocr_detect(file_path, page_from=start_idx, zoomin=zoomin,
                                                            page_to=start_idx + OCR_BATCH_SIZE)
                start_idx += OCR_BATCH_SIZE
                result.extend(data)
            logger.info(f"{file_path}处理完成, 耗时: {time.time() - start :.4f}s")
            return result
        elif file_type in ('jpg', "png", "jpeg", "tif", "tiff", "bmp", "image"):
            result = self.image_parser.__images__(file_path)
            logger.info(f"{file_path}处理完成, 耗时: {time.time() - start :.4f}s")
            return result
        else:
            raise NotImplementedError(f'{file_type} not supported yet')

    def detect_layout(self, file_type: str, file_path: Union[str, io.BytesIO], **kwargs) -> list[dict]:
        start = time.time()
        if file_type == 'pdf':
            zoomin = kwargs.get("zoomin", 3)
            start_idx = 0
            has_next = True
            result = {
                "boxes": [],
                "tables": [],
                "page_cum_height": []
            }
            while has_next:
                has_next, data = self.pdf_parser.__call__(file_path, page_from=start_idx, zoomin=zoomin,
                                                          page_to=start_idx + OCR_BATCH_SIZE)
                start_idx += OCR_BATCH_SIZE
                result["boxes"].extend(data["boxes"])
                result["tables"].extend(data["tables"])
                result["page_cum_height"].extend(data["page_cum_height"])
            # return self.pdf_parser.__call__(file_path)
            logger.info(f"{file_path}处理完成, 耗时: {time.time() - start :.4f}s")
            return result
        elif file_type in ('jpg', "png", "jpeg", "tif", "tiff", "bmp", "image"):
            result = self.image_parser.__call__(file_path)
            logger.info(f"{file_path}处理完成, 耗时: {time.time() - start :.4f}s")
            return result
        else:
            raise NotImplementedError(f'{file_type} not supported yet')
