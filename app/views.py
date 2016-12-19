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
    return render_template('visionapi.html', request = 'visionapi')

@app.route('/speechapi', methods=['GET','POST'])
def speechapi():
    return render_template('speechapi.html', request = 'speechapi')
