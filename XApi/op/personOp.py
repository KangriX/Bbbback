
from tokenize import String
import  pymysql
import json
 
def  selectPersonByName(name:String):
    # 打开数据库连接
    db = pymysql.connect(host="124.222.244.117", user="zrgj", password="zrgj", database="abc")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor(cursor = pymysql.cursors.DictCursor)
    # SQL 插入语句
    sql = """SELECT * FROM `customer` where account= """  + """'"""+name+"""'"""
    
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
    return data[0]