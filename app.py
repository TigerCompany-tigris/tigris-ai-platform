# -*- coding: utf-8 -*-
import importlib
import traceback
from time import strftime
from xml.etree import ElementTree

from flask import Flask, request
from flask_restful import Api

from interface import BaseApi
from interface.DataApi import DataApi

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
    config = ElementTree.parse('properties/config.xml')

    nlp_prop = config.find('nlp-handler')
    mod = importlib.import_module(nlp_prop.attrib['package-path'])
    nlp = getattr(mod, nlp_prop.attrib['method-name'])
    setattr(BaseApi, 'nlp', nlp)

    data_prop = config.findall('data-handler/*')
    dataApi = DataApi()
    for prop in data_prop:
        attr = prop.attrib
        mod = importlib.import_module(attr['package-path'])
        cls = getattr(mod, attr['class-name'])

        setattr(dataApi, prop.tag, cls)
    setattr(BaseApi, 'dataApi', dataApi)

    api_prop = config.findall('api-handler/*')

    for prop in api_prop:
        attr = prop.attrib
        parameters = {}
        for params in prop.findall('params'):
            paramList = []
            for param in params.findall('param'):
                paramList.append(param.attrib)
            parameters[params.attrib['type']] = paramList

        mod = importlib.import_module(attr['package-path'])
        cls = getattr(mod, attr['class-name'])
        api.add_resource(cls, attr['service-url'], endpoint=attr['endpoint'], resource_class_kwargs={'parameters': parameters})


if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=7777, debug=True)
