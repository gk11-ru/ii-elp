import os

msgs = os.listdir('m')
for h in msgs:
    if os.path.getsize('m/%s' % h) == 0:
        os.remove('m/%s' % h)
        msgs.remove(h)

echoes = os.listdir('e')

for ea in echoes:
    passed = []
    echo = open('e/%s' % ea).read().splitlines()
    for h in echo:
        if h in msgs:
            msgs.remove(h)
            passed.append(h)
    if passed != echo:
        open('e/%s' % ea,'w').write('\n'.join(passed + ['']))

for h in msgs:
    os.remove('m/%s' % h)
