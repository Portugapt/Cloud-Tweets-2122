from flask import Flask, json

import functions_framework

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def _create_app():
    print('INFO: functions.clear_tweet_list.app.main._create_app')

    return Flask(__name__)

app = _create_app()


def _clear_tweets(tweet_list):
    results = []

    for row in tweet_list:
        new_id = row['id']
        new_text = row['text']
        new_user = row['user']

        results.append({'id': new_id, 'text': new_text, 'user': new_user})

    return results

@functions_framework.http
def clear_tweet_list(request):
    tweets_list = json.loads(request.form['tweets'])

    results = _clear_tweets(tweets_list)

    response = app.response_class(
        response=json.dumps(results),
        status=200,
        mimetype='application/json'
    )
    return response