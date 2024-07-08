import sqlalchemy

import tables
from config import *


def confirm(msg: str):
    print(msg, end="")
    word = input("(y或yes表示是，其他表示否) ")
    if word.lower() in ("y", "yes"):
        return True
    return False


def main():
    if not confirm("请确认：使用%s用户登录位于%s:%d的%s数据库?" % (USERNAME, HOST, PORT, DIALECT)):
        return

    engine = sqlalchemy.create_engine(
        "%s+%s://%s:%s@%s:%d/?charset=utf8" % (DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT))

    connection = engine.connect()
    print("数据库连接成功！")

    rs = connection.execute(sqlalchemy.text("show databases like '%s'" % DATABASE))
    if len(rs.fetchall()) == 0:
        print("目标数据库不存在，正在创建数据库...")
        connection.execute(sqlalchemy.text("create database `%s` charset=`utf8`" % DATABASE))
        connection.close()

        engine = sqlalchemy.create_engine(
            "%s+%s://%s:%s@%s:%d/%s?charset=utf8" % (DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE))
        connection = engine.connect()
        tables.db.metadata.create_all(connection)
        print("数据库创建成功！")
    else:
        print("目标数据库已存在，退出")


if __name__ == "__main__":
    main()
