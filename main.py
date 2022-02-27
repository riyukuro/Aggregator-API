from flask import Flask, send_file
from flask_restful import Resource, Api, reqparse
from server import server_import
import os
from requests import get
from io import BytesIO


app = Flask(__name__)
api = Api(app)

#/latest?source={source}
class latest(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True) #TODO: Global
        args = parser.parse_args()

        if args['source'] == 'global': return get_global('latest')
        
        source = server_import(str(args['source']))
        return {'data': source.fetch_latest()}

#/popular?source={source}
class popular(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True) #TODO: Global
        args = parser.parse_args()

        if args['source'] == 'global': return get_global('popular')
        
        source = server_import(str(args['source']))
        return {'data': source.fetch_popular()}

#/search?source={source}&search={search}
class search(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True) #TODO: Global
        parser.add_argument('search', type=str, required=True)
        args = parser.parse_args()

        if args['source'] == 'global': return get_global('search', args['search'])

        source = server_import(str(args['source']))
        return {'data': source.fetch_search(args['search'])}

#/manga?source={source}&slug={manga_slug}
class manga(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True)
        parser.add_argument('slug', type=str, required=True)
        args = parser.parse_args()

        source = server_import(str(args['source']))
        return source.fetch_manga(str(args['slug']))

#/pages?source={source}&slug={chapter_slug}
class pages(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('source', type=str, required=True)
        parser.add_argument('slug', type=str, required=True)
        args = parser.parse_args()

        source = server_import(str(args['source']))
        return {'isPaged': source.isPaged, 'pages': source.fetch_pages(str(args['slug']))}

#/page?source={source}&slug={page_slug}
@app.route('/page', methods=['GET'])
def page():
    parser = reqparse.RequestParser()
    parser.add_argument('source', required=True)
    parser.add_argument('slug', required=True)
    args = parser.parse_args()

    source = server_import(str(args['source']))
    if source.isPaged is False: return {'Error': 'This source is not paged.'}
    return send_file(
        BytesIO(get(source.fetch_page(str(args['slug'].rstrip('.png')))).content),
        mimetype='image/png',
        as_attachment=False
        )

class sources(Resource):
    def get(self):
        mypath = os.path.dirname(os.path.abspath(__file__)) + '/sources'
        return {'sources': [f.strip('.py') for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]}

def get_global(*argv):
    mypath = os.path.dirname(os.path.abspath(__file__)) + '/sources'
    source_list = [f.strip('.py') for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    data = []
    for i in source_list:
        x = server_import(i)
        if argv[0] == 'popular': 
            for i in x.fetch_popular():
                if i['manga_title'] not in [y['manga_title'] for y in data]:
                    data.append(i)
        elif argv[0] == 'latest': 
            for i in x.fetch_latest():
                if i['manga_title'] not in [y['manga_title'] for y in data]:
                    data.append(i)
        else: 
            for i in x.fetch_search(argv[1]):
                if i['manga_title'] not in [y['manga_title'] for y in data]:
                    data.append(i)

    return {'data': data}

api.add_resource(latest, '/latest')
api.add_resource(popular, '/popular')
api.add_resource(search, '/search')
api.add_resource(manga, '/manga')
api.add_resource(pages, '/pages')
api.add_resource(sources, '/sources')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    