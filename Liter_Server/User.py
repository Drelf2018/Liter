import sqlite3
import time
import os


def all_number(s: str):
    try:
        int(s)
    except Exception:
        return False
    return True


def new(username: str, password: str, mail: str):
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


def login(uid: str, pwd: str):
    if '@' in uid:  # 邮箱
        cursor = c.execute('SELECT UID, PASSWORD, TOPIC from USER where MAIL="{}"'.format(uid))
    elif all_number(uid):  # 账号
        cursor = c.execute('SELECT UID, PASSWORD, TOPIC from USER where UID={}'.format(uid))
    else:  # 用户名
        cursor = c.execute('SELECT UID, PASSWORD, TOPIC from USER where USERNAME="{}"'.format(uid))
    info = cursor.fetchone()
    if not info:
        return 0, None
    else:
        uid, password, topic = info
        if pwd == password:
            topic = [int(t) for t in topic.split('|')]
            return uid, topic
        else:
            return 0, None


def get(uid: int, need: str):
    return c.execute('SELECT {} from USER where UID={}'.format(need, uid)).fetchone()


def modify(uid: int, dic: dict):
    s = ''
    for key in dic.keys():
        if isinstance(dic[key], str):
            s += '{}="{}",'.format(key, dic[key])
        else:
            s += '{}={},'.format(key, dic[key])
    c.execute("UPDATE USER set {} where UID={}".format(s[:-1], uid))
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

if __name__ == '__main__':
    cursor = c.execute('SELECT * from USER')
    for row in cursor:
        print(row)
    print(login('1', 'drelf...'))
