import pymysql
def getAllShopInfo():
    conn = pymysql.connect(
    host='124.222.244.117',
    port=3306,
    user='zrgj8',
    password='zrgj8',
    database='zrgj8',
    charset='utf8'
    )
    cursor=conn.cursor()
    sql = 'select name,credit,sale,needytime,distance,logo,thresholdprice from shop;'
    res=None
    try:
        cursor.execute(sql)
        res=cursor.fetchall()
        print("finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 关闭连接
    cursor.close()
    conn.close()
    dic={}
    for i in res:
        dic[i[0]]=list(i)
    return dic

def selectShopByName(name:str):
    # 打开数据库连接
    db = pymysql.connect(
        host="124.222.244.117", 
        user="zrgj8", 
        password="zrgj8", 
        database="zrgj8",
        cursorclass=pymysql.cursors.DictCursor
        )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # SQL 插入语句
    sql = """SELECT * FROM `shop` where name like """  + """'"""+name+"""'"""
    
    try:
    # 执行sql语句
        cursor.execute(sql)
        data = cursor.fetchall()   
    ## 把查询的数据填充到person对象是否可以(要循环这个游标进行数据的填充)
    ## 可以将查询的数据填充(组合)到自定义的模型中
    # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
    # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    cursor.close()
    db.close()
    return data