import json
from datetime import datetime
import pathlib
import requests

#fhir = 'http://104.208.68.39:8080/fhir/'#4600VM outside
#fhir = "http://61.67.8.220:8080/fhir/"#skh outside
fhir = "http://10.200.251.72:8080/fhir/"#tpech inside
#fhir = "http://106.105.181.72:8080/fhir/"#tpech outside

def PostFhirComposition(record):
    try:
        CompositionjsonPath=str(pathlib.Path().absolute()) + "/Composition.json"
        Compositionjson = json.load(open(CompositionjsonPath,encoding="utf-8"), strict=False)
        
        Postjson = record
        #print(Postjson)
        Compositionjson['resourceType'] = 'Composition'
        Compositionjson['language'] = 'zh-TW'
        Compositionjson['text']['status'] = 'generated'
        text = '<table border="1"><caption>出院病摘單</caption><tr><th>身分證字號</th><th>病歷號</th><th>病人姓名</th><th>性別</th><th>出生日期</th><th>文件列印日期</th><th>醫師姓名</th><th>醫師記錄日期時間</th><th>醫院名稱</th><th>住院日期</th><th>出院日期</th><th>轉出醫事機構名稱</th><th>轉入醫事機構名稱</th></tr>'
        text = text + '<tr><td>' + Postjson[0]['ID_NUMBER'] + '</td><td>' + Postjson[0]['CHART_NO'] + '</td><td>' + Postjson[0]['NAME'] + '</td><td>' + Postjson[0]['GENDER'] + '</td><td>' + Postjson[0]['BIRTH_DATE'] + '</td><td>' + Postjson[0]['CREATE_DATE'] + '</td><td>' + Postjson[0]['PHYSICIAN_NAME'] + '</td><td>' + Postjson[0]['CREATE_DATE'] + '</td><td>' + Postjson[0]['Hospital_Name'] + '</td><td>'\
            + Postjson[0]['DATE_OF_HOSPITALIZATION'] + '</td><td>' + Postjson[0]['DISCHARGE_DATE'] + '</td><td>' + Postjson[0]['Receiving_hospital_name'] + '</td><td>' + Postjson[0]['REFERRING_HOSPITAL_NAME'] + '</td></tr></table>'
        Compositionjson['text']['div'] = '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + text + '</div>'         
        Compositionjson['status'] = 'preliminary'
        Compositionjson['type'] = {"coding":[{"system":"http://loinc.org","code":"18842-5","display":"Discharge Summary"}]}
        #print(Compositionjson)
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
        
        url = fhir + 'Composition/'
        headers = {
          'Content-Type': 'application/json'
        }
        payload = json.dumps(Compositionjson)
        response = requests.request("POST", url, headers=headers, data=payload)
        resultjson=json.loads(response.text)
        #print(response.status_code)
        return (resultjson, response.status_code)
    except:
        return ({'NG'})

def PostVisitNote(record):
    try:
        CompositionjsonPath=str(pathlib.Path().absolute()) + "/Composition.json"
        Compositionjson = json.load(open(CompositionjsonPath,encoding="utf-8"), strict=False)
        
        Postjson = record
        #print(Postjson)
        Compositionjson['resourceType'] = 'Composition'
        Compositionjson['language'] = 'zh-TW'
        Compositionjson['text']['status'] = 'generated'
        text = '<table><caption>門診病歷</caption><tr><th>身分證字號</th><th>病歷號</th><th>病人姓名</th><th>性別</th><th>出生日期</th><th>文件列印日期</th><th>醫師姓名</th><th>醫師記錄日期時間</th><th>醫院名稱</th><th>科別</th><th>門診日期</th></tr>'
        text = text + '<tr><td>' + Postjson['SOA'][0]['PERSONAL_ID'] + '</td><td>' + Postjson['SOA'][0]['CHART_NO'] + '</td><td>' + Postjson['SOA'][0]['NAME'] + '</td><td>' + Postjson['SOA'][0]['GENDER'] + '</td><td>' + Postjson['SOA'][0]['BIRTH_DATE']\
            + '</td><td>' + Postjson['SOA'][0]['DATE'] + '</td><td>' + Postjson['SOA'][0]['PHYSICIAN_NAME'] + '</td><td>'\
                + Postjson['SOA'][0]['TIME'] + '</td><td>' + Postjson['SOA'][0]['HOSPITAL_NAME'] + '</td><td>'  \
                    + Postjson['SOA'][0]['DEPARTMENT'] + '</td><td>' + Postjson['SOA'][0]['OPD_DATE']  + '</td></tr></table>'
        Compositionjson['text']['div'] = '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + text + '</div>'   
        Compositionjson['status'] = 'preliminary'
        Compositionjson['type'] = {"coding":[{"system":"http://loinc.org","code":"28579-1","display":"Visit note"}]}
        #print(Compositionjson)
        
        #datetime_object = datetime.strptime(Postjson[0]['CREATE_DATE']+Postjson[0]['CREATE_TIME'], '%Y%m%d%H%M')
        #Compositionjson['date']=datetime_object.strftime("%Y-%m-%dT%H:%M:00")
        Compositionjson['date']=Postjson['SOA'][0]['DATE']
        
        ##Compositionjson['subject']['reference'] = 'Patient/' + Postjson[0]['PAT_NO']
        Compositionjson['subject']['display'] = Postjson['SOA'][0]['NAME']
        
        Compositionjson['encounter']['display'] = Postjson['SOA'][0]['CHART_NO']
        
        ##Compositionjson['author'][0]['reference'] = 'Practitioner/' + PractitionerPut(xmldict['author']['assignedAuthor'])
        Compositionjson['author'][0]['display'] = Postjson['SOA'][0]['PHYSICIAN_NAME']
        Compositionjson['title'] = '門診病歷'
        Compositionjson['confidentiality'] = 'N'
        Compositionjson['attester'][0]['mode'] = 'professional'
        #date_object = datetime.strptime(xmldict['author']['time']['@value'], '%Y%m%d%H%M')
        #Compositionjson['attester'][0]['time'] = date_object.strftime("%Y-%m-%dT%H:%M:00")
        
        ##Compositionjson['custodian']['reference'] = 'Organization/' + Postjson[0]['Hospital_Id']
        Compositionjson['custodian']['display'] = Postjson['SOA'][0]['HOSPITAL_NAME']
        
        LAB_CONTENTS ={
            "title": "實驗室檢查紀錄",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "19146-0",
                        "display": "Reference lab test results"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr>實驗室檢查紀錄:\t病人血型及D抗原性:\t</tr><tr>" + Postjson['SOA'][0]['BLOOD_TYPE'] + "\t" + Postjson['SOA'][0]['RH_TYPE'] + "</tr></table></div>"
            },
            "entry": [
                {
                    #reference": "https://fhirtest.uhn.ca/baseR4/Observation/127858",
                    "display": Postjson['SOA'][0]['BLOOD_TYPE']
                },
                {
                    #"reference": "https://fhirtest.uhn.ca/baseR4/Observation/127859",
                    "display": Postjson['SOA'][0]['RH_TYPE']
                }
            ]
        }
        Compositionjson['section'].append(LAB_CONTENTS)
        
        MAJOR_ILLNESS = {
            "title": "重大傷病",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "11338-1",
                        "display": "History of major illnesses and injuries"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>重大傷病\t</b></tr><tr>" + str(Postjson['MAJOR_ILLNESS']) + "</tr></table></div>"
            },
            "entry": [
                {
                    "reference": "",
					"display": str(Postjson['MAJOR_ILLNESS'])
                }
            ]
        }
        Compositionjson['section'].append(MAJOR_ILLNESS)
        
        HISTORY_OF_ALLERGIES = {
            "title": "過敏史",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "10155-0",
                        "display": "History of allergies, reported"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr><b>過敏史\t</b></tr><tr>" + str(Postjson['HISTORY_OF_ALLERGIES']) + "</tr></table></div>"
            }
        }        
        Compositionjson['section'].append(HISTORY_OF_ALLERGIES)
        
        SOA = {
            "title": "病人生活史",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "29762-2",
                        "display": "Social history Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr>病人生活史\t</tr></table></div>"
            },
            "section": [
                {
                    "title": "就診年齡",
                    "code": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "29553-5",
                                "display": "Age calculated"
                            }
                        ]
                    },
                    "text": {
                        "status": "generated",
                        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><table><tr>就診年齡\t" + str(Postjson['SOA'][0]['AGE']) + "</tr></table></div>"
                    }
                },
                {
                    "title": "職業",
                    "code": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "21847-9",
                                "display": "Usual occupation Narrative"
                            }
                        ]
                    },
                    "text": {
                        "status": "generated",
                        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><table><tr>職業\t" + Postjson['SOA'][0]['OCCUPATION'] + "</tr></table></div>"
                    }
                },
                {
                    "title": "就醫身分別",
                    "code": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "63513-6",
                                "display": "Are you covered by health insurance or some other kind of health care plan"
                            }
                        ]
                    },
                    "text": {
                        "status": "generated",
                        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><table><tr>就醫身分別\t" + Postjson['SOA'][0]['IDENTITY_TYPE'] + "</tr></table></div>"
                    }
                }
            ]
        }       
        Compositionjson['section'].append(SOA)
        
        diagnosis = {
            "title": "診斷",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "29548-5",
                        "display": "Diagnosis Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr>診斷\t</tr><tr>" + str(Postjson['SOA'][0]['ICD_CODE'])\
                    + "</tr><tr>" + str(Postjson['SOA'][0]['ICD_NAME']) + "</tr><tr>" + str(Postjson['SOA'][0]['NOTE']) +"</tr></table></div>"
            },
            "entry": [
                {
                    "display": Postjson['SOA'][0]['ICD_NAME']
                }
            ]
        }      
        Compositionjson['section'].append(diagnosis)
        
        conditions = {
            "title": "病情摘要",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "19824-2",
                        "display": "Return visit conditions"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><br/><table><tr>主觀描述、客觀描述及評估</tr></table></div>"
            },
            "section": [
                {
                    "title": "主觀描述",
                    "code": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "61150-9",
                                "display": "Subjective Narrative"
                            }
                        ]
                    },
                    "text": {
                        "status": "generated",
                        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><table><tr>主觀描述\t</tr><tr>" + Postjson['SOA'][0]['SUBJECTIVE'] +"</tr></table></div>"
                    }
                },
                {
                    "title": "客觀描述",
                    "code": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "61149-1",
                                "display": "Objective Narrative"
                            }
                        ]
                    },
                    "text": {
                        "status": "generated",
                        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><table><tr>客觀描述\t</tr><tr>" + Postjson['SOA'][0]['OBJECTIVE'] +"</tr></table></div>"
                    }
                },
                {
                    "title": "評估",
                    "code": {
                        "coding": [
                            {
                                "system": "http://loinc.org",
                                "code": "51847-2",
                                "display": "Evaluation +​ Plan note"
                            }
                        ]
                    },
                    "text": {
                        "status": "generated",
                        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><table><tr>評估\t</tr><tr>" + Postjson['SOA'][0]['ASSESSMENT'] +"</tr></table></div>"
                    }
                }
            ]
        } 
        Compositionjson['section'].append(conditions)
        Proceduretext=''
        for p in Postjson['PROCEDURE']:
            Proceduretext = Proceduretext + "<tr><td>"+ str(p['ITEM']) +"\t</td><td>"+ str(p['PROCEDURE_CODE'])+"\t</td><td>"+ str(p['PROCEDURE_NAME'])+"\t</td><td>"+str(p['FREQUENCY'])+"\t</td><td>"+str(p['AMOUNT'])\
                +"\t</td><td>"+str(p['UNITS'])+"\t</td><td>"+str(p['PART'])+"\t</td><td>"+str(p['NOTE'])+"\t\n</td></tr>"
        Procedure = {
            "title": "處置項目",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "29554-3",
                        "display": "Procedure Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><table><tr><td>項次\t</td><td>處置代碼\t</td><td>處置名稱\t</td><td>頻率\t</td><td>數量\t</td><td>單位\t</td><td>部位\t</td><td>註記\t\n</td></tr><tbody>"\
                    + Proceduretext + "</tbody></table></div>"
            },
            "entry": [
                {                  
                }
            ]
        }
        Compositionjson['section'].append(Procedure)
        PRESCRIPTIONtext=''
        for p in Postjson['PRESCRIPTION']:
            PRESCRIPTIONtext = PRESCRIPTIONtext + "<tr><td>"+str(p['ITEM'])+"\t</td><td>"+str(p['TYPES_OF_PRESCRIPTION'])+"\t</td><td>"+str(p['DRUG_CODE'])+"\t</td><td>"+str(p['BRAND_NAME'])\
                +"\t</td><td>"+str(p['GENERIC_NAME'])+"\t</td><td>"+str(p['DOSAGE_FORM'])+"\t</td><td>"+str(p['DOSE'])+"\t</td><td>"+str(p['DOSE_UNIT'])\
                    +"\t</td><td>"+str(p['FREQUENCY'])+"\t</td><td>"+str(p['ROUTE_OF_ADMINISTRATION'])+"\t</td><td>"+str(p['MEDICATION_DAYS'])+"\t</td><td>"\
                        +str(p['TOTAL_AMOUNT'])+"\t</td><td>"+str(p['ACTUAL_UNITS'])+"\t</td><td>"+str(p['TOTAL_AMOUNT'])+"\t</td><td>"+str(p['ACTUAL_UNITS'])\
                            +"\t</td><td>"+str(p['POWDERED'])+"\t</td><td>"+str(p['NOTE'])+"\t\n</td></tr>"
        Medication = {
            "title": "處方內容",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "29551-9",
                        "display": "Medication prescribed Narrative"
                    }
                ]
            },
            "text": {
                "status": "generated",
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><table><tr><td>項次\t</td><td>處方箋種類註記\t</td><td>藥品代碼\t</td><td>藥品商品名稱\t</td><td>藥品學名\t</td><td>劑型\t</td><td>劑量\t</td><td>劑量單位\t</td><td>頻率\t</td><td>給藥途徑\t</td><td>給藥日數\t</td><td>給藥總量\t</td><td>給藥總量單位\t</td><td>實際給藥總量\t</td><td>實際給藥總量單位\t</td><td>磨粉註記\t</td><td>註記\t\n</td></tr><tbody>"\
                    + PRESCRIPTIONtext +"</tbody></table></div>"
            },
            "entry": [
                {
                }
            ]
        }
        Compositionjson['section'].append(Medication)
        
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
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><table><tr>家族圖譜:</tr><tr></tr></table></div>"
            },
            "entry": [
                {
                    "reference": "",
                    "display": ""
                }
            ]
        } 
        Compositionjson['section'].append(FAMILY_TREE_CONTENTS)
        
        IMAGING_STUDY_CONTENTS = {
            "title": "門診圖像",
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
                "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><table><tr>門診圖像:</tr><tr></tr></table></div>"
            },
            "entry": [
                {
                    "reference": "",
                    "display": ""
                }
            ]
        }
        Compositionjson['section'].append(IMAGING_STUDY_CONTENTS)
        
        url = fhir + 'Composition/'
        headers = {
          'Content-Type': 'application/json'
        }
        payload = json.dumps(Compositionjson)
        response = requests.request("POST", url, headers=headers, data=payload)
        resultjson=json.loads(response.text)
        #print(response.status_code)
        #return (Compositionjson, 200)
        return (resultjson, response.status_code)
    except:
        return (record,501)