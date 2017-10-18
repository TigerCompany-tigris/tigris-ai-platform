# -*- coding: utf-8 -*-
import importlib
import traceback
from time import strftime
from xml.etree import ElementTree

from flask import Flask, request
from flask_restful import Api

from interface import BaseApi as ba
from util.data_handler import *

app = Flask(__name__)
api = Api(app)

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.teardown_appcontext
def teardown_appcontext(Exception):
    pass

@app.errorhandler(Exception)
def exceptions(e):
    print(e)
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    app.logger.error('!%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                 ts,
                 request.remote_addr,
                 request.method,
                 request.scheme,
                 request.full_path,
                 tb)

    return "Internal Server Error", 500

def main():
    extends = []
    reduces = []

    # db_path = 'db/word_fliter.db'
    #
    # if os.path.isfile(db_path):
    #     db = sqlite3.connect(db_path)
    #
    #     with db:
    #         localCursor = db.cursor()
    #         localCursor.execute("select real_text, text from extend_words order by length(tag) desc, tag")
    #         extends = [{'real_tag': r[0], 'tag': r[1]} for r in localCursor.fetchall()]
    #
    #         localCursor.execute("select tag from reduce_words")
    #         reduces = [r[0] for r in localCursor.fetchall()]

    config = ElementTree.parse('properties/config.xml')

    nlpprop = config.find('nlp-function')
    mod = importlib.import_module(nlpprop.attrib['package-path'])
    nlp = getattr(mod, nlpprop.attrib['function-name'])

    setattr(ba, 'set_nlp', nlp)

    dataprop = config.findall('data-handler/*')

    for prop in dataprop:
        attr = prop.attrib
        print(prop.tag)

        mod = importlib.import_module(attr['package-path'])
        cls = getattr(mod, attr['package-name'])

        setattr(ba, prop.tag, cls)

    apiprop = config.findall('api/class')

    for prop in apiprop:
        attr = prop.attrib
        mod = importlib.import_module(attr['package-path'])
        cls = getattr(mod, attr['class-name'])

        api.add_resource(cls, attr['url'])

if __name__ == '__main__':
    main()

    app.run(host='0.0.0.0', port=7777, debug=True)
