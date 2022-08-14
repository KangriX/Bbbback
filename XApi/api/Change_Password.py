import json
import time
import jwt
import pymysql
from fastapi import APIRouter, Header, Depends, HTTPException
from pydantic import BaseModel
from op.Token_is_True import token_is_true
from op.Token_Decode import token_decode
from op.database_op import sql_data_change

class Account(BaseModel):
    pre_pwd: str
    new_pwd: str

router = APIRouter()

@router.post("/ChangePassword")
async def change_Password(data: Account, token: str = Header(None)):
    # 验证token
    if not token_is_true(token):
        raise HTTPException(
                status_code=401,
                detail="Incorrect token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    res = token_decode(token)
    # print(res['data']['password'])
    # print(data.pre_pwd)
    if res and res['data']['password'] == data.pre_pwd and data.new_pwd != data.pre_pwd:
        #修改数据库信息
        conn = pymysql.connect(
            host='124.222.244.117',
            port=3306,
            user='zrgj8',
            password='zrgj8',
            database='zrgj8',
            charset='utf8'
        )
        update_info = [(data.new_pwd,res['data']['account'])]
        # 修改数据库
        sql_data_change(conn, update_info)
        new_acnt = {
            "account": res['data']['account'],
            "password": data.new_pwd
            }
        # print(new_acnt)
        return {
        "code": "1",
        "msg": "密码修改成功",
        "Oauth_Token": token_encode(new_acnt)  # 返回新的token
        }
    else:
        return {
            "code": "0",
            "msg": "密码修改失败",
            "Oauth_Token": token
        }

#生成token
def token_encode(data):
    # 生成一个字典，包含我们的具体信息
    d = {
        # 公共声明
        'exp': time.time()+3000,  # (Expiration Time) 此token的过期时间的时间戳
        'iat': time.time(),  # (Issued At) 指明此创建时间的时间戳
        'iss': 'Bbback',  # (Issuer) 指明此token的签发者

        # 私有声明
        'data': {
            'account': data['account'],
            'password': data['password'],
            'timestamp': time.time()
        }
    }
    jwt_encode = jwt.encode(d, '123456', algorithm='HS256')
    # print(jwt_encode)
    return jwt_encode

