import pymysql  # 实现连接mysql



# 插入数据
def Insert_into(url,subdomain,cname,ip):
# def Insert_into():
# 创建连接
    mysql = pymysql.connect(
        host='x.x.x.x',  # 连接地址, 本地
        user='root',  # 用户
        password='root',  # 数据库密码,记得修改为自己本机的密码
        port=3306,  # 端口,默认为3306
        charset='utf8',  # 编码
        database='ku'  # 选择数据库
    )

# print(mysql)

# 创建游标对象
#
    db = mysql.cursor()
# # # MySQL语法
#     sql = """CREATE TABLE awvs_zym (
#                 id               INT AUTO_INCREMENT PRIMARY KEY,
#                 url              varchar(50) NULL,
#                 subdomain        varchar(50) NULL,
#                 cname        varchar(50) NULL,
#                 ip               varchar(50) NULL,
#                 UNIQUE KEY `yuming_info` (subdomain,cname,ip)
#                 );
# """
#
#     try:
#         # 执行sql
#         db.execute(sql)
#         mysql.commit()	# 表示将修改操作提交到数据库
#         print('创建表成功')
#
#     except Exception as e:
#         print('操作失败',e)
#         mysql.rollback() # 表示不成功则回滚数据



# 游标关闭

# 添加两条数据

    append = 'insert into awvs_zym(url,subdomain,cname,ip) ' \
             'values(%s,%s,%s,%s) ON DUPLICATE KEY UPDATE url=url; '

    data = (url,subdomain,cname,ip)
    try:
        db.execute(append,data)
        mysql.commit()	# 表示将修改操作提交到数据库
        print('添加成功')

    except Exception as e:
        print('操作失败',e)
        mysql.rollback() # 表示不成功则回滚数据
    db.close()

    # 关闭连接
    mysql.close()


# 查询数据
def get_url_sql():
# 创建连接
    mysql = pymysql.connect(
        host='x.x.x.x',  # 连接地址, 本地
        user='root',  # 用户
        password='root',  # 数据库密码,记得修改为自己本机的密码
        port=3306,  # 端口,默认为3306
        charset='utf8',  # 编码
        database='ku'  # 选择数据库
    )


# 创建游标对象
#
    db = mysql.cursor()

# 添加两条数据

    query = "select url from awvs_zym"
    db.execute(query)
    result = db.fetchall()
    url_list = []
    for row in result:
        url_list.append(row[0])

    db.close()

    # 关闭连接
    mysql.close()
    return url_list



