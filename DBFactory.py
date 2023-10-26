# -*- coding: utf-8 -*-
import sqlite3


class DBFactory:
    conn = None
    cur = None

    def __init__(self, dbname="./db/student_083_2.db"):
        self.conn = sqlite3.connect(dbname, check_same_thread=False)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def do(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def get_fields(self, table_name):
        sql = f"PRAGMA table_info({table_name})"
        fields = [feild[1] for feild in self.do(sql)]
        return fields

    def all(self, table_name):
        sql = f"select * from {table_name}"
        return self.do(sql)

    def update(self, data: dict, table_name):
        values = []
        id_field_name = list(data)[0]
        for key in list(data)[1:]:
            values.append(f"{key}='{data[key]}'")
        sql = f"update {table_name} set {','.join(values)} where {id_field_name}=\"{data[id_field_name]}\""
        # print (sql)
        self.cur.execute(sql)
        self.conn.commit()

    def insert(self, data: dict, table_name):
        values = []
        keys = list(data)
        for key in keys:
            values.append(data[key])
        sql = f"insert into {table_name} ({','.join(keys)}) values ({','.join(['?'] * len(keys))})"
        # print(sql)
        self.cur.execute(sql, values)
        self.conn.commit()

    def delete_by_id(self, id_field_name, value, table_name):
        sql = f"delete from {table_name} where {id_field_name}=?"
        # print (sql)
        self.cur.execute(sql, (value,))
        self.conn.commit()


def init_db(dbname="./db/student_083_2.db"):
    conn = sqlite3.connect(dbname)
    return conn


def GetSql(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    fields = []
    for field in cur.description:
        fields.append(field[0])

    result = cur.fetchall()
    # for item in result:
    #     print(item)
    cur.close()
    return result, fields


def CloseDb(conn):
    conn.close()


def GetSql2(sql):
    conn = init_db()
    result, fields = GetSql(conn, sql)
    CloseDb(conn)
    return result, fields


def UpdateData(data, tablename):
    conn = init_db()
    values = []
    cusor = conn.cursor()
    idName = list(data)[0]
    for v in list(data)[1:]:
        values.append("%s='%s'" % (v, data[v]))
    sql = "update %s set %s where %s='%s'" % (
        tablename,
        ",".join(values),
        idName,
        data[idName],
    )
    # print (sql)
    cusor.execute(sql)
    conn.commit()
    CloseDb(conn)


def InsertData(data, tablename):
    conn = init_db()
    values = []
    cusor = conn.cursor()
    fieldNames = list(data)
    for v in fieldNames:
        values.append(data[v])
    sql = "insert into  %s (%s) values( %s) " % (
        tablename,
        ",".join(fieldNames),
        ",".join(["?"] * len(fieldNames)),
    )
    # print(sql)
    cusor.execute(sql, values)
    conn.commit()
    CloseDb(conn)


def DelDataById(id, value, tablename):
    conn = init_db()
    values = []
    cusor = conn.cursor()

    sql = "delete from %s  where %s=?" % (tablename, id)
    # print (sql)

    cusor.execute(sql, (value,))
    conn.commit()
    CloseDb(conn)
