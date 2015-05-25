#!flask/bin/python
"""
scaffold for API endpoint. Browse to localhost:5000/api/test to view.
"""
from flask import Flask, jsonify, render_template, url_for, request
from flask import abort
import requests
from SPARQLWrapper import SPARQLWrapper, RDF, JSON
import json

app = Flask(__name__)

REPOSITORY = 'http://localhost:8080/openrdf-sesame/repositories/AR-AI'

connections = [
    {
        'id': 1,
        'endpoint': u'2067e12fc5b99516e4971cfbdacfe75e',
    },
    {
        'id': 2,
        'endpoint': u'206dc79b92758760bd6df5c476796729',
    }
]



@app.route('/')
def first_page():
    app.logger.debug('You arrived at ' + url_for('first_page'))
    return render_template('LOD_Identity_Home.html')


def get_similar(uri):
    app.logger.debug('You arrived at /get_similar')
    app.logger.debug('I received the following uri: ' +  uri)
    
    query = "select ?p where {" + uri + " <http://www.w3.org/2002/07/owl#sameAs> ?p}"
    endpoint = REPOSITORY
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    
    #initialize dict to return counted results
    to_return = {}

    sparql.setReturnFormat(JSON)
    app.logger.debug('Query:\n{}'.format(query))        

    try :
        response = sparql.query().convert()
        app.logger.debug('Results were returned')
        app.logger.debug(response)
      
        for item in response['results']['bindings']:
            if item['p']['value'] in to_return:
                to_return[item['p']['value']] +=1
            else:
                to_return[item['p']['value']] = 1
            
            
    except Exception as e:
        app.logger.error('Something went wrong')
        app.logger.error(e)
        return jsonify({'result': 'Error'})
            
        
    else :
        return jsonify(to_return)
    
@app.route('/api/identity', methods=['GET'])
def return_similar_api():
    return get_similar(str(request.args.get("uri",None)))
    

'''    
@app.route('/api/<path:uri>', methods=['GET'])
def get_task(uri):
    if len(uri) == 0:
        abort(404)
    return jsonify({'connections': connections})
'''

if __name__ == '__main__':
    app.run(debug=True)
