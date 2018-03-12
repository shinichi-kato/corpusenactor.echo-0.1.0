#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CorpusEnactor.Echo-0.1.0 UI

"""

from __future__ import unicode_literals
from __future__ import print_function


import os
import logging
import pickle
from flask import Flask,render_template, request

from corpusenactor.echo import Echo


app = Flask(__name__)

MAIN_LOG_DISPLAY_LEN = 10
MAIN_LOG_PRESERVE_LEN = 100
LOG_FILENAME = '/'+BUCKET_NAME+"/main_log"



@app.route('/',methods=['POST','GET'])
def index():

    lines = []

    if request.method == 'POST':
        text = request.form['text']

        ce = Echo("chatbot/chatbot.yaml")
        reply = ce.reply(text)

        lines.append({"speaker":"user","text":text})
        lines.append({"speaker":"bot","text":reply})
        lines = lines[-MAIN_LOG_PRESERVE_LEN:]


    return render_template("index.html",lines=lines[-MAIN_LOG_DISPLAY_LEN:])




@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
