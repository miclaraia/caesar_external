
"""
Send Reductions to caesar
"""

from caesar_external.utils.caesar_utils import Client


class Reducer:

    @classmethod
    def reduce(cls, data):
        for subject, item in data:
            Client.reduce(subject, item)
