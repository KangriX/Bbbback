# 引入路由管理
from op import Token_Decode
from unicodedata import name
from fastapi import APIRouter,Header,HTTPException
from pydantic import BaseModel
# from op import personOp
import pymysql
from op.Token_is_True import token_is_true
import jwt
import time

# 构建api路由
router = APIRouter()
# 连接数据库

@router.get("/deleteAllShoppingCart")
async def deleteAllShoppingCart(name: str, token: str = Header(None)):
    if not token_is_true(token):
        raise HTTPException(
                status_code=401,
                detail="Incorrect token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    conn = pymysql.connect(
        host='124.222.244.117',
        port=3306,
        user='zrgj8',
        password='zrgj8',
        database='zrgj8',
        charset='utf8'
    )
    info=Token_Decode.token_decode(token)
    account=info['data']['account']
    # 获取一个光标
    cursor = conn.cursor()
    # 定义将要执行的SQL语句
    sql = "DELETE from cart where shopid=(select id from shop where name=%s and customerid=(select id from customer where account=%s));"
    # 拼接并执行SQL语句
    try:
        cursor.execute(sql, [name,account])
        print('delete successfully')
    except:
        print('fail to delete')
    # 涉及写操作注意要提交
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()
    return True