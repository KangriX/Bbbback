from fastapi.exceptions import HTTPException
import jwt
import pymysql
from fastapi import APIRouter, Header
from op.Token_is_True import token_is_true
from op.database_op import sql_data_selectOne,sql_data_selectAll1

router = APIRouter()
SECRET_KEY = "123456"

@router.get("/getShoppingCart")
async def getShoppingCart(name:str, token: str = Header(None)): #name:商家名
    # 验证token
    if not token_is_true(token):
        raise HTTPException(
                status_code=401,
                detail="Incorrect token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
    account = payload['data']['account']
    account = [(account)]
    sql_1 = 'SELECT * from customer where account=%s'
    customerid = sql_data_selectOne(account, sql_1)['id']
    # print("cus_id = ", customerid)

    # return {"code":1}

    sql_2 = 'SELECT * from shop where name=%s'
    shopid = sql_data_selectOne(name, sql_2)['id']
    # print("shop_id = ", shopid)

    sql_3 = 'SELECT * from cart where customerid='+str(customerid)+' and shopid='+str(shopid)
    
    shoppingcart = sql_data_selectAll1(sql_3)

    result = []
    sumprice = 0
    for x in shoppingcart:
        menuid = x['menuid']
        count = x['count']
        sql_4 = 'SELECT * from menu where id=%s'
        menu = sql_data_selectOne(menuid, sql_4)
        print(menu)
        sumprice += float(menu['price']) * count
        temp = {
            "name": menu['name'],
            "count":count,
            "price": menu['price'],
            "sale": menu['sale'],
            "logo": menu['logo'],
            "description": menu['description'],
            "category": menu['category']
        }
        result.append(temp)

    return {
        "sumprice":sumprice,
        "goods": result
    }
