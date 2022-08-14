from fastapi import APIRouter, Header, HTTPException
import pymysql
from op.database_op import sql_data_selectOne
from op.Token_is_True import token_is_true
from op.Token_Decode import token_decode


router = APIRouter()

@router.get('/addItemByName')
async def AddItemByName(shop_name: str, item_name: str, token: str = Header(None)):
    shop_id, cus_id, item_id = getIDs(shop_name, item_name, token)
    # print(shop_id, cus_id, item_id)
    # 数据库中查找菜品
    # 连接数据库 获取购物车中相应菜品信息
    conn = pymysql.connect(
        host='124.222.244.117',
        port=3306,
        user='zrgj8',
        password='zrgj8',
        database='zrgj8',
        charset='utf8'
        )
    # info = [(cus_id), (shop_id), (item_id)]
    info = [shop_id, item_id]
    print(info)
    # sql = "select * from cart where customerid = %s and shopid = %s and menuid = %s;"
    sql = "select * from cart where shopid = %s and menuid = %s;"
    res = menu_data_select(conn, info, sql)
    print(res)


@router.get('/deleteItemByName')
async def deleteItemByName(shop_name: str, item_name: str, token: str = Header(None)):    
    shop_id, cus_id, item_id = getIDs(shop_name, item_name, token)
    # print(shop_id, cus_id, item_id)





def getIDs(shop_name, item_name, token):
    # 验证token
    if not token_is_true(token):
        raise HTTPException(
                status_code=401,
                detail="Incorrect token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    # 连接数据库 获取商家id
    conn = pymysql.connect(
        host='124.222.244.117',
        port=3306,
        user='zrgj8',
        password='zrgj8',
        database='zrgj8',
        charset='utf8'
        )
    sql = "select * from shop where name = %s"
    res = sql_data_selectOne(conn, shop_name, sql)
    shop_id = res[0]

    # token解码 获取用户信息
    cus_info = token_decode(token)
    acnt = cus_info['data']['account']
    # 连接数据库 获取用户id
    conn = pymysql.connect(
        host='124.222.244.117',
        port=3306,
        user='zrgj8',
        password='zrgj8',
        database='zrgj8',
        charset='utf8'
        )
    sql = "select * from customer where account = %s"
    res = sql_data_selectOne(conn, acnt, sql)
    cus_id = res[0]

    # 连接数据库 获取用户id
    conn = pymysql.connect(
        host='124.222.244.117',
        port=3306,
        user='zrgj8',
        password='zrgj8',
        database='zrgj8',
        charset='utf8'
        )
    sql = "select * from menu where name = %s"
    res = sql_data_selectOne(conn, item_name, sql)
    item_id = res[0]

    return shop_id, cus_id, item_id


def menu_data_select(conn, info, sql):
    #用于搜索指定用户、店家、菜品的信息
    # account 格式：account = [('1234')]
    cursor=conn.cursor()
    # sql = 'select * from customer where account=%s;'
    row=None
    try:
        cursor.execute(sql, info)
        row = cursor.fetchone()  # 取一条
        print("menu select finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 关闭连接
    cursor.close()
    conn.close()
    return row