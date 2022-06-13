import re
import base64


def decode_to_base64(line):
    text = text = re.sub('\s+(?=<)', '', line)
    encode = base64.b64encode(bytes(text, "utf-8"))
    removeB = encode.decode()
    return removeB