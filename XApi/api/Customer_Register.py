# 引入路由管理
from unicodedata import name
from fastapi import APIRouter
from pydantic import BaseModel
# from op import personOp
from fastapi.responses import JSONResponse
# 让数据以json的格式返回
import pymysql
from op.database_op import sql_insert

class Register_Account(BaseModel):
    account: str
    password: str
    tele: str

# 构建api路由
router = APIRouter()

@router.post("/customerRegister")
async def RegisterService(data: Register_Account):
    # 连接数据库
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
    # 在数据库中插入注册用户的信息
    cus_info = [(data.account, '', data.password, '', '', '', '', '', data.tele, '', '')]
    sql = 'insert into customer(account,name,pwd,realname,sex,age,card,address,phone,email,cardcode) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    res = sql_insert(conn, cus_info, sql)
    # print(res)
    if res == 1:
        return {
        "code": "1",
        "msg": "注册成功"
        }
    return {
        "code": "0",
        "msg": "注册失败"
    }
    
        
# def customer_insert(conn,data):
#     #用于插入一条新的用户信息
#     # data 格式：data = [(1, 'kachi','123456','tzy','男',16,'5140545045','重庆大学','13251186577','971759126@qq.com','12354'),
#     #                   (2, 'kachi3','1234563','yzt','男',17,'12213232','重庆大学','13251186575','971759125@qq.com','12354w')]
#     cursor=conn.cursor()
#     sql = 'insert into customer(account,name,pwd,realname,sex,age,card,address,phone,email,cardcode) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
#     res=''
#     try:
#         res=cursor.executemany(sql, data)
#         print("insert finish")
#     except Exception as e:
#         print(str(e))
#         conn.rollback()
#     # 涉及写操作要注意提交
#     conn.commit()
#     # 关闭连接
#     cursor.close()
#     conn.close()
#     return res