from fastapi import APIRouter, Header, Depends, HTTPException
from pydantic import BaseModel
from op.database_op import sql_data_selectAll, sql_data_selectOne, sql_data_selectOne1
from op.Token_is_True import token_is_true
from op.Token_Decode import token_decode
from op.database_op import sql_data_selectAll
import pymysql
import datetime

router = APIRouter()

@router.get('/getAllOrdersInfo')
async def getAllOrdersInfo(token: str = Header(None)):
    if not token_is_true(token):
        raise HTTPException(
                status_code=401,
                detail="Incorrect token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    payload = token_decode(token)
    account = payload['data']['account']
    account = [(account)]
    sql_1 = 'select * from customer where account=%s'
    customerid = sql_data_selectOne(account, sql_1)['id']
    sql_2 = 'select * from orders where customerid=%s'
    orders = sql_data_selectAll(customerid, sql_2)
    result=[]
    for order in orders:
        goods=[]
        orderid = order['id']
        sql_3 = 'select * from history where orderid=%s' # bug
        histories = sql_data_selectAll(orderid, sql_3)
        for history in histories:
            menuid = history['menuid']
            sql_4 = 'select * from menu where id=%s'
            menu = sql_data_selectOne(menuid, sql_4)
            good={
                "name": menu['name'],
                "count":history['count'],
                "price": menu['price'],
                "sale": menu['sale'],
                "logo": menu['logo'],
                "description": menu['description'],
                "category": menu['category']
            }
            goods.append(good)
        shopid = order['shopid']
        sql_5 = "select * from shop where id=%s"
        shop = sql_data_selectOne(shopid, sql_5)
        delivered = True
        dt_str = str(order['paytime'])
        paytime = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        nowtime=datetime.datetime.now()
        nowtime=datetime.datetime.strptime(str(nowtime),'%Y-%m-%d %H:%M:%S.%f')
        if paytime - nowtime > datetime.timedelta(minutes=shop['needytime']):
            delivered = True
        else:
            delivered = False    
        temp = {
            "name_shop": shop['name'],
            "logo_shop": shop['logo'],
            "sumprice": order['sumprice'],
            "destination": order['destination'],
            "paytime": order['paytime'],
            "needytime": shop['needytime'],
            "delivered": delivered,
            "goods":goods
        }
        result.append(temp)
        # print(temp)
    return result
    


    