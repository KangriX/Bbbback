import pymysql
from fastapi import APIRouter,Header, Depends, HTTPException
from pydantic import BaseModel
from op.Token_is_True import token_is_true

router = APIRouter()
@router.get("/getAllShopInfo")
async def getAllShopInfo(*, token: str = Header(None)):
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
    cursor=conn.cursor()
    sql = 'select name,credit,sale,needytime,distance,logo,thresholdprice,id from shop;'
    res=None
    lis=['name','credit','sale','needytime','distance','logo','thresholdprice','id']
    try:
        cursor.execute(sql)
        res=cursor.fetchall()
        # print("finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 关闭连接
    cursor.close()
    conn.close()
    eli=[]
    for i in res:
        dic={}
        for x in range(8):
            dic[lis[x]]=i[x]
        eli.append(dic)
    return eli