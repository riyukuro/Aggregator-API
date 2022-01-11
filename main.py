from ast import parse
from typing_extensions import Required
from flask import Flask
from flask_restful import Resource, Api, reqparse
from importlib import import_module

#from os import listdir
import os

# /search/{source}/{search}

# /chapters/{source}/{manga_url}
## /manga/{source}/{manga_url}

# /pages/{source}/{chapter_url}

### No arg = Global/all
# /latest/{source}
# /popular/{source}

app = Flask(__name__)
api = Api(app)

class latest(Resource):
    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('source', type=str, required=True) #TODO: Global

        args = parser.parse_args()
        if type(args['source']) is None or args['source'] == 'global': 

            mypath = os.path.dirname(os.path.abspath(__file__)) + '/sources'
            onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
            
            latest = list()
            for i in onlyfiles:
               x = import_module(i.strip('.py'))
               latest.append({str(i.strip('.py')): x.fetch_latest()})
               #Pain Peko
            return latest
        
        source = import_module('sources.' + str(args['source']))
        return source.fetch_latest()

class manga(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        args = parser.parse_args()

        source = import_module('sources.' + str(args['source']))
        return source.fetch_manga(str(args['url']))

class pages(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        args = parser.parse_args()
        source = import_module('sources.' + str(args['source']))

        return source.fetch_pages(str(args['url']))

class search(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True) #TODO: Global
        parser.add_argument('search', type=str, required=True)
        args = parser.parse_args()

        if type(args['source']) is None or args['source'] == 'global':
            return None
            #PainPeko

        source = import_module('sources.' + str(args['source']))
        return source.fetch_search(args['search'])


api.add_resource(latest, '/latest')
api.add_resource(manga, '/manga')
api.add_resource(pages, '/pages')
api.add_resource(search, '/search')


if __name__ == '__main__':
    app.run()