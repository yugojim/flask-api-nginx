import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import Function

#fhir = 'http://104.208.68.39:8080/fhir/'#4600VM outside
#fhir = "http://61.67.8.220:8080/fhir/"#skh outside
#fhir = "http://10.200.251.72:8080/fhir/"#tpech inside
fhir = "http://106.105.181.72:8080/fhir/"#tpech outside


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

###serverstatus###
@app.route('/', methods=['GET'])
@cross_origin()
def serverstatus():
    return jsonify({'Server Status' : 'run'}), 200

###DischargeSummary###
@app.route('/', methods=['POST'])
@cross_origin()
def create_record():
    #record = json.loads(request.data)
    record = json.loads(request.data, strict=False)
    Composition, status_code = Function.PostFhirComposition(record)
    return jsonify(Composition), status_code

@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['GET'])
@cross_origin()
def query_DischargeSummaryID(DischargeSummary_Id):
    url = fhir + 'Composition/' + DischargeSummary_Id
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200
    
@app.route('/DischargeSummary/<string:DischargeSummary_Id>', methods=['DELETE'])
@cross_origin()
def delte_DischargeSummary(DischargeSummary_Id):
    url = fhir + 'Composition/' + DischargeSummary_Id
    response = requests.request("DELETE", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

###VisitNote###
@app.route('/VisitNote/', methods=['GET'])
@cross_origin()
def query_VisitNote():
    url = fhir + 'Composition?title=門診'
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200
    
@app.route('/VisitNote/<string:VisitNote_Id>', methods=['GET'])
@cross_origin()
def query_VisitNoteID(VisitNote_Id):
    url = fhir + 'Composition/' + VisitNote_Id
    response = requests.request("GET", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

@app.route('/VisitNote/', methods=['POST'])
@cross_origin()
def create_VisitNote():
    record = json.loads(request.data, strict=False)
    Composition, status_code = Function.PostVisitNote(record)
    return jsonify(Composition), status_code

@app.route('/VisitNote/<string:VisitNote_Id>', methods=['PUT'])
@cross_origin()
def update_VisitNote(VisitNote_Id):
    record = json.loads(request.data, strict=False)
    Composition, status_code = Function.PostVisitNote(record, VisitNote_Id)
    return jsonify(Composition), status_code    
    
@app.route('/VisitNote/<string:VisitNote_Id>', methods=['DELETE'])
@cross_origin()
def delte_VisitNote(VisitNote_Id):
    url = fhir + 'Composition/' + VisitNote_Id
    response = requests.request("DELETE", url, headers={}, data={}, verify=False)
    resultjson=json.loads(response.text)
    return jsonify(resultjson), 200

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8888, debug=True)