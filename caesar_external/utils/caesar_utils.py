
import panoptes_client as pan
from caesar_external.data import Config

import logging
logger = logging.getLogger(__name__)

"""
Utils to interact with caesar...
"""


class Client:

    _instance = None

    def __init__(self):
        self.pan = pan.Panoptes(login='interactive')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def extract(cls, project, last_id):
        print(last_id)
        cls.instance()
        kwargs = {
            'scope': 'project',
            'project_id': project,
        }
        if last_id:
            kwargs.update({'last_id': last_id})
        print(kwargs)
        return pan.Classification.where(**kwargs)

    @classmethod
    def reduce(cls, subject, data):
        """
        PUT subject score to Caesar
        """
        config = Config._config
        pan = cls.instance().pan

        endpoint = config.caesar_endpoint()
        path = config.workflow_path()

        body = {
            'reduction': {
                'subject_id': subject,
                'data': data
            }
        }

        r = pan.put(endpoint=endpoint, path=path, json=body)
        logger.debug('done')

        return r
        




