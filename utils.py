#!/usr/bin/env python
# -*- coding:utf-8 -*-
import codecs
import os
# python 3
try:
    import ConfigParser as cp
except Exception:
    import configparser as cp


class VicConfigParser():
    def __init__(self, filename):
        # self.filename = os.path.join(sys.path[0]+filename)
        self.filename = filename
        self.configparser = cp.ConfigParser()
        self._read()

    def set(self, name, value=None, section='DEFAULT'):
        if section != 'DEFAULT':
            if section not in self.configparser.sections():
                self.configparser.add_section(section)
        self.configparser.set(section=section, option=name, value=value)
        self._save()

    def get(self, name, section='DEFAULT'):
        try:
            return self.configparser.get(section=section, option=name)
        except cp.NoOptionError:
            return None

    def delkey(self, name, section='DEFAULT'):
        self.configparser.remove_option(section=section, option=name)
        self._save()

    def delsection(self, section='DEFAULT'):
        self.configparser.remove_section(section=section)
        self._save()

    def sections(self):
        return self.configparser.sections()

    def keys(self, section='DEFAULT'):
        return self.configparser.options(section)

    def _read(self):
        if os.path.exists(self.filename):
            self.configparser.readfp(codecs.open(self.filename,
                                                 "r", "utf-8"))

    def _save(self):
        with codecs.open(self.filename, "w", "utf-8") as f:
            self.configparser.write(f)
