
import panoptes_client as pan
from caesar_external.data import Config


"""
Utils to interact with caesar...
"""


class Client:

    _client = None

    def __init__(self):
        self.pan = pan.Panoptes(login='interactive')

    @classmethod
    def client(cls):
        if cls._client is None:
            cls._client = cls()
        return cls._client

    @classmethod
    def get_classifications(cls, last_id):
        c = pan.Classification.where(scope='project', last_id=last_id)
        cl = c.raw.copy()
        cl['user'] = c.links.user.id
        cl['subject'] = c.links.subject.id
        cl['project'] = c.links.project.id
        cl['workflow'] = c.links.workflow.id

        return cl

    @classmethod
    def respond(cls, subject, data):
        """
        PUT subject score to Caesar
        """
        config = Config._config
        pan = cls._client.pan

        endpoint = config.caesar_address()
        path = 'workflow/%d/reducers/external/reductions' % config.workflow

        body = {
            'reduction': {
                'subject_id': subject,
                'data': data
            }
        }

        r = pan.put(endpoint=endpoint, path=path, json=body)
        logger.debug('done')

        return r
        




