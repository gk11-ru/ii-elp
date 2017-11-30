# -*- coding: utf-8 -*-

import api
import points
import os
from api import sx
from api.bottle import request, response, route, post, run, TEMPLATE_PATH


II_PATH = os.path.dirname(__file__) or '.'
TEMPLATE_PATH.insert(0, II_PATH)


@route('/list.txt')
def list_txt():
    response.set_header('content-type', 'text/plain; charset=utf-8')
    lst = api.load_echo(False)[1:]
    if request.query.el:
        el = request.query.el.split('/')
        descs = dict([(a, c.decode('utf-8')) for a, b, c in lst])
        lst = [(x, api.echoarea_count(x), descs[x] if x in descs else '') for x in el]
    if request.query.n:
        return '\n'.join([t[0] for t in lst])
    elif request.query.h:
        return '\n'.join(['%s:%s:hsh/%s' % (t[0], t[1], sx.hsh(api.get_echoarea(t[0], True))) for t in lst])
    else:
        return '\n'.join(['%s:%s:%s' % t for t in lst])


@route('/blacklist.txt')
def blacklist_txt():
    response.set_header('content-type', 'text/plain; charset=utf-8')
    return api.ru('blacklist.txt')


@route('/u/m/<h:path>')
def jt_outmsg(h):
    response.set_header('content-type', 'text/plain; charset=iso-8859-1')
    lst = [x for x in h.split('/') if len(x) == 20 or len(x) == 8]
    return '\n'.join([api.mk_jt(x, api.raw_msg(x)) for x in lst])


@route('/u/e/<names:path>')
def index_list(names):
    response.set_header('content-type', 'text/plain; charset=utf-8')
    return api.echoareas(names.split('/'), request.query.sf)


def _point_msg(pauth, tmsg):
    msgfrom, addr = points.check_hash(pauth)
    if not addr: return 'auth error!'
    cfg = api.load_echo(False)
    mo = api.toss(msgfrom, '%s, %s' % (cfg[0][1], addr), tmsg.strip())
    if mo.msg.startswith('@repto:'):
        tmpmsg = mo.msg.splitlines()
        mo.repto = tmpmsg[0][7:]
        mo.msg = '\n'.join(tmpmsg[1:])
    if len(mo.msg.encode('utf-8')) < 64100:
        h = api.point_newmsg(mo)
        if h:
            return 'msg ok:%s: <a href="/%s">%s</a>' % (h, mo.echoarea, mo.echoarea)
        else:
            return 'error:unknown'
    else:
        return 'msg big!'


@route('/u/point/<pauth>/<tmsg:path>')
def point_msg_get(pauth, tmsg):
    return _point_msg(pauth, tmsg)


@post('/u/point')
def point_msg_post():
    return _point_msg(request.POST['pauth'], request.POST['tmsg'])


import iitpl
iitpl.II_PATH = II_PATH


run(host='0.0.0.0', port=62220, debug=False)
