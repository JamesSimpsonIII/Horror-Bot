import json
import random
import requests
import os

def random_num():
    return(random.randint(1, 8))

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
    session_attributes = get_session_attributes(intent_request)
    token = os.environ['token']
    baseUrl = "http://image.tmdb.org/t/p/"
    movieURL = "https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres=27"
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer {}".format(token)
    }
    
    randInt = random_num()
    movieList = requests.get(movieURL, headers=headers)
    data = movieList.json()
    title = data["results"][randInt]["title"]
    descr = data["results"][randInt]["overview"]
    
    imageSize = "w300"
    imagePath = data["results"][randInt]["backdrop_path"]

    message = {
        'contentType': 'ImageResponseCard',
        'content': "{} \n {}".format(title,descr),
        "imageResponseCard": {
                "title": title,
                "subtitle": descr[:245] + "...",
                "imageUrl": "{}{}{}".format(baseUrl,imageSize,imagePath)
        }      
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