import json
from flask import Flask, request, jsonify
from datetime import datetime
import pathlib

app = Flask(__name__)

def PostFhirComposition(record):
    try:
        CompositionjsonPath=str(pathlib.Path().absolute()) + "/Composition_DischargeSummary135726.json"
        Compositionjson = json.load(open(CompositionjsonPath,encoding="utf-8"), strict=False)
        
        #PostjsonPath=str(pathlib.Path().absolute()) + "/G01526-FHIRDischargeSummary1080422.json"
        #Postjson = json.load(open(PostjsonPath,encoding="utf-8"), strict=False)
        Postjson = record
        
        Compositionjson['resourceType'] = 'Composition'
        Compositionjson['language'] = 'zh-TW'
        Compositionjson['text']['status'] = 'generated'
        Compositionjson['text']['div'] = '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + 'text' + '</div>'         
        Compositionjson['status'] = 'preliminary'
        Compositionjson['type'] = {"coding":[{"system":"http://loinc.org","code":"18842-5","display":"Discharge Summary"}]}
        
        datetime_object = datetime.strptime(Postjson[0]['CREATE_DATE']+Postjson[0]['CREATE_TIME'], '%Y%m%d%H%M')
        Compositionjson['date']=datetime_object.strftime("%Y-%m-%dT%H:%M:00")
        
        Compositionjson['subject']['reference'] = 'Patient/' + Postjson[0]['PAT_NO']
        Compositionjson['subject']['display'] = Postjson[0]['NAME']
        
        Compositionjson['encounter']['display'] = Postjson[0]['BED_NO']
        
        #Compositionjson['author'][0]['reference'] = 'Practitioner/' + PractitionerPut(xmldict['author']['assignedAuthor'])
        #Compositionjson['author'][0]['display'] = xmldict['author']['assignedAuthor']['assignedPerson']['name']
        Compositionjson['title'] = '出院病摘'
        Compositionjson['confidentiality'] = 'N'
        Compositionjson['attester'][0]['mode'] = 'professional'
        #date_object = datetime.strptime(xmldict['author']['time']['@value'], '%Y%m%d%H%M')
        #Compositionjson['attester'][0]['time'] = date_object.strftime("%Y-%m-%dT%H:%M:00")
        
        Compositionjson['custodian']['reference'] = 'Organization/' + Postjson[0]['Hospital_Id']
        Compositionjson['custodian']['display'] = Postjson[0]['Hospital_Name']
        
        Compositionjson['section']=[]
        #for i in range(len(xmldict['component']['structuredBody']['component'])):
        #    Compositionjson['section'].append(component2section(xmldict['component']['structuredBody']['component'][i]))
       # print(Compositionjson['section'][7])
        #url = fhir + 'Composition/'
        headers = {
          'Content-Type': 'application/json'
        }
        payload = json.dumps(Compositionjson)
        #response = requests.request("POST", url, headers=headers, data=payload)
        #print(response.status_code)
        return (Compositionjson)
    except:
        return ({'NG'})

@app.route('/', methods=['GET'])
def query_records():
    #record = json.loads(request.data)
    #print(name)
    '''with open('/tmp/data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for record in records:
            if record['name'] == name:
                return jsonify(record)'''
    return jsonify({'message': 'GET'}), 200

@app.route('/', methods=['POST'])
def create_record():
    #record = json.loads(request.data)
    record = json.loads(request.data, strict=False)
    Composition = PostFhirComposition(record)
    '''with open('/tmp/data.txt', 'r') as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        records.append(record)
    with open('/tmp/data.txt', 'w') as f:
        f.write(json.dumps(records, indent=2))'''
    return jsonify(Composition), 201

@app.route('/', methods=['PUT'])
def update_record():
    #dataString = request.data.decode('utf-8')
    #dataString = dataString.replace('\n','')
    #print(dataString)

    '''new_records = []
    with open('/tmp/data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
    for r in records:
        if r['name'] == record['name']:
            r['email'] = record['email']
        new_records.append(r)
    with open('/tmp/data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))'''
    return jsonify({'message': 'PUT'}), 200
    
    
@app.route('/', methods=['DELETE'])
def delte_record():
    #record = json.loads(request.data)
    '''new_records = []
    with open('/tmp/data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['name'] == record['name']:
                continue
            new_records.append(r)
    with open('/tmp/data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))'''
    return jsonify({'message': 'DELETE'}), 200


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8181, debug=True)