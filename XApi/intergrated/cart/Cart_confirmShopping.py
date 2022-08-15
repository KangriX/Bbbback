import pymysql
from op import Token_Decode
import datetime
from pymysql.constants import CLIENT
from fastapi.exceptions import HTTPException
import jwt
from fastapi import APIRouter, Header
from op.Token_is_True import token_is_true
from op.database_op import sql_data_selectOne,sql_data_selectAll

# 构建api路由
router = APIRouter()
SECRET_KEY='123456'
# 连接数据库

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
    now = datetime.datetime.now()
    st=now.strftime('%Y-%m-%d %H:%M:%S')
    info=Token_Decode.token_decode(token)
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
    try:
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
    except Exception as e:
        print(str(e))
        conn.rollback()
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()
    return res


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
