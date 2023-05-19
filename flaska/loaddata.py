'''
import xmltodict
with open('VisitNote.xml', 'r', encoding="utf-8") as f:
    data = f.read()
record = xmltodict.parse(data)
Postxml = record['cdp:ContentPackage']['cdp:ContentContainer']['cdp:StructuredContent']['ClinicalDocument']
'''
import json
with open('tpehOPD.json', 'r', encoding="utf-8") as f:
    data = f.read()
    record = json.loads(data)