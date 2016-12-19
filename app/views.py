from . import app
from flask import render_template, session, redirect, url_for, request, abort
import requests, base64, json
from . import key, translate, languages

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

    selected_lang = request.form.get('language') or 'Español'
    #We generate the result of this API in the processed_picture data structure
    processed_picture = None
    image = request.files.get('visionapi_image')
    #print(image)
    if image is not None:
        imagestream = image.read()
        imagestream64 = base64.b64encode(imagestream).decode('utf-8')
        json_req = {'requests':[{'image':{'content':imagestream64},\
                    'features':[{'type':'LABEL_DETECTION','maxResults':10}, \
                                {'type':'TEXT_DETECTION'}
                                ]}]}
        r = requests.post(vision_url+'?key='+key, data = json.dumps(json_req))
        response = json.loads(r.text)
        #LABEL_DETECTION. Always exists.
        labelsList = response['responses'][0]["labelAnnotations"]
        #We translate the text labels:
        textList = [ label['description'] for label in labelsList ]
        scoreList = [ label['score'] for label in labelsList ]
        translatedTextList = translate(textList, 'en', languages[selected_lang])
        translatedLabelsList = list(zip(translatedTextList, scoreList))
        #TEXT_DETECTION. May not exist.
        #If it detects text, use the Translate API
        textList = response['responses'][0].get("textAnnotations")

        inputTextList = None
        translatedTextList = None
        if textList is not None :
            inputTextList = textList[0]['description'].split('\n')
            translatedTextList = translate(inputTextList, textList[0]['locale'], languages[selected_lang])



        processed_picture = dict(image = imagestream64, labelsList = translatedLabelsList, \
                                inputTextList = inputTextList, translatedTextList = translatedTextList)



    return render_template('visionapi.html', selected_lang = selected_lang, \
    languages = list(languages.keys()), processed_picture = processed_picture, \
    request='visionapi')

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
    input_selected_lang = request.form.get('inputlanguage') or 'Español'
    output_selected_lang = request.form.get('targetlanguage') or 'Español'
    #We generate the result of this API in the processed_audio data structure
    processed_audio = None
    audio = request.files.get('speechapi_audio')
    #print(image)
    if audio is not None:
        fileext = audio.filename[audio.filename.rfind('.')+1:]
        if fileext == 'wav':
            encoding = 'LINEAR16'
            sampleRate = 16000
        else:
            #Bad file format
            return abort(400, 'Formato de audio no soportado.')

        audiostream = audio.read()
        audiostream64 = base64.b64encode(audiostream).decode('utf-8')

        json_req = {'config': {'encoding':encoding,'sampleRate':sampleRate,'languageCode':'es'},'audio': {'content': audiostream64}}
        r = requests.post(speech_url+'?key='+key, data = json.dumps(json_req))
        response = json.loads(r.text)
        inputText = [text['transcript'] for text in response['results'][0]['alternatives']]
        #Now we translate the text
        translatedText = translate(inputText, languages[input_selected_lang], languages[output_selected_lang])
        processed_audio = dict(audio = audiostream64, fileext = fileext, \
                            inputText = inputText, translatedText = translatedText)

    return render_template('speechapi.html', input_selected_lang = input_selected_lang, \
                            output_selected_lang = output_selected_lang,\
                            languages = list(languages.keys()), processed_audio = processed_audio, \
                            request='speechapi')
