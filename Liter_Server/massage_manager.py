from Mybase58 import encode
import os
import json
import time


def get_path(file: str):
    return os.path.join(os.path.dirname(__file__), 'message',  encode(file) + '.json')


def get_msg(mid: int):
    page = mid//100
    mid %= 100
    file = get_path(str(page))
    if os.path.exists(file):
        with open(file, encoding="utf-8") as f:
            msg = json.load(f)
    return msg[mid]


def get_msg_line(mid):
    mid = int(mid)
    msgs = []
    page = -1
    while mid > 0:
        if not page == mid//100:
            page = mid//100
            file = get_path(str(page))
            if os.path.exists(file):
                with open(file, encoding="utf-8") as f:
                    msg = json.load(f)
            else:
                break
        mid %= 100
        msgs.append(msg[mid])
        mid = msgs[-1]['next']
    return msgs


def new_massage(ip, text, uid, last):
    global total
    total += 1
    if not last == -1:
        page = last//100
        last %= 100
        file = get_path(str(page))
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                msg = json.load(f)
            msg[last]['next'] = total
            with open(file, 'w', encoding="utf-8") as f:
                json.dump(msg, f, indent=4, ensure_ascii=False)
        else:
            return False
    last = total
    page = last//100
    last %= 100
    file = get_path(str(page))
    if not os.path.exists(file):
        fp = open(file, 'w', encoding="utf-8")
        fp.write('[{"ip": "127.0.0.1","text": "None","time": "2021/3/27 9:17","mid": -1,"from": -1,"next": -1}]')
        fp.close()
    with open(file, encoding="utf-8") as f:
        msg = json.load(f)
        msg.append({
            'ip': ip,
            'text': text,
            "time": time.strftime('%Y/%m/%d %H:%M', time.localtime()),
            "mid": total,
            'from': uid,
            'next': -1
        })
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(msg, f, indent=4, ensure_ascii=False)
    return total


total = 0
while os.path.exists(get_path(str(total))):
    total += 1
with open(get_path(str(total-1)), encoding="utf-8") as f:
    msg = json.load(f)
    total = 100 * (total-1) + len(msg) - 1
