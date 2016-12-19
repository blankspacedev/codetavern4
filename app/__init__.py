from flask import Flask
from flask_script import Manager
from flask_bootstrap import Bootstrap
import requests, base64, json

languages = {'Español':'es','English':'en','French':'fr','Chinese':'zh-CN','Gujarati':'gu'}

key = ''
translate_url = 'https://translation.googleapis.com/language/translate/v2'

def translate(textList, langInput, langOutput):
    '''
    -translate API-
    post request:
        requests.post(translate_api_url, data = dict(key = key, source = inputLang,
                                            target = outputLang, q = list of texts))
    '''
    #If the language to translate is the same we do nothing
    if langInput == langOutput:
        return textList

    r = requests.post(translate_url, data = dict(key = key, source = langInput, \
                                                target = langOutput, q = textList))
    response = json.loads(r.text)
    translatedObject = response['data']["translations"]

    return [ text['translatedText'] for text in translatedObject ]

app = Flask(__name__)
app.config['DEBUG']=True

manager = Manager(app)
bootstrap = Bootstrap(app)

from .views import *
