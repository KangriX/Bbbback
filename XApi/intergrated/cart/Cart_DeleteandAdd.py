from fastapi import APIRouter, Header, HTTPException
import pymysql
from datetime import datetime
from op.database_op import sql_insert1
from op.database_op import sql_data_selectOne
from op.database_op import sql_data_selectOne1
from op.database_op import sql_delete
from op.database_op import sql_data_change1
from op.Token_is_True import token_is_true
from op.Token_Decode import token_decode


router = APIRouter()

@router.get('/addItemByName')
async def AddItemByName(shop_name: str, item_name: str, token: str = Header(None)):
    shop_id, cus_id, item_id = getIDs(shop_name, item_name, token)
    try:
        info = [cus_id, item_id]
        sql_4 = "SELECT * from cart where customerid = %s and menuid = %s;"
        res = menu_data_select(info, sql_4)
        # print("res = ", res)
        dt = datetime.now()
        sql_5 = 'UPDATE cart SET count = ' + str(res[4] + 1) + ', datetime = \
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
    # print(shop_id, cus_id, item_id)
    # 数据库中查找菜品
    # 连接数据库 获取购物车中相应菜品信息
    # info = [(cus_id), (shop_id), (item_id)]
    info = [cus_id, item_id]
    # print("info = ", info)
    # sql = "select * from cart where customerid = %s and shopid = %s and menuid = %s;"
    sql = "SELECT * from cart where customerid = %s and menuid = %s;"
    res = menu_data_select(info, sql)
    try:
        if res[4] == 1:
            delete_sql = 'DELETE from cart where customerid = ' + str(cus_id) + " and menuid = " + str(item_id)
            sql_delete(delete_sql)
        else:
            dt = datetime.now()
            change_sql = 'UPDATE cart SET count = ' + str(res[4] - 1) + ', datetime = \
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


def menu_data_select(info, sql):
    #用于搜索指定用户、店家、菜品的信息
    # account 格式：account = [('1234')]
    conn = pymysql.connect(
        host='124.222.244.117',
        port=3306,
        user='zrgj8',
        password='zrgj8',
        database='zrgj8',
        charset='utf8'
        )
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
