import requests
API_ENDPOINT = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
API_DEFAULT_PARAMS = {
    'continuous': True,
    'timestamps': True,
    'word_confidence': True,
    'profanity_filter': False,
    'word_alternatives_threshold': 0.4
}

API_DEFAULT_HEADERS = {
    'content-type': 'audio/wav'
}



def speech_to_text_api_call(audio_filename, username, password):
    with open(audio_filename, 'rb') as a_file:
        http_response = requests.post(API_ENDPOINT,
                      auth=(username, password),
                      data=a_file,
                      params=API_DEFAULT_PARAMS,
                      headers=API_DEFAULT_HEADERS,
                      stream=False)
        return http_response
