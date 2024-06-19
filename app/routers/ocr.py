import os
import io
from app.service.factory import ServiceFactory
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.ocr import OcrFileModel, OcrPathModel
from pydantic import ValidationError

service_type = os.getenv("SERVICE_TYPE", "deepdoc")
ocr_service = ServiceFactory.get_ocr_service(service_type)

router = APIRouter()


@router.post("/ocr/path")
async def detect_ocr_by_path(item: OcrPathModel):
    file_type = item.file_type
    file_path = item.file_path
    result = ocr_service.detect_text(file_type, file_path)
    return {"result": result}


@router.post("/ocr/file")
async def detect_ocr_by_file(file: UploadFile = File(...), file_type: str = Form(...)):
    try:
        OcrFileModel(file_type=file_type)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    file_io = io.BytesIO(await file.read())
    result = ocr_service.detect_text(file_type, file_io)
    return result


@router.post("/layout/path")
async def detect_layout_by_path(item: OcrPathModel):
    file_type = item.file_type
    file_path = item.file_path
    result = ocr_service.detect_layout(file_type, file_path)
    return {"result": result}


@router.post("/layout/file")
async def detect_layout_by_file(file: UploadFile = File(...), file_type: str = Form(...)):
    try:
        OcrFileModel(file_type=file_type)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    file_io = io.BytesIO(await file.read())
    result = ocr_service.detect_layout(file_type, file_io)
    return result
