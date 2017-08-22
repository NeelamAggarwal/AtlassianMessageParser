from flask import current_app

# Use a list to buffer all request time
# This is just to demostrate, not scalable
"""
Using a list to store all request received by the
applications. This is to server the '/stats' endpoint.
Currently, just storing request path and query parameter.
We can expand this to return other stats like response time,
other api used, etc.
"""
request_stats = []


def add_request(request):
    """
    Adds request path and query parameter to request stats list.
    Params:
            request (Request): request object from flask framework
    """
    response = {}
    response['path'] = request.path
    response['queryParameters'] = request.args
    request_stats.append(response)
