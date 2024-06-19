# OCRIntegrator-
封装开源的OCR模型，表格检测，布局识别等能力，以接口方式提供服务。 目前只集成了deepdoc，看过源码，实际上模型是基于百度paddle平台训练的。后续会提供更多的服务集成

## Introduce
1. deepdoc中使用pdfplumber读取文本，同时使用OCR识别文字，优先取pdfplumber中的文本，扫描件则完全使用OCR识别的文本。
## Install
1. 使用poetry安装依赖
`poetry install `
2. 项目运行
`uvicorn main:app`
