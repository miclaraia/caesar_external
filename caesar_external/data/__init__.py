

"""
Storage module to track which classification was gotten last
"""

import os
import json

import logging
logger = logging.getLogger(__name__)


class Config:
    _config = None

    def __init__(self, name, project, workflow, last_id, **kwargs):
        """
        Parameters
        ----------
        auth_mode: interactive, api_key, or environment
        """
        self.name = name
        self.project = project
        self.workflow = workflow
        self.last_id = last_id

        self.caesar_name = kwargs.get('caesar_name', 'ext')
        self.sqs_queue = kwargs.get('sqs_queue', None)
        self.staging_mode = kwargs.get('staging_mode', False)

        self.auth_mode = kwargs.get('auth_mode', 'interactive')
        self.client_id = kwargs.get('client_id', None)
        self.client_secret = kwargs.get('client_secret', None)

        self.__class__._config = self

    @classmethod
    def instance(cls):
        return cls._config

    @staticmethod
    def caesar_endpoint():
        if Config._config.staging_mode:
            return 'https://caesar-staging.zooniverse.org'
        return 'https://caesar.zooniverse.org'

    @staticmethod
    def login_endpoint():
        if Config.instance().staging_mode:
            return 'https://panoptes-staging.zooniverse.org'
        return 'https://panoptes.zooniverse.org'

    def workflow_path(self):
        return 'workflows/%d/subject_reductions/%s/reductions' % \
            (self.workflow, self.caesar_name)

    def save(self):
        fname = '%s.json' % self.name
        with open(path(fname), 'w') as fp:

            json.dump(self.dump(), fp)

    @classmethod
    def load(cls, name):
        fname = '%s.json' % name
        with open(path(fname), 'r') as fp:
            data = json.load(fp)

        print(data)

        return cls(**data)

    def dump(self):
        return self.__dict__.copy()

    def __str__(self):
        return str(self.dump())

    def __repr__(self):
        return str(self)

def dir():
    return os.path.abspath(os.path.dirname(__file__))


def path(fname):
    return os.path.join(dir(), fname)
