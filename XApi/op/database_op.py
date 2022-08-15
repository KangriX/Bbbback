import pymysql
from pymysql.constants import CLIENT
 
def sql_insert(data,sql):
    #用于插入一条新的用户信息
    # data 格式：data = [(1, 'kachi','123456','tzy','男',16,'5140545045','重庆大学','13251186577','971759126@qq.com','12354'),
    #                   (2, 'kachi3','1234563','yzt','男',17,'12213232','重庆大学','13251186575','971759125@qq.com','12354w')]
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
    cursor=conn.cursor()
    try:
        cursor.execute(sql, data)
        print("insert finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 涉及写操作要注意提交
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()
    return 1

def sql_insert1(sql):
    #用于插入一条新的用户信息
    # data 格式：data = [(1, 'kachi','123456','tzy','男',16,'5140545045','重庆大学','13251186577','971759126@qq.com','12354'),
    #                   (2, 'kachi3','1234563','yzt','男',17,'12213232','重庆大学','13251186575','971759125@qq.com','12354w')]
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
    cursor=conn.cursor()
    try:
        cursor.execute(sql)
        print("insert finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 涉及写操作要注意提交
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()
    return 1

def sql_data_change(update_info):
    #用于改变用户信息（这里是改密码）
    # update_info 格式：update_info = [('12345','1234')]
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
    cursor=conn.cursor()
    sql = "update customer set pwd=%s where account=%s;"
    try:
        cursor.executemany(sql, update_info)
        print("change finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 涉及写操作要注意提交
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()

def sql_data_change1(sql):
    # update_info 格式：update_info = [('12345','1234')]
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
    cursor=conn.cursor()
    try:
        cursor.execute(sql)
        print("change finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 涉及写操作要注意提交
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()

def sql_data_selectOne(account,sql):
    #用于搜索一条新的用户信息
    # account 格式：account = [('1234')]
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
    cursor=conn.cursor()
    # sql = 'select * from customer where account=%s;'
    row=None
    try:
        cursor.execute(sql, account)
        row = cursor.fetchone()  # 取一条
        print("select finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 关闭连接
    cursor.close()
    conn.close()
    return row

def sql_data_selectOne1(sql):
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
    #用于搜索一条新的用户信息
    # account 格式：account = [('1234')]
    cursor=conn.cursor()
    # sql = 'select * from customer where account=%s;'
    row=None
    try:
        cursor.execute(sql)
        row = cursor.fetchone()  # 取一条
        print("select finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 关闭连接
    cursor.close()
    conn.close()
    return row

def sql_data_selectAll(account,sql):
    #用于搜索一条新的用户信息
    # account 格式：account = [('1234')]
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
    cursor=conn.cursor()
    # sql = 'select * from customer where account=%s;'
    row=None
    try:
        cursor.execute(sql, account)
        row = cursor.fetchall()  # 取所有信息
        print("select finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 关闭连接
    cursor.close()
    conn.close()
    return row

def sql_data_selectAll1(sql):
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
    #用于搜索一条新的用户信息
    # account 格式：account = [('1234')]
    cursor=conn.cursor()
    # sql = 'select * from customer where account=%s;'
    row=None
    try:
        cursor.execute(sql)
        row = cursor.fetchall()  # 取所有信息
        print("select finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 关闭连接
    cursor.close()
    conn.close()
    return row


def sql_delete(sql):
    #用于删除一条新的用户信息
    # data 格式：data = [(1, 'kachi','123456','tzy','男',16,'5140545045','重庆大学','13251186577','971759126@qq.com','12354'),
    #                   (2, 'kachi3','1234563','yzt','男',17,'12213232','重庆大学','13251186575','971759125@qq.com','12354w')]
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
    cursor=conn.cursor()
    try:
        cursor.execute(sql)
        print("delete finish")
    except Exception as e:
        print(str(e))
        conn.rollback()
    # 涉及写操作要注意提交
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()
    return 1