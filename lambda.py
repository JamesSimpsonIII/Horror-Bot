import json
import random
import requests

def random_num():
    return(random.randint(1, 1000))

def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']
    
def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }

def getMovie(intent_request):
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres=27"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMTE2NDUzYmNmYjNiNjk2ODQ1MTNkODk2NDM5ZjgyMyIsInN1YiI6IjY0OWY5YWUwODFkYTM5MDE0ZDQ5NDJlNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.dOU5FdfZ_2INIPH3Wioh6fsOH3j9tuSqCv_HTL95Lng"
    }
    
    session_attributes = get_session_attributes(intent_request)
    movieList = requests.get(url, headers=headers)
    movie = movieList["results"][random_num()]["title"]
    message = {
        'contentType': 'PlainText',
        'content': movie
    }
    fulfillment_state = "Fulfilled"
    return close(intent_request, session_attributes, fulfillment_state, message)


def dispatch(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']
    response = None
    # Dispatch to your bot's intent handlers
    if intent_name == 'GetMovie':
        return getMovie(intent_request)

def lambda_handler(event, context):
    response = dispatch(event)
    return response