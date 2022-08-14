# 引入路由管理
from fastapi import APIRouter, Header
from pydantic import BaseModel
from op.shopOp import selectShopByName
from fastapi.responses import JSONResponse
# 让数据以json的格式返回
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from op.Token_is_True import token_is_true
router = APIRouter()

@router.get('/searchShopByName')
async def searchShopByNameApi(name: str, token: str = Header(None)):
    if not token_is_true(token):
        raise HTTPException(
                status_code=401,
                detail="Incorrect token",
                headers={"WWW-Authenticate": "Bearer"},
            ) 
    data = selectShopByName(name)
    return JSONResponse(data)