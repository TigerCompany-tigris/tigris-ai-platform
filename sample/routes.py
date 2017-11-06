# -*- coding: utf-8 -*-
from flask import render_template
from flask import request
from flask import url_for

import json
import requests

def init(app):
    app.add_url_rule('/web/', view_func=home, methods=['GET'], endpoint='web/home')
    app.add_url_rule('/web/topicWord/', view_func=topicWord, methods=['GET', 'POST'], endpoint='web/topicWord')
    app.add_url_rule('/web/themeSentence/', view_func=themeSentence, methods=['GET', 'POST'], endpoint='web/themeSentence')
    app.add_url_rule('/web/cloud/', view_func=cloud, methods=['GET'], endpoint='web/cloud')
    app.add_url_rule('/web/network/', view_func=network, methods=['GET'], endpoint='web/network')


def home():
    return render_template('layout.html')

def topicWord():
    if request.method == 'GET':
        return render_template('topicWord.html')
    elif request.method == 'POST':
        corpus = request.form['corpus']
        result_count = request.form['result_count']

        params = {
            'text': corpus,
            'result_count': result_count
        }

        r = requests.post(url_for('searchtopic', _method='POST', _external=True), params=params, timeout=60)
        data = json.loads(r.text)
        r.close()

        data['corpus'] = corpus
        data['result_count'] = result_count

        return render_template('topicWord.html', **data)


def themeSentence():
    if request.method == 'GET':
        return render_template('themeSentence.html')
    elif request.method == 'POST':
        corpus = request.form['corpus']
        result_count = request.form['result_count']

        params = {
            'corpus': corpus,
            'result_count': result_count
        }

        r = requests.post(url_for('themesentence', _method='POST', _external=True), params=params, timeout=60)
        data = json.loads(r.text)
        r.close()

        data = {
            'sentences': data,
            'corpus': corpus,
            'result_count': result_count
        }

        return render_template('themeSentence.html', **data)


def cloud():
    return render_template('cloud.html')

def network():
    return render_template('network.html')

