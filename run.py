#!/usr/bin/env python

import datetime
import json
import os
import time

from flask import Flask, make_response, request, render_template
from utils.translator import make_translator

from location import LocationManager

# Load language files
lang = {}
langs = os.listdir('lang')
for l in langs:
    name,ext = os.path.splitext(l)
    if ext == '.json':
        with open('lang/' + l, 'r') as f:
            lang[name] = json.load(f)

app = Flask(__name__)
lm = LocationManager.LocationManager('places')
lm.startPlaceWatch()

def gen_info(region):
    ''' Generate static-ish info'''
    info = {}
    start = datetime.date(2012, 06, 2)
    info['days'] = (datetime.date.today() - start).days
    info['regions'] = lm.getRegions()
    info['area_order'] = lm.getGroupOrder(region)
    return info

@app.route('/', methods=['GET', ])
def home():
    return site('north')

@app.route('/<region>', methods=['GET', ])
def site(region):
    if 'lang' in request.args and request.args['lang'] in lang:
        selected_lang = request.args['lang']
    elif 'lang' in request.cookies and request.cookies['lang'] in lang:
        selected_lang = request.cookies['lang']
    else:
        selected_lang = 'en'

    if region == '' or region not in lm.getRegions():
        region = 'north'

    status = lm.getStatuses(region)
    trans = make_translator(lang[selected_lang], lang['en'])

    title = 'OmNom{0}!'.format(region.title())

    info = gen_info(region)
    info['title'] = title

    try:
        with open('analytics.txt') as f:
            analytics = f.read()
    except IOError:
        analytics = ''
    resp = make_response(
        render_template(
            'main.html',
            info=info,
            places=status,
            translate=trans,
            analytics=analytics))
    resp.set_cookie('lang', selected_lang)
    return resp

if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')
