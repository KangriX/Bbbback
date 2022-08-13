# 容器
import uvicorn
# FASTAPI模板
from fastapi import FastAPI
# 注册相应的api
from api import Customer_Login
from api import Customer_Register
from api import Token_Check
from api import Change_Password
from api import getAllGoodsByName
from api import searchShopByName
from api import getAllShopInfo
# 配置跨域
from starlette.middleware.cors import CORSMiddleware
# 返回json格式的数据
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


# 声明fastapi的实例
app = FastAPI()
# 跨域配置
# 配置允许域名
origins = [
    "https://v3710z5658.oicp.vip"
]

# origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# 注册api模块
app.include_router(Customer_Login.router, prefix="/customer")
app.include_router(Customer_Register.router, prefix="/customer")
app.include_router(Token_Check.router, prefix="/customer")
app.include_router(Change_Password.router, prefix="/customer")
app.include_router(getAllGoodsByName.router, prefix="/shop")
app.include_router(searchShopByName.router,prefix="/shop")
app.include_router(getAllShopInfo.router, prefix="/shop")


# 配置容器启动相应的实例
if __name__ == '__main__':
    uvicorn.run(app='main:app', port=8000, reload=True)

# if __name__ == '__main__':
    # uvicorn.run(app='main:app', reload=True)
