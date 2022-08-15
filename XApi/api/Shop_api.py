from fastapi import APIRouter, Header, Depends, HTTPException
from pydantic import BaseModel
from op.database_op import sql_data_selectAll, sql_data_selectOne
from op.Token_is_True import token_is_true
import pymysql
from op.shopOp import selectShopByName
from fastapi.responses import JSONResponse

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

@router.get("/getAllShopInfo")
async def getAllShopInfo(*, token: str = Header(None)):
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
    cursor=conn.cursor()
    sql = 'select name,credit,sale,needytime,distance,logo,thresholdprice,id from shop;'
    res=None
    lis=['name','credit','sale','needytime','distance','logo','thresholdprice','id']
    try:
        cursor.execute(sql)
        res=cursor.fetchall()
        # print("finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 关闭连接
    cursor.close()
    conn.close()
    eli=[]
    for i in res:
        dic={}
        for x in range(8):
            dic[lis[x]]=i[x]
        eli.append(dic)
    return eli

@router.get('/searchShopByName')
async def searchShopByNameApi(name: str, token: str = Header(None)):
    if not token_is_true(token):
        raise HTTPException(
                status_code=401,
                detail="Incorrect token",
                headers={"WWW-Authenticate": "Bearer"},
            ) 
    data = selectShopByName(name)
    # print("data = ", data)
    return JSONResponse(data)