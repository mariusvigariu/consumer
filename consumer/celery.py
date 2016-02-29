from __future__ import absolute_import

from celery import Celery

app = Celery('consumer',
             broker='amqp://guest@localhost//',
             backend='rpc://',   # send result back trough AMQP
             include=['consumer.tasks'])


class CeleryConfig(object):
    """
    Can also be kept in a file
    """
    CELERY_TASK_RESULT_EXPIRES = 3600
    CELERY_RDB_PORT = '9191'
    # ...


app.config_from_object(CeleryConfig)


if __name__ == '__main__':
    app.start()
