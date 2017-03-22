"Talks to AWS"

import logging

import boto3

class Awsqueue(object):
    "Calling an aws queue"
    def __init__(self, queue_url):
        self.queue_url = queue_url
        self.logger = logging.getLogger(__name__)

    def get_messages(self):
        "Gets the next few messages"
        self.logger.info('Loading messages')
        try:
            sqs = boto3.resource('sqs')
            queue = sqs.Queue(self.queue_url)
            return queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=600)
        except boto3.exceptions.Boto3Error as awserror:
            self.logger.error(awserror)
            return []
