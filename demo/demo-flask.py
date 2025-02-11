#!/usr/bin/python
# -*- coding: utf-8 -*-
import pdb

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    pdb.set_trace()
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
