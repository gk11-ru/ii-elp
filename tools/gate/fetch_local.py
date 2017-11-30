# -*- coding: utf-8 -*-

import sys, os, shutil

INDIR=sys.argv[1]
OUTDIR=sys.argv[2]
ECHOES=sys.argv[3:]

def get_echoarea(lpath,name):
    try: return open(os.path.join(lpath,'e/%s' % name)).read().splitlines()
    except: return []

def mk_echo_file(lpath,f):
    return os.path.join(lpath,'e/%s' % f)

def mk_msg_file(lpath,f):
    return os.path.join(lpath,'m/%s' % f)

def parse():
    for ea in ECHOES:
        print ea
        el = get_echoarea(INDIR,ea)
        myel = set(get_echoarea(OUTDIR,ea))
        dllist = [x for x in el if x not in myel]
        for dl in dllist:
            print dl
            shutil.copy2(mk_msg_file(INDIR,dl),mk_msg_file(OUTDIR,dl))
            open(mk_echo_file(OUTDIR,ea),'a').write(dl + '\n')

parse()
