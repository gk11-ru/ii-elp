# -*- coding: utf-8 -*-

import api
from api import sx, flt
import points
import rssg
import os
import random
from api.bottle import route, post, redirect, request, response, static_file, local, template


def allstart():
    ip=request.headers.get('X-Real-Ip') or request.environ.get('REMOTE_ADDR')
    local.r = sx.mydict(ua=request.headers.get('User-Agent'), ip=ip, kuk=sx.mydict(request.cookies), fz=sx.mydict(request.POST), getl=sx.mydict(request.GET))
    local.r.auth = local.r.kuk.auth


def _msg(o, ml):
    allstart()
    if o == 'msg':
        mo = api.get_msg(ml) + {'msgid':ml}
        local.r.page_title =  mo.subj + ' @ ' + mo.echoarea
        lst = [mo]
    elif o == 'lst':
        lst=[api.get_msg(n) + {'msgid':n} for n in ml.split('/')]
        local.r.page_title = u'Список сообщений'
    return template('iitpl/msg.html', lst=[mo] if o != 'lst' else lst, r=local.r)


@route('/')
def start_page():
    allstart()
    cfg = api.load_echo(True)
    if local.r.kuk.myel:
        myel = [e for e in local.r.kuk.myel.splitlines() if flt.echo_flt(e)]
    else:
        myel = []
    if not myel:
        myel = cfg[1:]
    else:
        myel = api.separate_myel(myel, cfg[1:])
        #print myel
    lst=[(e, api.get_echoarea_f(e)) for e, c, d in myel]
    local.r.page_title = u'ii : всё для хорошего общения'
    return template('iitpl/index.html', r=local.r, lst=lst)


@route('/reg')
def hash_reg():
    return u'Введите желаемое имя: <form method="post" action="/reg"><input type="text" name="user" /> <input type="submit"></form>'


@post('/reg')
def reg_it():
    user = request.POST['user']
    phash = points.sha(user + str(random.randint(1, 99999999)))
    points.save_point(phash, user)
    return 'Регистрация завершена, запомните вашу строку доступа<br /><strong>%s</strong><br /><br /><a href="/h/savehash/%s">автологин</a>' % (phash, phash)


@route('/rss/<echo>.<year>')
@route('/rss/<echo>.<year>/<num:int>')
def rss_echo(echo, year, num=50):
    cfg = api.load_echo(True)
    response.set_header('content-type', 'application/rss+xml; charset=utf-8')
    return rssg.gen_rss('%s.%s' % (echo, year), cfg[0][0], num)


@route('/reply/<ea>/<repto>')
def index_list(ea, repto):
    allstart()
    cfg = api.load_echo()
    local.r.NODE = cfg[0][1]
    if repto and repto != '-': 
        local.r.repto = repto
        local.r.rmsg = api.get_msg(repto)
    if not flt.echo_flt(ea): return ea
    local.r.page_title = u'message to ' + ea
    return template('iitpl/mform.html', r=local.r, ea=ea)


@route('/<echo>.<year>')
def index_list(echo, year):
    allstart()
    ea = '%s.%s' % (echo, year)
    if not flt.echo_flt(ea): return ea
    cfg = api.load_echo(True)
    local.r.update(page_title=ea, echolist=cfg[1:], ea=ea)
    return template('iitpl/echoarea.html', r=local.r, j=api.get_echoarea_f(ea))


@post('/a/savemsg/<ea>')
def msg_post(ea):
    allstart(); fz = local.r.fz
    cfg = api.load_echo(False)
    ufor = request.forms.msgfrom.encode('utf-8')
    if not flt.echo_flt(ea): return ea
    if not fz.msg or not fz.subj: return 'empty msg or subj'
    uname, uaddr = points.check_hash(ufor)
    if uaddr:
        mo = sx.mydict()
        for _ in ('subj', 'msg', 'repto'):
            mo[_] = fz[_].decode('utf-8')
        mo['msgfrom'] = uname
        mo['msg']=mo['msg'].replace('\r\n', '\n')
        mo['date'] = str(sx.gts())
        mo.update(addr='%s, %s' % (cfg[0][1], uaddr), msgto=request.forms.msgto, echoarea=ea)
        api.savemsg(mo)
    else:
        return 'no auth'
    if ufor != local.r.auth:
        response.set_cookie('auth', ufor, path='/', max_age=7776000)
        return('<html><head><meta http-equiv="refresh" content="0; /%s" /></head><body></body></html>' % ea)
    else:
        redirect('/%s' % ea)


@post('/a/myel')
@route('/a/myel/<eset:path>')
def save_myel(eset=''):
    elist = eset or request.forms.myel.replace('\r\n', '\n')
    response.set_cookie('myel', elist.replace('/', '\n') , path='/', max_age=7776000)
    return('<html><head><meta http-equiv="refresh" content="0; /" /></head><body></body></html>')


@route('/h/savehash/<h>')
@route('/h/logout')
def cookie_page(h=''):
    allstart()
    response.set_cookie('auth', h, path='/', max_age=7776000)
    return('<html><head><meta http-equiv="refresh" content="0; /" /></head><body></body></html>')


@route('/h/showhash')
def show_my_hash():
    allstart()
    return local.r.auth


@route('/h/<page>')
def show_custom_page(page):
    allstart()
    return template('iitpl/%s.pge' % page, r=local.r)


@route('/<p:re:s|e|m>/<filename:path>')
def new_style(p,filename):
    return static_file(filename, root='%s/%s' % (II_PATH,p))


@route('/q/<msglst:path>')
def msg_qpage(msglst):
    return _msg('lst', msglst)


@route('/<msghash:re:[^/]{20}>')
def msg_page(msghash):
    return _msg('msg', msghash)


@route('/<msghash:re:[A-Za-z0-9]{6}>')
def msg_page_short(msghash):
    lst = os.listdir('m')
    msglst = [x for x in lst if x.startswith(msghash)]
    return _msg('msg', '/'.join(msglst))
