from flask import Flask, render_template, request

import requests
import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def dict_page():
    return render_template('dict.html')


@app.route('/translate', methods=['GET', 'POST'])
def index_post():

    langFrom = request.form['langFrom']
    langTo = request.form['langTo']
    original_text = request.form['word']
    print(original_text)

    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    path = '/translate?api-version=3.0&'

    target_language_parameter = 'from=' + langFrom + '&to=' + langTo

    constructed_url = endpoint + path + target_language_parameter

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }


    body = [{'text': original_text}]

    translator_request = requests.post(
        constructed_url, headers=headers, json=body)

    translator_response = translator_request.json()
    translated_text = translator_response[0]['translations'][0]['text']

    return render_template(
        'result.html',
        word=translated_text
    )

if __name__ == '__main__':
    app.run()