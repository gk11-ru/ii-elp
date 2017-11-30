import os

msgs = os.listdir('m')
passed = set()

echoes = os.listdir('e')

for ea in echoes:
    for h in open('e/%s' % ea).read().splitlines():
        if h in msgs:
            msgs.remove(h)
            passed.add(h)
        else:
            if h in passed:
                print 'double in %s: %s' % (ea, h)
            else:
                print 'bad record in %s: "%s"' % (ea, h)

for h in msgs:
    print 'no owner for %s' % h
