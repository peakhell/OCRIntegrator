import os
from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional


class SupportFileType(str, Enum):
    jpg = "jpg"
    pdf = "pdf"
    png = "png"
    jpeg = "jpeg"
    bmp = "bmp"
    tiff = "tiff"
    tif = "tif"
    image = "image"


class OcrPathModel(BaseModel):
    file_path: str = Field(description="文件路径")
    file_type: SupportFileType
    zoomin: Optional[int] = None

    @validator('file_path')
    def check_file_path_exists(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"File path does not exist: {v}")
        return v


class OcrFileModel(BaseModel):
    file_type: SupportFileType
    zoomin: Optional[int] = None
