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


@app.route('/')
def first_page():
    app.logger.debug('You arrived at ' + url_for('first_page'))
    return render_template('LOD_Identity_Home.html')

def get_similar(uri):
    app.logger.debug('You arrived at /get_similar')
    app.logger.debug('I received the following uri: ' +  uri)
    
    query = "select ?p ?o where {{ " + uri + "<http://www.w3.org/2002/07/owl#sameAs> ?p} union { graph ?o {" + uri + " <http://www.w3.org/2002/07/owl#sameAs> ?p}}}"
    endpoint = REPOSITORY
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    
    #initialize dict to return counted results
    to_return_implicit = {}
    to_return_explicit = {}
    to_return = {}

    sparql.setReturnFormat(JSON)
    app.logger.debug('Query:\n{}'.format(query))        

    try :
        response = sparql.query().convert()
        app.logger.debug('Results were returned')
        app.logger.debug("response: " + str(response))
        
        #construct dictionary from explicit and implicit statements with count
        for item in response['results']['bindings']:
            if 'o' not in item:
                if item['p']['value'] in to_return_implicit:
                    to_return_implicit[item['p']['value']] +=1
                else:
                    to_return_implicit[item['p']['value']] = 1
                #number_of_implicit -=1
            elif 'o' in item:
                if item['p']['value'] in to_return_explicit:
                    to_return_explicit[item['p']['value']] +=1
                else:
                    to_return_explicit[item['p']['value']] = 1
        
        app.logger.debug("explicit: " + str(to_return_explicit))
        
        #removing explicit from implicit
        for element in to_return_explicit.keys():
            if element in to_return_implicit:
                app.logger.debug("element: " + str(element))
                to_return_implicit[element] -= to_return_explicit[element]
        
        #removing empty keys
        for element in to_return_implicit.keys():
            if to_return_implicit[element] < 1:
                del to_return_implicit[element]
        
        app.logger.debug("implicit: " + str(to_return_implicit))
        
        #make sure no empty dictionaries are returned
        if len(to_return_implicit) > 0:
            to_return['implicit'] = to_return_implicit
        if len(to_return_explicit) > 0:
            to_return['explicit'] = to_return_explicit
        
            
    except Exception as e:
        app.logger.error('Something went wrong')
        app.logger.error(e)
        return jsonify({'result': 'Error'})
            
        
    else :
        return jsonify(to_return)
    
@app.route('/api/identity', methods=['GET'])
def return_similar_api():
    return get_similar(str(request.args.get("uri",None)))

@app.route('/api/compare', methods=['GET'])
def compare_uris():
    
    app.logger.debug("you arrived at 'compare uris'")
    uri1 = str(request.args.get("uri1", None))
    uri2 = str(request.args.get("uri2", None))
    
    
    query = "select ?p where {{ " + uri1 + " <http://www.w3.org/2002/07/owl#sameAs> " + uri2 + "} union {GRAPH ?p {" + uri1 + " <http://www.w3.org/2002/07/owl#sameAs> " + uri2 + "}}}"
    app.logger.debug('Query:\n{}'.format(query)) 
    endpoint = REPOSITORY
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    uris = {}
    i = 1
    count_explicit = 0
        
    try :
        response = sparql.query().convert()
        
        app.logger.debug("response: " + str(response))
        
        #first add all explicit
        for item in response['results']['bindings']:
            if item != {}:
                uris[i] = item['p']['value']
                count_explicit +=1
                i+=1
        
        #then add total - implicit
        for item in response['results']['bindings']:
            if item =={}:
                if count_explicit < 1:
                    uris[i] = 'implicit'
                    i +=1
                else:
                    count_explicit -=1
        
        
        app.logger.debug("results = " + str(uris))
        
        
    except Exception as e:
        app.logger.error('Something went wrong')
        app.logger.error(e)
        return jsonify({'result': 'Error'})
    else:
        return jsonify(uris)
    

'''    
@app.route('/api/<path:uri>', methods=['GET'])
def get_task(uri):
    if len(uri) == 0:
        abort(404)
    return jsonify({'connections': connections})
'''

if __name__ == '__main__':
    app.run(debug=True)
