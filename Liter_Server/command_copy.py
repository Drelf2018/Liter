import json
import user_manager as um
import massage_manager as mm
import topic_manager as tm


AVAILABLE_COMMANDS = {
    '/login': 2,
    '/update': 1,
    '/sendto': 2,
    '/close': 0
}


def analysis_command(cmd: str, need=None, user=None):
    args = cmd.split(' ')
    if need and not args[0] == need:
        return False
    para = tuple(args[1:])
    if not args[0] in AVAILABLE_COMMANDS:
        raise Exception('Wrong Command')
    else:
        if len(para) == AVAILABLE_COMMANDS.get(args[0]):
            if args[0] == '/login':
                resp = um.check(*para)
                if resp[0]:
                    resp[1] = [tm.topics['tid'][r] for r in resp[1]]
                    resp[1] = str(json.dumps(resp[1], ensure_ascii=False))
            elif args[0] == '/update':
                resp = mm.get_msg_line(*para)
                for i in range(len(resp)):
                    uid = resp[i]['from']
                    auth, nick = um.users['uid'][uid]['authority'], um.users['uid'][uid]['nickname']
                    resp[i]['from'] = '[{}]{}'.format(auth, nick)
                resp = str(json.dumps(resp, ensure_ascii=False))
            elif args[0] == '/sendto':
                mid = tm.get_last_mid(para[0])
                mid = mm.new_massage(user[1], para[1], user[0], mid)
                tm.set_last_mid(para[0], mid)
                resp = mm.get_msg(mid)
                uid = resp['from']
                auth, nick = um.users['uid'][uid]['authority'], um.users['uid'][uid]['nickname']
                resp['from'] = '[{}]{}'.format(auth, nick)
                resp = str(json.dumps(resp, ensure_ascii=False))
            elif args[0] == '/close':
                resp = False
            return resp
        else:
            raise Exception('Wrong Parameter')
