import sqlite3
import time
import os


def new(tid: int, uid: int, ip: str, msg: str):
    c.execute("INSERT INTO MASSAGE VALUES (NULL,?,?,?,?,?);", (tid, uid, time.strftime(r'%Y/%m/%d %H:%M', time.localtime()), ip, msg))
    conn.commit()
    return c.execute('SELECT MID from MASSAGE order by MID desc limit 0,1;').fetchone()[0]


def get(mid: int):
    tid = c.execute('SELECT TID from MASSAGE where MID={}'.format(mid)).fetchone()[0]
    msgs = c.execute("SELECT MID, UID, TIME, IP, MSG from MASSAGE where TID={} AND MID>={}".format(tid, mid))
    msgs = [{"mid": row[0], "uid": row[1], "time": row[2], "ip": row[3], "text": row[4]} for row in msgs]
    return msgs


def modify(mid: int, dic: dict):
    s = ''
    for key in dic.keys():
        if isinstance(dic[key], str):
            s += '{}="{}",'.format(key, dic[key])
        else:
            s += '{}={},'.format(key, dic[key])
    c.execute("UPDATE MASSAGE set {} where MID={}".format(s[:-1], mid))
    conn.commit()


os.chdir(os.path.dirname(__file__))
conn = sqlite3.connect('massage.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS MASSAGE(
    MID  INTEGER PRIMARY KEY AUTOINCREMENT,
    TID  INTEGER NOT NULL,
    UID  INTEGER NOT NULL,
    TIME TEXT    NOT NULL,
    IP   TEXT    NOT NULL,
    MSG  TEXT    NOT NULL);''')


if __name__ == '__main__':
    cursor = c.execute('SELECT * from MASSAGE')
    for row in cursor:
        print(row)
