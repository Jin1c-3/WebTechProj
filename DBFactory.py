# -*- coding: utf-8 -*-
import sqlite3
import hmac
import hashlib
import pickle


class DBFactory:
    conn = None
    cur = None

    def __init__(self, dbname="./db/student_083_2.db"):
        self.conn = sqlite3.connect(dbname, check_same_thread=False)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def do(self, sql, *value):
        """
        @param sql: sql语句
        @param value: sql语句中的参数，是可变长的
        """
        self.cur.execute(sql, value)
        self.conn.commit()
        return self.cur.fetchall()
    
    def register(self, username, password):
        encrytor=hmac.new(bytes(username,encoding='utf-8'),pickle.dumps(password),hashlib.sha256)
        self.insert({"username": username, "pwd": encrytor.hexdigest()}, "users")

    def validate_username_password(self, username, password):
        """
        len长度大于零就是对的
        """
        encrytor=hmac.new(bytes(username,encoding='utf-8'),pickle.dumps(password),hashlib.sha256)
        return (
            len(
                self.do(
                    "select * from users where username=? and pwd=?",
                    username,
                    encrytor.hexdigest(),
                )
            )
            > 0
        )

    def get_fields(self, table_name):
        """
        @param table_name: 表名
        获取表的字段名
        """
        sql = f"PRAGMA table_info({table_name})"
        fields = [feild[1] for feild in self.do(sql)]
        return fields

    def all(self, table_name):
        """
        @param table_name: 表名
        获取表的所有数据
        """
        sql = f"select * from {table_name}"
        return self.do(sql)

    def update(self, data: dict, table_name):
        """
        @param data: 数据的第一个字段必须是id，字段名可以不是id
        """
        values = []
        id_field_name = list(data)[0]
        for key in list(data)[1:]:
            values.append(f"{key}='{data[key]}'")
        sql = f"update {table_name} set {','.join(values)} where {id_field_name}=?"
        print(sql)
        print(data[id_field_name])
        self.do(sql, data[id_field_name])
        self.conn.commit()

    def insert(self, data: dict, table_name):
        values = []
        keys = list(data)
        for key in keys:
            values.append(data[key])
        sql = f"insert into {table_name} ({','.join(keys)}) values ({','.join(['?'] * len(keys))})"
        self.cur.execute(sql, values)
        self.conn.commit()

    def delete_by_id(self, id_field_name, value: str, table_name):
        sql = f"delete from {table_name} where {id_field_name}=?"
        self.cur.execute(sql, (value,))
        self.conn.commit()
