from Mybase58 import encode
import os
import json
import time


def open_users():
    global users, dic
    with open(os.path.join(os.path.dirname(__file__), 'users.json'), encoding="utf-8") as f:
        users = json.load(f)
    for i in range(1, users['total']+1):
        dic[users['uid'][i]['username']] = i
        dic[users['uid'][i]['mail']] = i


def save_users():
    with open(os.path.join(os.path.dirname(__file__), 'users.json'), 'w', encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def check(uid, pwd: str):
    if not type(uid) == int:
        uid = dic.get(uid)
    if not uid:
        return [False, None]
    pwd = encode(pwd)
    if uid <= users['total']:
        user = users['uid'][uid]
        if pwd == user['password']:
            return [uid, user['topic']]
        else:
            return [False, None]
    else:
        return [False, None]


def new_user(username='unknown', nickname="unknown", password='ABC123', mail='unknown'):
    user = {
        'status': 'Normal',
        'authority': 'Default',
        'username': username,
        'nickname': nickname,
        'password': encode(password),
        'regtime': time.strftime('%Y/%m/%d %H:%M', time.localtime()),
        'name': "unknown",
        'age': "unknown",
        'sex': "unknown",
        'mail': mail
    }
    users['uid'].append(user)
    users['total'] += 1
    save_users()


def del_user(uid: int):
    if uid <= users['total']:
        users['uid'][uid]['status'] = 'Delete'
    save_users()


def modify_user(uid: int, val: dict):
    if uid <= users['total']:
        user = users['uid'][uid]
        for key in val:
            if key in user:
                user[key] = val[key]
        users['uid'][uid] = user
        save_users()
    else:
        pass


users, dic = {}, {}
open_users()
