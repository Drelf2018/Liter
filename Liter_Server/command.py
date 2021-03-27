import json
import user_manager as um
import massage_manager as mm


AVAILABLE_COMMANDS = {
    '/login': [2, um.check],
    '/update': [1, mm.get_msg_line],
    '/close': [0, lambda: False]
}


def analysis_command(cmd: str, need=None):
    args = cmd.split(' ')
    if need and not args[0] == need:
        return False
    cmd = AVAILABLE_COMMANDS.get(args[0], [-1, None])
    para = tuple(args[1:])
    if cmd[0] == -1:
        raise Exception('Wrong Command')
    else:
        if cmd[0] == len(para):
            resp = cmd[1](*para)
            if args[0] == '/update':
                for i in range(len(resp)):
                    uid = resp[i]['from']
                    auth, nick = um.users['uid'][uid]['authority'], um.users['uid'][uid]['nickname']
                    resp[i]['from'] = '[{}]{}'.format(auth, nick)
                resp = str(json.dumps(resp, ensure_ascii=False))
            return resp
        else:
            raise Exception('Wrong Parameter')
