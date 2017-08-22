from flask import Blueprint, jsonify, request
from webargs import fields
from webargs.flaskparser import use_args
from parser.helper.mentions import Mentions
from parser.helper.emoticons import Emoticons
from parser.helper.links import Links
from parser.helper import stats
from injector import inject
from webargs import core

api_blueprint = Blueprint('api', __name__)


@api_blueprint.before_app_request
def before_request():
    """
    Executes before every requests.
    We can add statistics here Eg: Total no of requests
    We could also log requests object for development purpose.
    """
    stats.add_request(request)


@api_blueprint.errorhandler(422)
def handle_error(err):
    """
    Webargs library returns an Html page with the error message.
    We are overriding it to return a json error response.
    """
    return jsonify(err.data), 422


@inject
@api_blueprint.route('/parse-message')
@use_args({'input': fields.Str(required=True)})
def parseMessage(args, m: Mentions, e: Emoticons, l: Links):
    """
    Get endpoint that parse the given string and returns
    Mentions, Emoticons and Links.

    Input:
            input (str) input string to be parsed

    Returns:
    HTTP 200 OK with a json response.
        Eg: http://127.0.0.1:5000/api/v1/parse-message?input=Hello%20@atlassian,%20please%20check%20http://www.google.com%20(smile)
        Response:
        {
            "emoticons": [
                    "smile"
                ],
            "links": [
                {
                        "link": "http://www.google.com",
                        "title": "Google"
                }
            ],
            "mentions": [
                "atlassian"
            ]
        }

    HTTP 422 UNPROCESSABLE ENTITY, with json error response
        Eg: http://127.0.0.1:5000/api/v1/parse-message
        Response:
        {
            "messages":	{
                "input": [
                    "Missing data for required field."
                ]
            }
        }
    """
    input_str = args['input']
    response = {}

    mentions = m.getMentions(input_str)
    if mentions:
        response['mentions'] = mentions

    emoticons = e.getEmoticons(input_str)
    if emoticons:
        response['emoticons'] = emoticons

    links = l.getLinks(input_str)
    if links:
        response['links'] = links
    return jsonify(response)


@api_blueprint.route('/stats')
def get_stats():
    """
    Endpoint to display the statistics about the applications.
    Current just returns the all the request to the server
    and the totalRequestCount.
    Examples Response:
    {
        "requests": [
            {
                "path": "/api/v1/parse-message",
                "queryParameters": {
                    "input": "Hello @atlassian"
                }
            },
            {
                "path": "/api/v1/stats",
                "queryParameters": {}
            }
        ],
        "totalRequestCount": 2
    }
    """
    response = {}
    response['totalRequestCount'] = len(stats.request_stats)
    response['requests'] = stats.request_stats
    return jsonify(response)
