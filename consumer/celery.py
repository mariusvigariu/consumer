from __future__ import absolute_import

from celery import Celery
from celery import bootsteps
from kombu import Consumer, Exchange, Queue

my_queue = Queue('myq', Exchange('myq'), 'myq-route')

app = Celery('consumer',
             broker='amqp://guest@localhost//',
             backend='rpc://',   # send result back trough AMQP
             include=['consumer.tasks'])



# http://celery.readthedocs.org/en/latest/userguide/extending.html
class MyConsumerStep(bootsteps.ConsumerStep):
    """
    Custom consumer so Celery can accept custom message formats.
    """
    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[my_queue],
                         callbacks=[self.handle_message],
                         #on_message=self.on_message,
                         accept=['json'])]

    def handle_message(self, body, message):
        print('Received message: {0!r}'.format(body))
        message.ack()

    # def on_message(self, message):
    #     payload = message.decode()
    #     from celery.contrib import rdb
    #     rdb.set_trace()
    #     print 'Received message: {0!r} {props!r} rawlen={s} msg={m}'.format(
    #         payload, props=message.properties, s=len(message.body),
    #         m=type(message)
    #     )
    #     # message.ack()

app.steps['consumer'].add(MyConsumerStep)


class CeleryConfig(object):
    """
    Can also be kept in a file
    """
    CELERY_TASK_RESULT_EXPIRES = 3600
    CELERY_RDB_PORT = 9191
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    # ...
    # CELERY_ROUTES = {
    #     'consumer.tasks.handle_request': {'queue': 'myq'},
    # }


app.config_from_object(CeleryConfig)

if __name__ == '__main__':
    app.start()
