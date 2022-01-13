from flask import Flask
from flask_restful import Resource, Api, reqparse
from importlib import import_module
import os

app = Flask(__name__)
api = Api(app)

#/latest?{source}
class latest(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True) #TODO: Global
        args = parser.parse_args()

        if type(args['source']) is None or args['source'] == 'global': 

            #mypath = os.path.dirname(os.path.abspath(__file__)) + '/sources'
            #onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
            
            #latest = list()
            #for i in onlyfiles:
            #   x = import_module(i.strip('.py'))
            #   latest.append({str(i.strip('.py')): x.fetch_latest()})
            #   #Pain Peko
            #return latest
            return None
        
        source = import_module('sources.' + str(args['source']))
        return source.fetch_latest()

#/popular?{source}
class popular(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True) #TODO: Global
        args = parser.parse_args()

        if type(args['source']) is None or args['source'] == 'global': 

            #mypath = os.path.dirname(os.path.abspath(__file__)) + '/sources'
            #onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
            
            #latest = list()
            #for i in onlyfiles:
            #   x = import_module(i.strip('.py'))
            #   latest.append({str(i.strip('.py')): x.fetch_latest()})
            #   #Pain Peko
            #return latest
            return None
        
        source = import_module('sources.' + str(args['source']))
        return source.fetch_popular()

#/search?source={source}&search={search}
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

#/manga?source={source}&slug={manga_slug}
class manga(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True)
        parser.add_argument('slug', type=str, required=True)
        args = parser.parse_args()

        source = import_module('sources.' + str(args['source']))
        return source.fetch_manga(str(args['slug']))

#/pages?search={source}&url={chapter_slug}
class pages(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        args = parser.parse_args()
        source = import_module('sources.' + str(args['source']))

        return source.fetch_pages(str(args['url']))

api.add_resource(latest, '/latest')
api.add_resource(popular, '/popular')
api.add_resource(search, '/search')
api.add_resource(manga, '/manga')
api.add_resource(pages, '/pages')


if __name__ == '__main__':
    app.run()