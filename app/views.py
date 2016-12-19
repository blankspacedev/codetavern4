from . import app
from flask import render_template, session, redirect, url_for, request, abort
import requests, base64, json

vision_url = 'https://vision.googleapis.com/v1/images:annotate'
speech_url = "https://speech.googleapis.com/v1beta1/speech:syncrecognize"


@app.route('/', methods=['GET','POST'])
def init():
    return redirect(url_for('visionapi'))

@app.route('/visionapi', methods=['GET','POST'])
def visionapi():
    '''
    json request:
    {'requests':[{'image':{'content':data stream},
                  'features':[{'type':'LABEL_DETECTION','maxResults': N},
                                {'type':'TEXT_DETECTION'}]
                 }]}
    '''
    '''
    post request:
        requests.post(vision_api_url+'?key='+key, data = json.dumps(json request))
    '''

    return render_template('visionapi.html', request = 'visionapi')

@app.route('/speechapi', methods=['GET','POST'])
def speechapi():
    '''
    json request:
    {'config': {'encoding': encoding, 'sampleRate':sampleRate, 'languageCode': LANG},
                'audio': {'content': data stream}}
    '''
    '''
    post request:
        requests.post(speech_api_url+'?key='+key, data = json.dumps(json request))
    '''
    return render_template('speechapi.html', request = 'speechapi')

'''
-translate API-
post request:
    requests.post(translate_api_url, data = dict(key = key, source = inputLang,
                                        target = outputLang, q = list of texts))
'''
