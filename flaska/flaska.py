import json
from flask import Flask, request, jsonify
from datetime import datetime
import pathlib

app = Flask(__name__)

def PostFhirComposition(record):
    try:
        CompositionjsonPath=str(pathlib.Path().absolute()) + "/Composition_DischargeSummary135726.json"
        Compositionjson = json.load(open(CompositionjsonPath,encoding="utf-8"), strict=False)
        
        Postjson = record
        
        Compositionjson['resourceType'] = 'Composition'
        Compositionjson['language'] = 'zh-TW'
        Compositionjson['text']['status'] = 'generated'
        text = '<table border="1"><caption>出院病摘單</caption><tr><th>身分證字號</th><th>病歷號</th><th>病人姓名</th><th>性別</th><th>出生日期</th><th>文件列印日期</th><th>醫師姓名</th><th>醫師記錄日期時間</th><th>醫院名稱</th><th>住院日期</th><th>出院日期</th><th>轉出醫事機構名稱</th><th>轉入醫事機構名稱</th></tr>'
        text = text + '<tr><td>' + Postjson[0]['ID_NUMBER'] + '</td><td>' + Postjson[0]['CHART_NO'] + '</td><td>' + Postjson[0]['NAME'] + '</td><td>' + Postjson[0]['GENDER'] + '</td><td>' + Postjson[0]['BIRTH_DATE'] + '</td><td>' + Postjson[0]['CREATE_DATE'] + '</td><td>' + Postjson[0]['PHYSICIAN_NAME'] + '</td><td>' + Postjson[0]['CREATE_DATE'] + '</td><td>' + Postjson[0]['Hospital_Name'] + '</td><td>'\
            + Postjson[0]['DATE_OF_HOSPITALIZATION'] + '</td><td>' + Postjson[0]['DISCHARGE_DATE'] + '</td><td>' + Postjson[0]['Receiving_hospital_name'] + '</td><td>' + Postjson[0]['Receiving_hospital_name'] + '</td><td>' + Postjson[0]['REFERRING_HOSPITAL_NAME'] + '</td></tr></table>'
        Compositionjson['text']['div'] = '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + text + '</div>'         
        Compositionjson['status'] = 'preliminary'
        Compositionjson['type'] = {"coding":[{"system":"http://loinc.org","code":"18842-5","display":"Discharge Summary"}]}
        
        datetime_object = datetime.strptime(Postjson[0]['CREATE_DATE']+Postjson[0]['CREATE_TIME'], '%Y%m%d%H%M')
        Compositionjson['date']=datetime_object.strftime("%Y-%m-%dT%H:%M:00")
        
        ##Compositionjson['subject']['reference'] = 'Patient/' + Postjson[0]['PAT_NO']
        Compositionjson['subject']['display'] = Postjson[0]['NAME']
        
        Compositionjson['encounter']['display'] = Postjson[0]['BED_NO']
        
        ##Compositionjson['author'][0]['reference'] = 'Practitioner/' + PractitionerPut(xmldict['author']['assignedAuthor'])
        Compositionjson['author'][0]['display'] = Postjson[0]['PHYSICIAN_NAME']
        Compositionjson['title'] = '出院病摘'
        Compositionjson['confidentiality'] = 'N'
        Compositionjson['attester'][0]['mode'] = 'professional'
        #date_object = datetime.strptime(xmldict['author']['time']['@value'], '%Y%m%d%H%M')
        #Compositionjson['attester'][0]['time'] = date_object.strftime("%Y-%m-%dT%H:%M:00")
        
        ##Compositionjson['custodian']['reference'] = 'Organization/' + Postjson[0]['Hospital_Id']
        Compositionjson['custodian']['display'] = Postjson[0]['Hospital_Name']

        IMPRESSION_CONTENTS ={
            "title": "住院臆斷",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "46241-6",
                        "display": "Hospital admission diagnosis Narrative - Reported"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>住院臆斷:</b></tr><tr>" + Postjson[0]['IMPRESSION_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }
        Compositionjson['section'].append(IMPRESSION_CONTENTS)
        
        DISCHARGE_DIAGNOSIS_CONTENTS = {
            "title": "出院診斷",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "11535-2",
                        "display": "Hospital discharge Dx Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>出院診斷:</b></tr><tr>" + Postjson[0]['IMPRESSION_CONTENTS'].replace('&','') + "</tr></table></div>"
            },
            "entry": [
                {
                    "reference": "",
					"display": Postjson[0]['IMPRESSION_CONTENTS'].replace('&','')
                }
            ]
        }
        Compositionjson['section'].append(DISCHARGE_DIAGNOSIS_CONTENTS)
        
        CANCER_STAGING_CONTENTS = {
            "title": "癌症期別",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "22037-6",
                        "display": "Staging Cancer Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>癌症期別:</b></tr><tr>" + Postjson[0]['CANCER_STAGING_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }        
        Compositionjson['section'].append(CANCER_STAGING_CONTENTS)
        
        CHIEF_COMPLAINT_CONTENTS = {
            "title": "主訴",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "10154-3",
                        "display": "Chief complaint Narrative - Reported"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>主訴:</b></tr><tr>" + Postjson[0]['CHIEF_COMPLAINT_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }       
        Compositionjson['section'].append(CHIEF_COMPLAINT_CONTENTS)
        
        PRESENT_ILLNESS_CONTENTS = {
            "title": "病史",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "10164-2",
                        "display": "History of Present illness Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>病史:</b></tr><tr>" + Postjson[0]['PRESENT_ILLNESS_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }      
        Compositionjson['section'].append(PRESENT_ILLNESS_CONTENTS)
        
        FAMILY_TREE_CONTENTS = {
            "title": "家族圖譜",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "74027-4",
                        "display": "Family pedigree identifier"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>家族圖譜:</b></tr><tr>" + Postjson[0]['FAMILY_TREE_CONTENTS'].replace('&','') + "</tr></table></div>"
            },
            "entry": [
                {
                    "reference": "",
                    "display": Postjson[0]['FAMILY_TREE_CONTENTS'].replace('&','')
                }
            ]
        } 
        Compositionjson['section'].append(FAMILY_TREE_CONTENTS)
        
        PHYSICAL_EXAMINATION_CONTENTS = {
            "title": "理學檢查發現",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "10184-0",
                        "display": "Hospital discharge physical findings Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>理學檢查發現:</b></tr><tr>" + Postjson[0]['PHYSICAL_EXAMINATION_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }
        Compositionjson['section'].append(PHYSICAL_EXAMINATION_CONTENTS)
        
        SPECIFIC_EXAMINATION_CONTENTS = {
            "title": "檢驗及特殊檢查",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "11493-4",
                        "display": "Hospital discharge studies summary Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>檢驗:</b></tr><tr>" + Postjson[0]['LABORATORY_DATA_CONTENTS'].replace('&','') + "</tr></table><br/><table><tr><b>特殊檢查:</b></tr><tr>" + Postjson[0]['SPECIFIC_EXAMINATION_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }
        Compositionjson['section'].append(SPECIFIC_EXAMINATION_CONTENTS)
        
        IMAGING_STUDY_CONTENTS = {
            "title": "醫療影像檢查",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "19005-8",
                        "display": "Radiology Imaging study [Impression] (narrative)"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>醫療影像檢查:</b></tr><tr>" + Postjson[0]['IMAGING_STUDY_CONTENTS'].replace('&','') + "</tr></table></div>"
            },
            "entry": [
                {
                    "reference": "",
                    "display": Postjson[0]['IMAGING_STUDY_CONTENTS'].replace('&','')
                }
            ]
        }
        Compositionjson['section'].append(IMAGING_STUDY_CONTENTS)
        
        PATHOLOGY_REPORT_CONTENTS = {
            "title": "病理報告",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "22034-3",
                        "display": "Pathology report Cancer Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>病理報告:</b></tr><tr>" + Postjson[0]['PATHOLOGY_REPORT_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }
        Compositionjson['section'].append(PATHOLOGY_REPORT_CONTENTS)
        
        SURGICAL_METHOD_AND_FINDING_CONTENTS = {
            "title": "手術日期及方法",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8724-7",
                        "display": "Surgical operation note description Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>手術日期及方法:</b></tr><tr>" + Postjson[0]['SURGICAL_METHOD_AND_FINDING_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }
        Compositionjson['section'].append(SURGICAL_METHOD_AND_FINDING_CONTENTS)
        
        HOSPITAL_COURSE_CONTENTS = {
            "title": "住院治療經過",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8648-8",
                        "display": "Hospital course Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>住院治療經過:</b></tr><tr>" + Postjson[0]['HOSPITAL_COURSE_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }
        Compositionjson['section'].append(HOSPITAL_COURSE_CONTENTS)
        
        COMORBIDITES_CONTENTS = {
            "title": "合併症與併發症",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "55109-3",
                        "display": "Complications Document"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>合併症與併發症:</b></tr><tr>" + Postjson[0]['HOSPITAL_COURSE_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }
        Compositionjson['section'].append(COMORBIDITES_CONTENTS)
        
        INSTRUCTIONS_ON_DISCHARGE_CONTENTS = {
            "title": "出院指示",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "8653-8",
                        "display": "Hospital Discharge instructions"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>出院指示:</b></tr><tr>" + Postjson[0]['INSTRUCTIONS_ON_DISCHARGE_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }
        Compositionjson['section'].append(INSTRUCTIONS_ON_DISCHARGE_CONTENTS)
        
        DISCHARGE_STATUS_CONTENTS = {
            "title": "出院狀況",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "42345-9",
                        "display": "Discharge functional status (narrative)"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>出院狀況:</b></tr><tr>" + Postjson[0]['DISCHARGE_STATUS_CONTENTS'].replace('&','') + "</tr></table></div>"
            }
        }
        Compositionjson['section'].append(DISCHARGE_STATUS_CONTENTS)
        
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