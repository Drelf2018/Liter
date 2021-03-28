import os
import json
import time


def open_topics():
    global topics
    with open(os.path.join(os.path.dirname(__file__), 'topics.json'), encoding="utf-8") as f:
        topics = json.load(f)


def save_topics():
    with open(os.path.join(os.path.dirname(__file__), 'topics.json'), 'w', encoding="utf-8") as f:
        json.dump(topics, f, indent=4, ensure_ascii=False)


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


def new_topic(name, belong, mid):
    topics['total'] += 1
    topic = {
        'name': name,
        'regtime': time.strftime('%Y/%m/%d %H:%M', time.localtime()),
        'tid': topics['total'],
        'belong': belong,
        'first': mid,
        'last': mid
    }
    topics['tid'].append(topic)
    save_topics()
    return topics['total']


topics = {}
open_topics()
