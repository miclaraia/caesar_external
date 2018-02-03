

"""
Get classifications from Panoptes
"""

from caesar_external.utils.caesar_utils import Client
from caesar_external.data import Config
import panoptes_client as pan


class Extractor:

    @classmethod
    def last_id(cls, next_id=None):
        if next_id is None:
            return Config.instance().last_id
        Config.instance().last_id = next_id

    @classmethod
    def get_classifications(cls, last_id):
        project = Config.instance().project
        data = []
        for c in Client.extract(project, last_id):
            cl = {
                'id': int(c.id),
                'subject': int(c.links.subjects[0].id),
                'project': int(c.links.project.id),
                'workflow': int(c.raw['links']['workflow']),
                'annotation': c.annotations,
            }

            if cl['workflow'] != Config.instance().workflow:
                continue

            if 'user' in c.raw['links']:
                user = pan.User.find(c.raw['links']['user'])
                cl.update({'user': int(user.id), 'username': user.login})
            else:
                session = c.raw['metadata']['session'][:10]
                cl.update({'user': 'not-logged-in-%s' % session})

            data.append(cl)

        return data

    @classmethod
    def next(cls):
        client = Client.client()
        data = client.get_classifications(cls.last_id())

        # for item in data:
            # yield item
        if len(data)>1:
            cls.last_id(data[-1]['id'])
        return data

