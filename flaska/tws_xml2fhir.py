# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:48:58 2023

@author: jim
"""
import os,shutil
#import xml.etree.ElementTree as ET
import xmltodict, json
from datetime import datetime
import pathlib
import requests

fhir = 'http://104.208.68.39:8080/fhir/'#4600VM
#fhir = "http://61.67.8.220:8080/fhir/"#skh
#fhir = "http://106.105.181.72:8080/fhir/"#tpech
#http://104.208.68.39:8080/fhir/Composition/17?_format=json

def OrganizationPut(providerOrganization_dict):
    jsonPath=str(pathlib.Path().absolute()) + "/patient_medical_records/Organization.json"
    Datajson = json.load(open(jsonPath,encoding="utf-8"))
    try:
        Datajson['id'] = providerOrganization_dict['@classCode'] + providerOrganization_dict['id']['@extension']
        Datajson['identifier'][0]['value'] = providerOrganization_dict['id']['@extension']
        Datajson['identifier'][0]['type']['coding'][0]['code'] = providerOrganization_dict['id']['@root']
        Datajson['name'] = providerOrganization_dict['name']
        payload = json.dumps(Datajson)
        url = fhir + 'Organization/' + providerOrganization_dict['@classCode'] + providerOrganization_dict['id']['@extension']
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("PUT", url, headers=headers, data=payload)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return (resultjson['id'])
    except:
        return ('NG')
    
def PatientPut(patientRole_dict):
    jsonPath=str(pathlib.Path().absolute()) + "/patient_medical_records/Patient.json"
    Datajson = json.load(open(jsonPath,encoding="utf-8"))
    try:
        date_object = datetime.strptime(patientRole_dict['patient']['birthTime']['@value'], '%Y%m%d')
        Datajson['birthDate'] = date_object.strftime("%Y-%m-%d")
        Datajson['identifier'][0]['value'] = patientRole_dict['id']['@extension']
        Datajson['identifier'][0]['type']['coding'][0]['code'] = patientRole_dict['id']['@root']
        Datajson['identifier'][1]['value'] = patientRole_dict['patient']['id']['@extension']
        Datajson['identifier'][1]['type']['coding'][0]['code'] = patientRole_dict['patient']['id']['@root']
        Datajson['id'] = patientRole_dict['patient']['id']['@extension']
        Datajson['gender'] = patientRole_dict['patient']['administrativeGenderCode']['@displayName'].lower()
        Datajson['name'][0]['family'] = patientRole_dict['patient']['name'][0]
        Datajson['name'][0]['given'][0] = patientRole_dict['patient']['name'][1:]
        Datajson['name'][0]['text'] = patientRole_dict['patient']['name']
        OrganizationID = OrganizationPut(patientRole_dict['providerOrganization'])
        if OrganizationID != 'NG':
            Datajson['managingOrganization']['reference'] = 'Organization/' + OrganizationID
        payload = json.dumps(Datajson)
        url = fhir + 'Patient/' + patientRole_dict['patient']['id']['@extension']
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("PUT", url, headers=headers, data=payload)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return (resultjson['id'])
    except:
        return ('NG')
    
def PractitionerPut(assignedAuthor_dict):
    jsonPath=str(pathlib.Path().absolute()) + "/patient_medical_records/Practitioner.json"
    Datajson = json.load(open(jsonPath,encoding="utf-8"))
    try:
        Datajson['identifier'][0]['value'] = assignedAuthor_dict['id']['@extension']
        Datajson['identifier'][0]['type']['coding'][0]['code'] = assignedAuthor_dict['id']['@root']
        Datajson['id'] = assignedAuthor_dict['id']['@extension']
        Datajson['name'][0]['family'] = assignedAuthor_dict['assignedPerson']['name'][0]
        Datajson['name'][0]['given'][0] = assignedAuthor_dict['assignedPerson']['name'][1:]
        Datajson['name'][0]['text'] = assignedAuthor_dict['assignedPerson']['name']
        payload = json.dumps(Datajson)
        url = fhir + 'Practitioner/' + assignedAuthor_dict['id']['@extension']
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("PUT", url, headers=headers, data=payload)
        resultjson=json.loads(response.text)
        #print(resultjson)
        return (resultjson['id'])
    except:
        return ('NG')
    
  
def component2section(component_dict):
    section = {
        'title': '',
        'code': {'coding': []},
        'text': {},
        'entry': []
        }
   
    try:
        coding = {
            "system": component_dict['section']['code']['@codeSystem'],
            "code": component_dict['section']['code']['@code'],
            "display": component_dict['section']['code']['@displayName']
            }
        section['code']['coding'].append(coding)
        section['title'] = component_dict['section']['title']
        if type(component_dict['section']['text'])==dict:
            try:
                section['text'] = {\
                    'status' : 'additional',\
                        'div' : '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + str(component_dict['section']['text']).strip().replace('\n', '').replace('\r', '').replace('\t', '') + '</div>'
                        } 
            except:
               section['text'] = {\
                   'status' : 'additional',\
                       'div' : '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + 'NG' + '</div>'
                       }  
                               
        else:
            section['text'] = {\
                'status' : 'additional',\
                    'div' : '<div xmlns=\"http://www.w3.org/1999/xhtml\">' + component_dict['section']['text'] + '</div>'
                    }
                
        if component_dict['section']['code']['@code'] == '19146-0':
            for i in range(len(component_dict['section']['component'])):
                section['entry'].append({
                        "title" :  component_dict['section']['title'],                        
                        "code": {
                            "coding": [
                                {
                                    "system": "http://loinc.org",
                                    "code": component_dict['section']['code']['@code'], 
                                    "display": component_dict['section']['code']['@displayName']
                                }
                            ]
                        },
                        "text": {
                            "status": "generated",
                            "div": '<div xmlns=\"http://www.w3.org/1999/xhtml\">'++'</div>'
                        },
                        'display' : component_dict['section']['component'][i]['section']['text']['paragraph']
                        })
            print('Observation')

        elif component_dict['section']['code']['@code'] == '11338-1':
            for i in range(len(component_dict['section']['entry'])):
                section['entry'].append({'display' : component_dict['section']['entry'][i]['observation']['code']['@displayName']})
            print('Condition')
                        
        elif component_dict['section']['code']['@code'] == '10155-0':
            section['entry'].append({'display' : component_dict['section']['text']['paragraph']})
            print('AllergyIntolerance')
            
        elif component_dict['section']['code']['@code'] == '29762-2':
            for i in range(len(component_dict['section']['component'])):
                section['entry'].append({'display' : component_dict['section']['component'][i]['section']['text']['paragraph']})
            print('social history Narrative')
            
        elif component_dict['section']['code']['@code'] == '29548-5':
            if len(component_dict['section']['entry'])>1:
                for i in range(len(component_dict['section']['entry'])):
                    section['entry'].append({'display' : component_dict['section']['entry'][i]['observation']['code']['@displayName']})
                print('Diagnosis Narrative')
            else:
                section['entry'].append({'display' : component_dict['section']['entry']['observation']['code']['@displayName']})
                print('Diagnosis Narrative 1')
                
            
        elif component_dict['section']['code']['@code'] == '19824-2':
            for i in range(len(component_dict['section']['component'])):
                try:
                    section['entry'].append({'display' : component_dict['section']['component'][i]['section']['text']['paragraph']})
                except :
                    section['entry'].append({'display' : component_dict['section']['component'][i]['section']['text']})
            print('Return visit conditions')
            
        elif component_dict['section']['code']['@code'] == '29554-3':
            if len(component_dict['section']['entry'])>1:
                for i in range(len(component_dict['section']['entry'])):
                    section['entry'].append({'display' : component_dict['section']['entry'][i]['procedure']['code']['@displayName']})
                print('Procedure')
            else:
                section['entry'].append({'display' : component_dict['section']['entry']['procedure']['code']['@displayName']})
                print('Procedure 1')
            
        elif component_dict['section']['code']['@code'] == '29551-9':
            if len(component_dict['section']['entry'])>1:
                for i in range(len(component_dict['section']['entry'])):
                    section['entry'].append({'display' : component_dict['section']['entry'][i]['substanceAdministration']['text']})
                print('MedicationStatement')
            else:
                section['entry'].append({'display' : component_dict['section']['entry']['substanceAdministration']['text']})
                print('MedicationStatement 1')
            
        elif component_dict['section']['code']['@code'] == '74027-4' or component_dict['section']['code']['@code'] == '19005-8':
            if len(component_dict['section']['entry'])>1:
                for i in range(len(component_dict['section']['component'])):
                    section['entry'].append({'display' : component_dict['section']['component'][i]['section']['text']['paragraph']})
                print('Media')
            else:
                section['entry'].append({'display' : component_dict['section']['component']['section']['text']['paragraph']})
                print('Media 1')
        else:
            print('None')
        return (section)
    except:
        return ('NG')
    
#print("date",date_time)
#print(os.getcwd())
jsonPath=str(pathlib.Path().absolute()) + "/patient_medical_records/Composition.json"
#print(jsonPath)
Compositionjson = json.load(open(jsonPath,encoding="utf-8"))
try:
    now = datetime.now()
    date_time = now.strftime("%Y%m%d")
    if os.path.exists('./mount_cos/processed/'+date_time)==True:
        print('exists')
    else:
        os.makedirs('./mount_cos/processed/'+date_time)
        print('makedirs')
        
    filelist = os.listdir('./mount_cos')
    #for file in filelist:
    #    try:
    #        print(file)
    #        shutil.move('./mount_cos/'+file, './mount_cos/processed/'+date_time)
    #    except :
    #        None
    
    with open('./mount_cos/'+filelist[3], 'r', encoding="utf-8") as myfile:
            obj = xmltodict.parse(myfile.read())
    xmldict=obj['cdp:ContentPackage']['cdp:ContentContainer']['cdp:StructuredContent']['ClinicalDocument']
    
    Compositionjson['title'] = xmldict['title']
    Compositionjson['confidentiality'] = xmldict['confidentialityCode']['@code']
    
    datetime_object = datetime.strptime(xmldict['effectiveTime']['@value'], '%Y%m%d%H%M')
    Compositionjson['date']=datetime_object.strftime("%Y-%m-%dT%H:%M:00")
    
    Compositionjson['subject']['reference'] = 'Patient/' + PatientPut(xmldict['recordTarget']['patientRole'])
    Compositionjson['subject']['display'] = xmldict['recordTarget']['patientRole']['patient']['name']
    
    Compositionjson['encounter']['display'] = xmldict['componentOf']['encompassingEncounter']['location']['healthCareFacility']['location']['name']
    
    Compositionjson['author'][0]['reference'] = 'Practitioner/' + PractitionerPut(xmldict['author']['assignedAuthor'])
    Compositionjson['author'][0]['display'] = xmldict['author']['assignedAuthor']['assignedPerson']['name']
    
    date_object = datetime.strptime(xmldict['author']['time']['@value'], '%Y%m%d%H%M')
    Compositionjson['attester'][0]['time'] = date_object.strftime("%Y-%m-%dT%H:%M:00")
    
    Compositionjson['custodian']['reference'] = 'Organization/' + OrganizationPut(xmldict['custodian']['assignedCustodian']['representedCustodianOrganization'])
    Compositionjson['custodian']['display'] = xmldict['custodian']['assignedCustodian']['representedCustodianOrganization']['name']
    
    Compositionjson['section']=[]
    for i in range(len(xmldict['component']['structuredBody']['component'])):
        Compositionjson['section'].append(component2section(xmldict['component']['structuredBody']['component'][i]))
   # print(Compositionjson['section'][7])
    url = fhir + 'Composition/'
    headers = {
      'Content-Type': 'application/json'
    }
    payload = json.dumps(Compositionjson)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
except :
    None