import sqlite3
import time
import os


def new(uid: int, mid: int, name: str, icon=None):
    c.execute("INSERT INTO TOPIC VALUES (NULL,?,?,?,?,?,?);", (uid, mid, mid, name, time.strftime(r'%Y/%m/%d %H:%M', time.localtime()), icon))
    conn.commit()
    return c.execute('SELECT TID from TOPIC order by TID desc limit 0,1;').fetchone()[0]


def get(tid: list):
    s = ''
    topics = []
    for t in tid:
        s += 'TID={} OR '.format(t)
    cursor = c.execute('SELECT * from TOPIC where {}'.format(s[:-4]))
    for row in cursor:
        topics.append(
            {
                'tid': row[0],
                'belong': row[1],
                'first': row[2],
                'last': row[3],
                'name': row[4],
                'regtime': row[5],
                'icon': row[6]
            }
        )
    return topics


def modify(tid: int, dic: dict):
    s = ''
    for key in dic.keys():
        if isinstance(dic[key], str):
            s += '{}="{}",'.format(key, dic[key])
        else:
            s += '{}={},'.format(key, dic[key])
    c.execute("UPDATE TOPIC set {} where TID={}".format(s[:-1], tid))
    conn.commit()


os.chdir(os.path.dirname(__file__))
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


if __name__ == '__main__':
    cursor = c.execute('SELECT * from TOPIC')
    for row in cursor:
        print(row)
