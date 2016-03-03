ONEm core platform POC. RabbitMQ and Celery approach.
---

Steps to get started:
---

1. Install pip dependencies: 
    `pip install -r requirements.pip`

2. Install rabbitmq server:
    `sudo apt-get install rabbitmq-server` (if on Debian)
    `https://www.rabbitmq.com/download.html` (otherwise)

3. Run celery in foreground:
    `celery worker --app=consumer --loglevel=info`

4. Publish a message as a 3rd party publisher - pika client:
    `python publish.py`

5. Publish a message as Celery publiser:
    `python celery_publish.py`


Useful links:
---
Basics of RabbitMQ:
https://www.rabbitmq.com/getstarted.html

Basics of Celery:
http://docs.celeryproject.org/en/latest/getting-started/index.html

Celery best practices:
https://denibertovic.com/posts/celery-best-practices/

Celery autoreload on any change:
http://stackoverflow.com/questions/21666229/celery-auto-reload-on-any-changes
