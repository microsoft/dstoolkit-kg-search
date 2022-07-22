from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
from flask_cors import CORS
import pandas as pd
import pandasql as ps
import json
import random
import time
import os
from datetime import datetime
from dotenv import load_dotenv
from utilities import search_sdk

load_dotenv() 
# instantiate flask app
app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = os.environ['MAX_CONTENT_SIZE']*1024*1024
CORS(app)

# initiate custom search sdk
searchSDK = search_sdk.SearchSDK()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('index'))
    else:
        document_types=['.pdf']
        document_languages=['en']
        return render_template('index.html',document_types=document_types, document_languages=document_languages)

@app.route('/search', methods=['POST'])
def search():
    
    results = []
    
    # input data
    data = request.json
    
    kg_enabled = 1 if 'input_kg_check' in data.keys() and data['input_kg_check'] else 0
    input_keywords = data['input_keywords'] if 'input_keywords' in data.keys() and len(data['input_keywords'])>0 else '*'
    
    # advanced search
    query_schema = {  
        "count": True,
        "search": input_keywords,
        "filter": "",
        # "facets": [],  
        # "select": "",
        "highlight": "title, abstract, mesh_terms",
        "highlightPreTag": "<em class='highlight'>",
        "highlightPostTag": "</em>",
        "searchMode": "any",  
        "queryType": "simple",
        "skip": 0,
        "top": 50
    }
        
    results = None
    
    try:
        # API Call
        status_code, raw_results = searchSDK.search(query_schema, kg_enabled)

        if status_code == 200 and raw_results['@odata.count'] > 0:
            # parse results
            search_count = raw_results['@odata.count']
            results = raw_results['value']

        else:
            search_count = 0

        # placeholder for testing
        # results = [{'@search.score': 7.9158406, '@search.highlights': {'content': ["The P-<em class='highlight'>ELSORTM</em> session \n\nwas conducted from 2nd to 4th February 2016.", "The P-\n\n<em class='highlight'>ELSORTM</em> session has surfaced issues related to design integrity, safety and operability for Puteri \n\nplatform.", "P-\n\n<em class='highlight'>ELSORTM</em> session has surfaced issues related to design integrity, safety, reliability and operability \n\nfor Puteri Platform.", "REFERENCES \n\nThe following documents were used as main reference for this P-<em class='highlight'>ELSORTM</em>. \n\n1.", "APPENDICES \n\nAppendix – A : P-<em class='highlight'>ELSORTM</em> Team Members \n\nAppendix – B : Overall Single Line Diagram of Puteri Platform."], 'enrich_keyphrases': ["P-<em class='highlight'>ELSORTM</em> Team Member", "The P-<em class='highlight'>ELSORTM</em> session", "<em class='highlight'>ELSORTM</em> session", "<em class='highlight'>ELSORTM</em>", "P-<em class='highlight'>ELSORTM</em>"]}, 'metadata_storage_content_type': 'application/pdf', 'metadata_storage_path': 'https://jixjiastorage.blob.core.windows.net/myexperts/poc/P-ELSOR%20Puteri%20Platform%20PMO.pdf.pdf', 'enrich_people': ['SMAY', 'Busbar B', 'Puteri', 'Loss'], 'enrich_organizations': ['PETRONAS', 'P-ELSORTM', 'PETRONAS Carigali Sdn. Bhd.', 'PETROLIAM NASIONAL BERHAD', 'MAAT', 'PETRONAS CARIGALI SDN', 'BHD', 'ESATO', 'Electrical Safety and Operability', 'GTG', 'ELSORTM', 'PCSB-PMO', 'SapuraKencana', 'PCSB', 'P-ELSOR™', 'Team', 'EDG', 'ACB-111', 'ACB-110', 'ACB', 'DEG', 'SB', 'SB-7710', 'ACB-101', 'Busbar B', 'ACB-', 'ACB-103', 'Heat Media', 'UPS', '11', '101', 'DB', 'MCCB', 'LOTO', 'NIL', 'PMO'], 'enrich_locations': ['Puteri Platform', 'Peninsular Malaysia', 'PENINSULAR MALAYSIA', 'Platform', 'Puteri platform', 'platform', 'plant', 'Bus-B', 'Puteri', 'GQ', 'SB-7', '-111', 'C', 'GQ-7720', 'EDG', 'B. Lube oil', 'kitchen', 'battery room', '-1', 'ACB', 'facility', 'room', 'Exit', 'bar', 'LQ', 'well', 'galley', 'wellhead', 'Zone 2', 'Electrical Room'], 'enrich_language': 'en', 'ref_file_name': 'P-ELSOR Puteri Platform PMO.pdf.pdf', 'ref_content_length': 615760, 'ref_created_on': '2016-03-15T02:01:30Z', 'ref_author': 'myexperts', 'ref_special_note': 'This is a PoC for MyExperts project building Search Engine and Knowledge Graph'}]
        # search_count = 1
        
        return json.dumps({
            'data': render_template('results.html', results=results, search_count=search_count)
        })
    
    except Exception as e:
        return 'error', e.args


if __name__ == '__main__':
    app.run(debug=True)
