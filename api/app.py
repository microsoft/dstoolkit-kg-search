from datetime import datetime
from flask import Flask, request
import os
import sys
from api.search_expansion.search_expander import UMLSSearchExpander

# sys.path.append('../')

app = Flask(__name__)

search_expander = UMLSSearchExpander()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/search', methods=['POST'])
def search():

    kg_enabled = request.args.get('kg_enabled', default = 1, type = int)
    payload = request.get_json()

    print(f"KG Enable Flag: {kg_enabled}")

    if payload:
        print(f'The requested Json is: {payload}')

        if "search" not in payload:
            return "search keyword is not found in the JSON payload", 400
            
        else:
            search_text = payload["search"]

            if kg_enabled == 1:
                return search_expander.expand(search_text=search_text, parameters=payload)
            
            else:
                return search_expander.search(search_text=search_text, parameters=payload)
    else:
        print('No json body is recieved')
        return "Body is none", 400

if __name__ == '__main__':
    app.run(debug=True)

