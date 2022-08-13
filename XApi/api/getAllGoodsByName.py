from fastapi import APIRouter, Header, Depends, HTTPException
from pydantic import BaseModel
from op.database_op import sql_data_selectAll, sql_data_selectOne
from op.Token_is_True import token_is_true
import pymysql

router = APIRouter()

@router.get("/getAllGoodsByName")
async def getAllGoodsByName(name: str, token: str = Header(None)):
    # 验证token
    if not token_is_true(token):
        raise HTTPException(
                status_code=401,
                detail="Incorrect token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    # 连接数据库
    # print(type(name))
    conn = pymysql.connect(
        host='124.222.244.117',
        port=3306,
        user='zrgj8',
        password='zrgj8',
        database='zrgj8',
        charset='utf8'
        )
    name = [(name)]

    sql_1 = 'select * from shop where name=%s'
    shop_info = sql_data_selectOne(conn, name, sql_1)
    # print(shop_info)

    # 重连数据库
    conn = pymysql.connect(
        host='124.222.244.117',
        port=3306,
        user='zrgj8',
        password='zrgj8',
        database='zrgj8',
        charset='utf8'
        )

    sql_2 = 'select * from menu where shop=%s'
    tmp = sql_data_selectAll(conn, [(shop_info[0])], sql_2)

    result = []
    for x in tmp:
        temp = {
            "name": x[2],
            "price": x[3],
            "sale": x[4],
            "logo": x[5],
            "description": x[6],
            "category": x[7]
        }
        result.append(temp)

    return {
        "name": shop_info[1],
        "needytime": shop_info[6],
        "credit": shop_info[5],
        "logo": shop_info[8],
        "sale": shop_info[7],
        "threshold": shop_info[-1],
        "goods": result
    }