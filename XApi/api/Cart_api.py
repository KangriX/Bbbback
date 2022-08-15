import jwt
import pymysql
from pymysql.constants import CLIENT
from unicodedata import name
from op.Token_is_True import token_is_true
from op.database_op import sql_data_selectOne,sql_data_selectOne1,sql_data_selectAll1,sql_insert1,sql_delete,sql_data_change,sql_data_change1,sql_data_selectAll
from op.Token_Decode import token_decode
from fastapi import APIRouter,Header,HTTPException
from pydantic import BaseModel
from op.Token_is_True import token_is_true
import time
from datetime import datetime

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


@router.get('/addItemByName')
async def AddItemByName(shop_name: str, item_name: str, token: str = Header(None)):
    shop_id, cus_id, item_id = getIDs(shop_name, item_name, token)
    try:
        info = [cus_id, item_id]
        sql_4 = "SELECT * from cart where customerid = %s and menuid = %s;"
        res = sql_data_selectOne(info, sql_4)
        # print("res = ", res)
        dt = datetime.now()
        sql_5 = 'UPDATE cart SET count = ' + str(res["count"] + 1) + ', datetime = \
            str_to_date("%s","%%Y-%%m-%%d %%H:%%i:%%S") where customerid = '%dt + str(cus_id) + " and menuid = " + str(item_id)
        sql_data_change1(sql_5)
        return {
                'code':1,
                'msg':'success'
            }
    except Exception as e:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql_5 = 'INSERT INTO cart(customerid,shopid,menuid,count,datetime) \
            value(%d,%d,%d,%d,str_to_date("%s","%%Y-%%m-%%d %%H:%%i:%%S"))'%(cus_id,shop_id,item_id,1,dt)
        sql_insert1(sql_5)
        return {
            'code':1,
            'msg':'success'
        }
    

@router.get('/deleteItemByName')
async def deleteItemByName(shop_name: str, item_name: str, token: str = Header(None)):    
    shop_id, cus_id, item_id = getIDs(shop_name, item_name, token)
    info = [cus_id, item_id]
    # print("info = ", info)
    # sql = "select * from cart where customerid = %s and shopid = %s and menuid = %s;"
    sql = "SELECT * from cart where customerid = %s and menuid = %s;"
    res = sql_data_selectOne(info, sql)
    # print("res = ", res)
    try:
        if res['count'] == 1:
            delete_sql = 'DELETE from cart where customerid = ' + str(cus_id) + " and menuid = " + str(item_id)
            sql_delete(delete_sql)
        else:
            dt = datetime.now()
            change_sql = 'UPDATE cart SET count = ' + str(res['count'] - 1) + ', datetime = \
            str_to_date("%s","%%Y-%%m-%%d %%H:%%i:%%S") where customerid = '%dt + str(cus_id) + " and menuid = " + str(item_id)
            sql_data_change1(change_sql)
        return {
            "code": 1,
            "msg": "删除成功"
        }
    except Exception as e:
        return {
            "code": 0,
            "msg": "删除失败"
        }
        
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
    info = token_decode(token)
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

@router.get("/confirmShoppingCart")
async def confirmShoppingCart(name: str, token: str = Header(None)):
    #用于将购物车内容移到订单处，并且删除购物车数据库内容，返回订单信息
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
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor,
    client_flag=CLIENT.MULTI_STATEMENTS
    )
    now = datetime.now()
    st=now.strftime('%Y-%m-%d %H:%M:%S')
    info=token_decode(token)
    account=info['data']['account']
    # 获取一个光标
    cursor = conn.cursor()
    # 定义将要执行的SQL语句'
    sel_order_sql='select id,shopid,customerid,menuid,count from cart where shopid=(select id from shop where name=%s and customerid=(select id from customer where account=%s)) '
    add_sql = "insert into orders(shopid,customerid,paytime,delivered,sumprice) values(%s,%s,%s,%s,%s);"
    sel_price_sql='select price from menu where id=(%s)'#使用菜品id
    delete_sql="delete from cart where id=%s;"
    history_sql='insert into history(orderid,menuid,count) values(%s,%s,%s);'
    get_last_sql='select id from orders order by id desc limit 0,1;'
    sumprice=0
    res=getShoppingCart(name,token)
    # 拼接并执行SQL语句
    # try:
    p=cursor.execute(sel_order_sql, [name,account])
    sel_order_res=cursor.fetchall()
    for dic in sel_order_res:
        cursor.execute(sel_price_sql,dic['menuid'])
        sumprice+=(cursor.fetchone()['price'])*dic['count']
    cursor.execute(add_sql,[sel_order_res[0]['shopid'],sel_order_res[0]['customerid'],st,1,sumprice])
    #添加完成后，获取order数据库最后一条的id，用于记录历史
    lastid=cursor.execute(get_last_sql)
    for dic in sel_order_res:
        cursor.execute(history_sql,[lastid,dic['menuid'],dic['count']])
    cursor.executemany(delete_sql,[[dic['id']] for dic in sel_order_res])
    # except Exception as e:
    #     print(str(e))
    #     conn.rollback()
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()
    return res

def getIDs(shop_name, item_name, token):
    # 验证token
    if not token_is_true(token):
        raise HTTPException(
                status_code=401,
                detail="Incorrect token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    sql = "SELECT * from shop where name = %s"
    res = sql_data_selectOne(shop_name, sql)
    shop_id = res['id']

    # token解码 获取用户信息
    cus_info = token_decode(token)
    acnt = cus_info['data']['account']

    sql = "SELECT * from customer where account = %s"
    res = sql_data_selectOne(acnt, sql)
    cus_id = res['id']

    sql = "SELECT * from menu where name = %s"
    res = sql_data_selectOne(item_name, sql)
    item_id = res['id']

    return shop_id, cus_id, item_id


def getShoppingCart(name:str, token: str = Header(None)): #name:商家名
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
    sql_1 = 'select * from customer where account=%s'
    customerid = sql_data_selectOne(account, sql_1)['id']

    # return {"code":1}

    sql_2 = 'select * from shop where name=%s'
    shopid = sql_data_selectOne(name, sql_2)['id']

    sql_3 = 'select * from cart where customerid=%s and shopid=%s'
    shoppingcart = sql_data_selectAll([customerid,shopid],sql_3)

    result = []
    sumprice = 0
    for x in shoppingcart:
        menuid = x['menuid']
        count = x['count']
        sql_4 = 'select * from menu where id=%s'
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