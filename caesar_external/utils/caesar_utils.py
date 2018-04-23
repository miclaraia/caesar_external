
import panoptes_client as pan
from caesar_external.data import Config

import hashlib
import json

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

        return r


class SQSClient(Client):

    def __init__(self):
        # Create SQS client
        self.sqs = boto3.client('sqs')

    @classmethod
    def extract(cls, queue_url):
        return cls.instance().sqs_retrieve(queue_url)

    def sqs_retrieve(self, queue_url):
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp', 'MessageDeduplicationId'
            ],
            MaxNumberOfMessages=10,  # Allow up to 10 messages to be received
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,  # Allows the message to be retrieved again immediately
            WaitTimeSeconds=5  # Wait at most 5 seconds for an extract
        )

        receivedMessageIds = []
        recievedMessages = []

        # Loop over messages
        for message in response['Messages']:
            # extract message body expect a JSON formatted string
            # any information required to deduplicate the message should be
            # present in the message body
            messageBody = message['Body']
            receivedMessages = json.loads(messageBody)
            # verify message body integrity
            messageBodyMd5 = hashlib.md5(messageBody).digest()

            if messageBodyMd5 == message['MD5OfBody'] :
                # the message has been retrived successfully - delete it.
                self.sqs_delete(queue_url, message['ReceiptHandle'])

        return messages

    def sqs_delete(self, queue_url, receipt_handle):
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
