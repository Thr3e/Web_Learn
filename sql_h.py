#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' sql handler module '            #表示模块的文档注释

__author__ = 'Thr3e'

import sqlite3
import time

__dbname__ = 'weblearn.db'
__htmltable__ = 'Articles_html'

def __dbhandler__(func):
    conn = sqlite3.connect(__dbname__)
    args = func(conn.cursor())
    c = args['cursor']
    c.close()
    conn.commit()
    conn.close()
    args.pop('cursor')
    return args

#初始化文章内容表
def init_htmlDB():
    def fo(c):
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='%s';"%(__htmltable__))
        if(c.fetchone()):
            pass
        else:
            c.execute('''
                CREATE TABLE %s
                (ID INT PRIMARY KEY NOT NULL,
                TITLE TEXT,
                CONTENT TEXT,
                ART_ID INT);
            '''%(__htmltable__))
        return {"cursor":c}
    __dbhandler__(fo)

#获取数据库所有表
def query_table_name():
    def fo(c):
        cursor = c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables=[]
        for row in cursor:
            if(row[0] != __htmltable__):
                tables.append(row[0])
            else:
                pass
        tables.reverse()
        return {"cursor":c,'tables':tables}
    return __dbhandler__(fo)['tables']

#最近的表名
latest_table = query_table_name()[0]

#通过id查询文章信息
def query_art_by_id(num):
    def fo(c):
        cursor = c.execute('SELECT * FROM %s WHERE ID=?'%(latest_table), (int(num),))
        data=[]
        for row in cursor:
            data.append({'id':row[0],'title':row[1],'url':row[2],'update_time':row[3],'likes':row[4]})
        return {"cursor":c,'data':data}
    return __dbhandler__(fo)['data']

#获取数据库数据
def query_art_by_title(db_name=latest_table, key="*"):
    def fo(c):
        sel_sql="SELECT * FROM %s WHERE TITLE LIKE '%%%s%%' ORDER BY ID;"%(db_name, key)
        if(key =="*"):
            sel_sql = "SELECT * FROM %s ORDER BY ID;"%(db_name)
        cursor = c.execute(sel_sql)
        data=[]
        for row in cursor:
            data.append({'id':row[0],'title':row[1],'url':row[2],'update_time':row[3],'likes':row[4]})
        data.reverse()
        return {"cursor":c,'data':data}
    return __dbhandler__(fo)['data']

#最近的文章数据
latest_art = query_art_by_title(latest_table)

#初始化列表table
def init_listtable():
    def fo(c):
        db_name="Articles_database_" + str(int(time.mktime(time.localtime())))
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='%s';"%(db_name))
        if(c.fetchone()):
            pass
        else:
            c.execute('''
                CREATE TABLE %s
                (ID INT PRIMARY KEY NOT NULL,
                TITLE TEXT,
                URL TEXT,
                TIME TEXT,
                LIKES INT);
            '''%(db_name))
        return {"cursor":c,'db_name':db_name}
    return __dbhandler__(fo)['db_name']

#存储到数据库
def db_restore(data):
    db_name = init_listtable()
    def fo(c):
        i=0
        for obj in data:
            i = i + 1
            c.execute("INSERT INTO %s (ID,TITLE,URL,TIME,LIKES) VALUES (?,?,?,?,?)"%(db_name),(obj['id'], obj['title'], obj['url'], obj['update_time'], obj['likes']))
        print('DataBase Commit!')
        return {"cursor":c}
    return __dbhandler__(fo)

#验证html表中是否已存在id对应值
def verif_htmldb(num):
    def fo(c):
        cursor = c.execute('SELECT * FROM %s WHERE ID=?'%(__htmltable__), (int(num),))
        has_data = len(cursor.fetchall()) != 0
        return {"cursor":c,'has_data':has_data}
    return __dbhandler__(fo)['has_data']

#存储文章数据
def update_contdb(data):
    init_htmlDB()
    def fo(c):
        if(verif_htmldb(data['id'])):
            c.execute("UPDATE %s SET CONTENT=? WHERE ID=?"%(__htmltable__),(data['cont'],data['id'],))
        else:
            c.execute("INSERT INTO %s (ID,TITLE,CONTENT,ART_ID) VALUES (?,?,?,?);"%(__htmltable__),(data['id'], data['title'], data['cont'], data['id']))
        return {"cursor":c}
    return __dbhandler__(fo)

#比较两个数据库
def query_new_art():
    table_list=query_table_name()
    old=table_list[1]
    new=table_list[0]
    def fo(c):
        diff=[]
        c.execute("SELECT * FROM {0} WHERE NOT EXISTS(SELECT 1 FROM {1} WHERE {1}.ID = {0}.ID)".format(new,old))
        diff = diff+c.fetchall()
        c.execute("SELECT * FROM {0} WHERE EXISTS(SELECT 1 FROM {1} WHERE {1}.ID = {0}.ID AND {1}.TIME <> {0}.TIME)".format(new,old))
        diff = diff+c.fetchall()
        res=[]
        for tup in diff:
            res.append({
                'id':tup[0],
                'title':tup[1],
                'url':tup[2],
                "update_time":tup[3],
                "like":tup[4]
            })
        return {"cursor":c,'res':res}
    return __dbhandler__(fo)['res']

