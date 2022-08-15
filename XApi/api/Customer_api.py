from op.Token_Encode import token_encode
# 引入路由管理
import time
from unicodedata import name
from fastapi import APIRouter
from pydantic import BaseModel
from op.database_op import sql_insert
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
        # 在数据库中检索该账号
        # cus_info = [(data.account, '', data.password, '', '', '', '', '', '', '', '')]
        acnt = [(data.account)]
        sql = 'SELECT * from customer where account=%s;'
        temp = sql_data_selectOne(acnt, sql)
        # print(temp)
        if temp and data.password == temp['pwd']:
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


class Register_Account(BaseModel):
    account: str
    password: str
    tele: str

@router.post("/customerRegister")
async def RegisterService(data: Register_Account):
    # print(data.account)
    # print(data.password)
    # 在数据库中插入注册用户的信息
    try:
        cus_info = [data.account, '', data.password, '', '', '', '', '', data.tele, '', '']
        sql = 'INSERT into customer(account,name,pwd,realname,sex,age,card,address,phone,email,cardcode) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        res = sql_insert(cus_info, sql)
        return {
        "code": "1",
        "msg": "注册成功"
        }
    except Exception(e):
        print(str(e))
        return {
            "code": "0",
            "msg": "注册失败"
        }