from fastapi import APIRouter, Depends, Header
from op.Token_is_True import token_is_true

router = APIRouter()
# 测试代码
@router.post("/tokenCheck")
async def test(*, token: str = Header(None)):
	"""测试代码"""
	return {
        "code":1,
        "msg":"success"
        } if token_is_true(token) else None