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
    name = [(name)]

    sql_1 = 'SELECT * from shop where name = %s'
    shop_info = sql_data_selectOne(name, sql_1)
    # print(shop_info)

    sql_2 = 'SELECT * from menu where shop = %s'
    tmp = sql_data_selectAll([(shop_info['id'])], sql_2)
    # print(tmp)
    cates = []
    cate = {'category':'', 'dishes': []}
    for x in tmp:
        temp = {
            "name": x['name'],
            "price": x['price'],
            "sale": x['sale'],
            "logo": x['logo'],
            "description": x['description']
        }
        if cate['category'] == x['category']:
            cate['dishes'].append(temp)
        else:
            # print("cate: ", cate)
            if cate['category'] != '':  # 避免为空
                cates.append(cate)
                # print("cates:     ", cates)
                # print("appended:", cate)
            cate = {'category': x['category'], 'dishes': [temp]}
    cates.append(cate)
    # print(cates)

    return {
        "name": shop_info['name'],
        "needytime": shop_info['needytime'],
        "credit": shop_info['credit'],
        "logo": shop_info['logo'],
        "sale": shop_info['sale'],
        "threshold": shop_info['thresholdprice'],
        "deliverprice": shop_info['deliverprice'],
        "categories": cates
    }