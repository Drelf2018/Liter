MAGIC = [20210318223204031831, 1145141919810]
BASE58 = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'


def encode(msg: str) -> str:
    temp = 0
    for m in msg:
        temp = temp * 256 + ord(m)
    temp = (temp ^ MAGIC[0]) + MAGIC[1]
    msg = ''
    while temp:
        msg = BASE58[temp % 58] + msg
        temp //= 58
    return msg


def decode(msg: str) -> str:
    temp = 0
    for m in msg:
        temp = temp * 58 + BASE58.index(m)
    temp = temp - MAGIC[1] ^ MAGIC[0]
    msg = ''
    while temp:
        msg = chr(temp % 256) + msg
        temp //= 256
    return msg


if __name__ == '__main__':
    print(encode('1145141919'))
