import os
import cPickle


FIXTURE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')

HANDLERS = {
        '.pyon': eval,
        '.mustache': lambda x: x.decode('utf-8'),
        '.pickle': cPickle.loads,
        }


def read_fixture(name):
    for extension, filter in HANDLERS.items():
        if name.endswith(extension):
            break
    else:
        filter = lambda x: x

    filename = os.path.join(FIXTURE_DIR, name)
    fp = open(filename)
    try:
        return filter(fp.read())
    finally:
        fp.close()
