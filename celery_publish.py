#!/usr/bin/env python
import sys

from consumer.tasks import handle_request

result = handle_request.delay(' '.join(sys.argv[1:]) or "Hello World!")

print result.get()
