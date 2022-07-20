from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
app = Flask(__name__)

@app.route('/', methods=['POST'])
def test():
   payload = request.get_json()

   if payload:
       print(f'The requested Json is: {payload}')
       return payload
   else:
       print('Request for test page received with json body')
       return payload

if __name__ == '__main__':
   app.run()