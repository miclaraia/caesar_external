

"""
Get classifications from Panoptes or SQS Queue
"""

from caesar_external.utils.caesar_utils import Client, SQSClient
from caesar_external.data import Config
import panoptes_client as pan
import logging

logger = logging.getLogger(__name__)


class Extractor(object):

    @classmethod
    def last_id(cls, next_id=None):
        if next_id is None:
            return Config.instance().last_id
        Config.instance().last_id = next_id

    @classmethod
    def next(cls):
        cl = None
        for cl in cls.get_classifications(cls.last_id()):
            yield cl
        if cl:
            cls.last_id(cl['id'])

    @classmethod
    def get_classifications(cls, last_id):
        if Config.instance().sqs_queue is not None:
            return SQSExtractor.get_classifications(last_id)
        else :
            return StandardExtractor.get_classifications(last_id)


class StandardExtractor(Extractor):

    @classmethod
    def get_classifications(cls, last_id):
        logger.debug('Getting classifications')
        project = Config.instance().project
        for c in Client.extract(project, last_id):
            cl = {
                'id': int(c.id),
                'subject': int(c.links.subjects[0].id),
                'project': int(c.links.project.id),
                'workflow': int(c.raw['links']['workflow']),
                'annotations': c.annotations,
            }

            if cl['workflow'] != Config.instance().workflow:
                continue

            if 'user' in c.raw['links']:
                cl.update({'user': c.raw['links']['user']})
            else:
                session = c.raw['metadata']['session'][:10]
                cl.update({'user': 'not-logged-in-%s' % session})

            yield cl


class SQSExtractor(Extractor):

    @classmethod
    def get_classifications(cls, last_id):
        # TODO: is there any way to use last_id?
        logger.debug('Getting classifications from SQS')
        project = Config.instance().project
        for c in SQSClient.extract(queue_url):
            cl = {
                'id': int(c['id']),
                'subject': int(c['subject_id']),
                'project': int(c['project_id']),
                'workflow': int(c['workflow_id']),
                'annotations': c['annotations'],
                'user': c['user']  # Assumes that extractor will handle user ID
            }

            # this should never happen unless multiple workflows share the same
            # queue
            if cl['workflow'] != Config.instance().workflow:
                continue

            yield cl
