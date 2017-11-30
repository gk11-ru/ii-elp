import re


def echo_flt(ea):
    rr = re.compile(r'^[a-z0-9_!.-]{3,120}')
    if rr.match(ea) and '.' in ea:
        return True


def msg_flt(msgid):
    rr = re.compile(r'^[a-z0-9A-Z]{8,20}$')
    if rr.match(msgid):
        return True
