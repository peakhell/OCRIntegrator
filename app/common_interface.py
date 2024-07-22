import io
from abc import ABC, abstractmethod
from typing import Union


class OCRInterface(ABC):
    """
    统一接口定义，不同开源OCR输入输出不同，需要进行统一的功能模块定义。
    表格识别与布局识别依赖于OCR检测结果，定义一个类即可。
    """

    @abstractmethod
    def detect_text(self, file_type, file: Union[str, io.BytesIO], **kwargs) -> dict:
        pass

    @abstractmethod
    def detect_layout(self, file_type: str, file: Union[str, io.BytesIO], **kwargs) -> list[dict]:
        """
        布局检测，输出格式如下：
        [{
            'type': 'header',              //类型
            'score': 0.7845141887664795,   //置信度
            'x0': 89.322998046875,       //左边界
            'x1': 239.1925048828125,     //右边界
            'top': 117.3193359375,       //上边界
            'bottom': 129.7491455078125, //下边界
            'page_number': 0,            //页码
            'visited': True              //是否可见
        },
        {
            'type': 'title',
            'score': 0.9028056859970093,
            'x0': 135.99578857421875,
            'x1': 478.801513671875,
            'top': 76.20449829101562,
            'bottom': 99.8682352701823,
            'page_number': 0,
            'visited': True
        }]
        类型是页面当中含有的多种类型，如标题、文本、表格等等。是一个枚举值，目前支持以下几种
        "_background_"
        "Text",          // 文本
        "Title",         // 标题
        "Figure",        // 配图
        "Figure caption", //配图标题
        "Table",          //表格
        "Table caption",  //表格标题
        "Header",         //页头
        "Footer",         //页尾
        "Reference",      //参考引用
        "Equation",       //公式
        """
        pass
