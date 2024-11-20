from fastapi import FastAPI

from script import init as init_script
from router import handlers
import uvicorn
import json

# 初始化app
app = FastAPI(
    title="API 文档标题",
    description="接口的详细描述",
    version="1.0.0"
)

app.include_router(handlers.router)

# 导出 OpenAPI JSON 文件
@app.on_event("startup")
async def export_openapi():
    openapi_data = app.openapi()  # 获取 OpenAPI JSON 数据
    with open("openapi.json", "w", encoding="utf-8") as f:
        json.dump(openapi_data, f, ensure_ascii=False, indent=4)
    print("OpenAPI 文档已导出为 openapi.json")

if __name__ == "__main__":
    init_script.init("./script/data.xlsx")
    uvicorn.run(app, host="0.0.0.0", port=5000)
