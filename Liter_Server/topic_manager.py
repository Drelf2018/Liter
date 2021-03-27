import os
import json


def open_topics():
    global topics
    with open(os.path.join(os.path.dirname(__file__), 'topics.json'), encoding="utf-8") as f:
        topics = json.load(f)


def save_topics():
    with open(os.path.join(os.path.dirname(__file__), 'topics.json'), 'w', encoding="utf-8") as f:
        json.dump(topics, f, indent=4)


def get_first_mid(tid):
    tid = int(tid)
    if tid > topics['total']:
        return False
    else:
        return topics['tid'][tid]['first']


def get_last_mid(tid):
    tid = int(tid)
    if tid > topics['total']:
        return False
    else:
        return topics['tid'][tid]['last']


def set_last_mid(tid, mid):
    tid = int(tid)
    mid = int(mid)
    if tid > topics['total']:
        return False
    else:
        topics['tid'][tid]['last'] = mid
        save_topics()


topics = {}
open_topics()
