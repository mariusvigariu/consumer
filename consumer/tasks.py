from __future__ import absolute_import

from celery.contrib import rdb

from consumer.celery import app


@app.task
def handle_request(*args, **kwargs):
    """
    Entry point for all requests coming from publishers
    """
    # some logic here to dispatch it further for
        # parsing sms text
        # checking permissions
        # return proper handler

    # we can set breakpoints for debugging with celery's rdb
    # rdb.set_trace()

    return 'Args: {}\nKwargs: {}'.format(args, kwargs)
