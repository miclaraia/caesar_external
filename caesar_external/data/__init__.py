

"""
Storage module to track which classification was gotten last
"""

import os
import json


class Config:
    _config = None

    def __init__(self, name, project, workflow, last_id, **kwargs):
        self.name = name
        self.project = project
        self.workflow = workflow
        self.last_id = last_id

        self._config = self

    def caesar_address(self):
        return 'https://caesar.zooniverse.org:443/workflows/%d' % self.workflow

    def save(self):
        with open(path(self.name), 'w') as fp:
            json.dump(self.__dict__, fp)

    @classmethod
    def load(cls, name):
        with open(path(name), 'r') as fp:
            data = json.load(fp)

        return cls(**data)
        


def dir():
    return os.path.abspath(os.path.dirname(__file__))


def path(fname):
    return os.path.join(dir(), fname)
