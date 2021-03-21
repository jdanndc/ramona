from os import walk
from os.path import isfile, join, relpath
import re


class Library(object):
    def __init__(self):
        self.dirs = []
        self.files = []
        self.blacklist = ['.DS_Store']

    def file_test(self, dir, f):
        ret = False
        if isfile(join(dir, f)):
            if f not in self.blacklist:
                ret = True
        return ret

    def pushdir(self, dir):
        self.dirs.append(dir)
        for (dirpath, dirnames, filenames) in walk(dir):
            rel = relpath(dirpath, dir)
            for fn in filenames:
                if self.file_test(dirpath, fn):
                   self.files.append({'basedir': dir, 'dir': rel, 'name': join(rel, fn), 'fname': fn, 'path': join(dirpath, fn), 'loaded': False, 'checked': False})
        return self

    def list(self):
        out = []
        for i, f in enumerate(self.files):
            loaded = '*' if f['loaded'] else ' '
            update = ' ' if not f['checked'] else '-' if f['loaded'] else '+'
            out.append(f"{loaded}[{update}] [{i}] {f['name']}")
        return out

    def toggle(self, i):
        if 0 <= i < len(self.files):
            self.files[i]['checked'] = not self.files[i]['checked']

    def check(self, i):
        if i > 0 and i < len(self.files):
            self.files[i]['checked'] = True

    def check_all(self):
        for d in self.files:
            d['checked'] = True

    def check_none(self):
        for d in self.files:
            d['checked'] = False

    def check_by_re(self, regex):
        p = re.compile(regex)
        for d in self.files:
            d['checked'] = p.match(d['name'])

    def reset(self):
        for d in self.files:
            d['loaded'] = False
            d['checked'] = False


