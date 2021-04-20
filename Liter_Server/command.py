import json
import User
import Topic
import Massage


AVAILABLE_COMMANDS = {
    '/login': 2,
    '/new_topic': 1,
    '/update': 1,
    '/sendto': 2,
    '/close': 0
}


def analysis(cmd: str, uid=None, ip=None, need=None):
    args = cmd.split(' ')
    cmd = args[0]
    para = tuple(args[1:])
    if need and not cmd == need:
        return 0, -1
    if cmd not in AVAILABLE_COMMANDS:
        # 命令不存在 抛出异常
        raise Exception('Wrong Command')
    else:
        if not len(para) == AVAILABLE_COMMANDS.get(cmd):
            # 参数个数不对 抛出异常
            raise Exception('Wrong Parameter')
        else:
            if cmd == '/login':  # 登录
                uid, topics = User.login(*para)
                if uid:
                    topics = Topic.get(topics)
                    topics = json.dumps(topics, ensure_ascii=False)
                return uid, topics
            elif cmd == '/new_topic':
                mid = Massage.new(None, 0, '127.0.0.1', '话题由用户 {} 建立'.format(uid))
                tid = Topic.new(uid, mid, para[0])
                Massage.modify(mid, {'TID': tid})
                User.modifyTopic(uid, tid)
                resp = Topic.get(tid)
                resp = json.dumps(resp, ensure_ascii=False)
                return resp
            elif cmd == '/update':
                resp = Massage.get(str(para[0]))
                for i in range(len(resp)):
                    auth, nick = User.get(resp[i]['uid'], 'AUTHORITY,NICKNAME')
                    resp[i]['name'] = '[{}]{}'.format(auth, nick)
                    resp[i]['from_me'] = 1 if uid == resp[i]['uid'] else 0
                resp = json.dumps(resp, ensure_ascii=False)
                return resp
            elif cmd == '/sendto':
                tid, text = para
                mid = Massage.new(int(tid), uid, ip, text)
                Topic.modify(tid, {'LAST': mid})
                return ''


if __name__ == '__main__':
    analysis('/login drelf drelf...')
