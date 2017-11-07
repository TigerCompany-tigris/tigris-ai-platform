# -*- coding: utf-8 -*-
from flask import render_template
from flask import request
from flask import url_for

import json
import requests

def init(app):
    app.add_url_rule('/web/', view_func=home, methods=['GET'], endpoint='web/home')
    app.add_url_rule('/web/topicWord/', view_func=topicWord, methods=['GET'], endpoint='web/topicWord')
    app.add_url_rule('/web/themeSentence/', view_func=themeSentence, methods=['GET',], endpoint='web/themeSentence')
    app.add_url_rule('/web/cloud/', view_func=cloud, methods=['GET'], endpoint='web/cloud')
    app.add_url_rule('/web/network/', view_func=network, methods=['GET'], endpoint='web/network')


def home():
    return render_template('layout.html')

def topicWord():
    return render_template('topicWord.html')

def themeSentence():
    return render_template('themeSentence.html')

def cloud():
    return render_template('cloud.html')

def network():
    return render_template('network.html')

