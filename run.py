#!/usr/bin/env python

import datetime
import json
import time

from flask import Flask, make_response, request, render_template
from translator import make_translator

from locations import LocationManager

with open('lang.json') as f:
   lang = json.load(f)

app = Flask(__name__)
#ig = InfoGatherer()
lm = LocationManager.LocationManager('locations')

def gen_info():
    ''' Generate static-ish info'''
    info = {}
    start = datetime.date(2012, 06, 2)
    info['days'] = (datetime.date.today() - start).days
    info['area_order'] = lm.getGroupOrder()
    return info



@app.route('/', methods=['GET', ])
def run():
    if 'lang' in request.args and request.args['lang'] in lang:
        selected_lang = request.args['lang']
    elif 'lang' in request.cookies and request.cookies['lang'] in lang:
        selected_lang = request.cookies['lang']
    else:
        selected_lang = 'en'

    status = lm.getStatuses()
    trans = make_translator(lang[selected_lang], lang['en'])
    try:
        with open('analytics.txt') as f:
            analytics = f.read()
    except IOError:
        analytics = ''
    resp = make_response(
        render_template(
            'main.html',
            info=gen_info(),
            places=status,
            translate=trans,
            analytics=analytics))
    resp.set_cookie('lang', selected_lang)
    return resp

if __name__ == "__main__":
    app.run(debug=True, port=5001)
