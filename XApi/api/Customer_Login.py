from op.Token_Encode import token_encode
# 引入路由管理
import time
from unicodedata import name
from fastapi import APIRouter
from pydantic import BaseModel
# from op import personOp
import pymysql
from op.database_op import sql_data_selectOne

class Account(BaseModel):
    account: str
    password: str

# 构建api路由
router = APIRouter()
# 连接数据库

@router.post("/customerLogin")
async def loginService(data: Account):
        conn = pymysql.connect(
            host='124.222.244.117',
            port=3306,
            user='zrgj8',
            password='zrgj8',
            database='zrgj8',
            charset='utf8'
        )
        # print(data.account)
        # print(data.password)
        # 在数据库中检索该账号
        # cus_info = [(data.account, '', data.password, '', '', '', '', '', '', '', '')]
        acnt = [(data.account)]
        sql = 'select * from customer where account=%s;'
        temp = sql_data_selectOne(conn, acnt, sql)
        # print(temp)
        if temp and data.password == temp[3]:
            return {
                "code": 1,
                "msg": "登录成功",
                "data": {
                    "Oauth_Token": token_encode(data),
                    "exprie": time.time() + 3000
                }
            }
        else:
            return {
                    "code": 0,
                    "msg": "账号不存在或账号密码错误",
                    "data": {
                        "Oauth_Token": None,
                        "exprie": time.time() + 3000
                    }
            }
            

# #用于搜索一条新的用户信息
# def customer_data_select(conn,account):
#     # account 格式：account = [('1234')]
#     cursor=conn.cursor()
#     sql = 'select * from customer where account=%s;'
#     row=''
#     try:
#         cursor.executemany(sql, account)
#         row = cursor.fetchone()  # 取一条
#         print("select finish")
#     except Exception as e:
#         print(str(e))
#         conn.rollback()
#     # 关闭连接
#     cursor.close()
#     conn.close()
#     return row
