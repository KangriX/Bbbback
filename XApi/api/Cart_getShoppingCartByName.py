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
    conn = pymysql.connect(
        host='124.222.244.117',
        port=3306,
        user='zrgj8',
        password='zrgj8',
        database='zrgj8',
        charset='utf8'
    )
    payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
    account = payload['data']['account']
    account = [(account)]
    sql_1 = 'SELECT * from customer where account=%s'
    customerid = sql_data_selectOne(conn, account, sql_1)[0]
    # print("cus_id = ", customerid)

    # return {"code":1}

    sql_2 = 'SELECT * from shop where name=%s'
    conn = pymysql.connect(
        host='124.222.244.117',
        port=3306,
        user='zrgj8',
        password='zrgj8',
        database='zrgj8',
        charset='utf8'
    )
    shopid = sql_data_selectOne(conn, name, sql_2)[0]
    # print("shop_id = ", shopid)

    sql_3 = 'SELECT * from cart where customerid='+str(customerid)+' and shopid='+str(shopid)
    
    shoppingcart = sql_data_selectAll1(sql_3)

    result = []
    sumprice = 0
    for x in shoppingcart:
        menuid = x[3]
        count = x[4]
        sql_4 = 'select * from menu where id=%s'
        conn = pymysql.connect(
        host='124.222.244.117',
        port=3306,
        user='zrgj8',
        password='zrgj8',
        database='zrgj8',
        charset='utf8'
        )
        menu = sql_data_selectOne(conn, menuid, sql_4)
        print(menu)
        sumprice += float(menu[3]) * count
        temp = {
            "name": menu[2],
            "count":count,
            "price": menu[3],
            "sale": menu[4],
            "logo": menu[5],
            "description": menu[6],
            "category": menu[7]
        }
        result.append(temp)

    return {
        "sumprice":sumprice,
        "goods": result
    }
