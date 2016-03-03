#!/usr/bin/env python
import json
import pika
import sys
import time
import uuid


class Publisher(object):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()

        # declare an exclusive queue for replies
        result = self.channel.queue_declare(exclusive=True)

        self.callback_queue = result.method.queue

        # subscribe to the callback queue so we can receive responses
        self.channel.basic_consume(
            self.on_response,
            no_ack=True,
            queue=self.callback_queue
        )

    def on_response(self, channel, method, props, body):
        """
        Checks for every response message if the correlation_id is the one we
        are looking for. If so, it stores the response into self
        """
        if self.corr_id == props.correlation_id:
            #import ipdb ; ipdb.set_trace()
            self.response = body

    def call(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # create the message payload as accepted by celery
        # http://docs.celeryproject.org/en/latest/internals/protocol.html#example-message
        payload = {
            'id': self.corr_id,
            'task': 'consumer.tasks.handle_request',
            'args': self._args,
            'kwargs': self._kwargs,
            'retries': 0,
        }
        self.channel.basic_publish(
            exchange='celery',  # send to celery exchange
            routing_key='celery',  # to this binding
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                content_type='application/json',
                correlation_id=self.corr_id,
                reply_to=self.callback_queue,
                delivery_mode=2, # make message persistent
            )
        )
        print " [x] Sent %r" % payload
        print " [x] Waiting for response ... task / correlation id: %s" % self.corr_id

        while self.response is None:
            self.connection.process_data_events()

        print " [x] Got response %s" % self.response

        return self.response


if __name__ == '__main__':

    s = time.time()

    args = sys.argv[1:] or ('some', 'default', 'args')

    publisher = Publisher(*args)
    publisher.call()

    e = time.time()

    print 'Time elapsed %.5f' % (e-s)
