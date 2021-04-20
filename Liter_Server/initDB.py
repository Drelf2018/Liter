import sqlite3
import time
import os


def Unew(username: str, password: str, mail: str):
    c.execute("INSERT INTO USER (USERNAME,NICKNAME,PASSWORD,REGTIME,MAIL) VALUES (?,?,?,?,?);",
              (username, username, password, time.strftime(r'%Y/%m/%d %H:%M', time.localtime()), mail))
    conn.commit()
    return c.execute('SELECT UID from USER order by UID desc limit 0,1;').fetchone()[0]


def modifyTopic(uid: int, tid: int):
    cursor = c.execute('SELECT TOPIC from USER where UID={}'.format(uid))
    topic = cursor.fetchone()[0].split('|')
    while '' in topic:
        topic.remove('')
    if tid > 0 and str(tid) not in topic:
        topic.append(str(tid))
    elif tid < 0 and str(-tid) in topic:
        topic.remove(str(-tid))
    c.execute("UPDATE USER set TOPIC='{}' where UID={}".format('|'.join(topic), uid))
    conn.commit()


os.chdir(os.path.dirname(__file__))
conn = sqlite3.connect('user.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS USER(
    UID       INTEGER PRIMARY KEY AUTOINCREMENT,
    STATUS    TEXT    NOT NULL DEFAULT 'Normal',
    AUTHORITY TEXT    NOT NULL DEFAULT 'Default',
    USERNAME  TEXT    NOT NULL,
    NICKNAME  TEXT    NOT NULL,
    PASSWORD  TEXT    NOT NULL,
    REGTIME   TEXT    NOT NULL,
    MAIL      TEXT    NOT NULL,
    NAME      TEXT    DEFAULT 'unknown',
    SEX       TEXT    DEFAULT 'unknown',
    AGE       INTEGER DEFAULT 0,
    TOPIC     TEXT    DEFAULT '');''')
Unew('drelf', 'drelf...', '3099665076@qq.com')
Unew('kidd', 'ABC123', '759984721@qq.com')
Unew('lazier', 'n199er', '1@163.com')
modifyTopic(1, 1)
modifyTopic(1, 2)
modifyTopic(1, 3)
modifyTopic(2, 1)
modifyTopic(2, 2)
modifyTopic(3, 1)
c.close()


def Mnew(tid: int, uid: int, ip: str, msg: str):
    c.execute("INSERT INTO MASSAGE VALUES (NULL,?,?,?,?,?);", (tid, uid, time.strftime(r'%Y/%m/%d %H:%M', time.localtime()), ip, msg))
    conn.commit()
    return c.execute('SELECT MID from MASSAGE order by MID desc limit 0,1;').fetchone()[0]


conn = sqlite3.connect('massage.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS MASSAGE(
    MID  INTEGER PRIMARY KEY AUTOINCREMENT,
    TID  INTEGER NOT NULL,
    UID  INTEGER NOT NULL,
    TIME TEXT    NOT NULL,
    IP   TEXT    NOT NULL,
    MSG  TEXT    NOT NULL);''')
Mnew(1, 3, '127.0.0.1', '话题由用户 {} 建立'.format(3))
Mnew(2, 2, '127.0.0.1', '话题由用户 {} 建立'.format(2))
Mnew(3, 1, '127.0.0.1', '话题由用户 {} 建立'.format(1))
Mnew(1, 1, '127.0.0.1', '话题一')
Mnew(2, 1, '127.0.0.1', '话题二')
Mnew(3, 1, '127.0.0.1', '话题三')
c.close()


def Tnew(uid: int, mid: int, name: str, icon=None):
    c.execute("INSERT INTO TOPIC VALUES (NULL,?,?,?,?,?,?);", (uid, mid, mid, name, time.strftime(r'%Y/%m/%d %H:%M', time.localtime()), icon))
    conn.commit()
    return c.execute('SELECT TID from TOPIC order by TID desc limit 0,1;').fetchone()[0]


def modify(tid: int, dic: dict):
    s = ''
    for key in dic.keys():
        if isinstance(dic[key], str):
            s += '{}="{}",'.format(key, dic[key])
        else:
            s += '{}={},'.format(key, dic[key])
    c.execute("UPDATE TOPIC set {} where TID={}".format(s[:-1], tid))
    conn.commit()


conn = sqlite3.connect('topic.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS TOPIC(
    TID     INTEGER PRIMARY KEY AUTOINCREMENT,
    BELONG  INTEGER NOT NULL,
    FIRST   INTEGER NOT NULL,
    LAST    INTEGER NOT NULL,
    NAME    TEXT    NOT NULL,
    REGTIME TEXT    NOT NULL,
    ICON    TEXT    DEFAULT '');''')
Tnew(3, 1, '测试一')
Tnew(2, 2, '测试二')
Tnew(1, 3, '测试三')
modify(1, {'LAST': 4})
modify(2, {'LAST': 5})
modify(3, {'LAST': 6})
c.close()
