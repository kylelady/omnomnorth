#!/usr/bin/env python

import datetime
import json
import time

from flask import Flask, make_response, request, render_template

from info_gatherer import InfoGatherer
from places import restaurant
from translator import make_translator

#from interval_tree import IntervalTree, Interval

#class ScheduleInterval(Interval):
#    __slots__ = ('priority', 'state')
#    def __init__(self, start_day, start_time, stop_day, stop_time, priority, state):
#        self.start = self.minutes_since_monday_midnight(start_day, start_time)
#        self.stop = self.minutes_since_monday_midnight(stop_day, stop_time)
#        self.priority = priority
#        self.state = state
#
#    def __repr__(self):
#        state = 'Open' if self.state == State.OPEN else 'Closed'
#        return 'Interval(%i, %i, $i, $s)' % (self.start, self.stop, self.priority, state)
#
#    def __getstate__(self):
#        return {'start': self.start, 'stop': self.stop,
#                'priority': self.priority, 'state': 1 if self.state == State.OPEN else 0}
#
#    def __setstate__(self, state):
#        for k, v in state.iteritems():
#            if k == 'state':
#                setattr(self, k, State.OPEN if v == 1 else State.CLOSED)
#            else:
#                setattr(self, k, v)
#
#    @staticmethod
#    def minutes_since_monday_midnight(day, t):
#        return day * 1440 + t.hour * 60 + t.minute
#
#    @staticmethod
#    def convert_time(s):
#        return datetime.time(int(s[:2]), int(s[2:]))
#
#    @staticmethod
#    def convert_state(s):
#        if s == 'open':
#            return State.OPEN
#        if s == 'closed':
#            return State.CLOSED
#        raise KeyError
#
#    @classmethod
#    def make_si(cls, day, ival, priority):
#        return cls(day, cls.convert_time(ival['start']), day, cls.convert_time(ival['end']), priority, cls.convert_state(ival['status']))


with open('lang.json') as f:
    lang = json.load(f)

#hours = {}
#for place in info['places']:
#    if place is None:
#        continue
#    with open('%s.json' % place) as f:
#        hours[place] = json.load(f)
#days = ['mon', 'tues', 'wed', 'thurs', 'fri', 'sat', 'sun']
#intervals = {}
#for place in hours:
#    intervals[place] = []
#    if 'default_hours' in hours[place]:
#        if 'all' in hours[place]['default_hours']:
#            for day in days:
#                intervals[place].append(ScheduleInterval.make_si(days.index(day), hours[place]['default_hours']['all'], 0))
#        if 'weekday' in hours[place]['default_hours']:
#            for day in days[:5]:
#                intervals[place].append(ScheduleInterval.make_si(days.index(day), hours[place]['default_hours']['weekday'], 1))
#        if 'weekend' in hours[place]['default_hours']:
#            for day in days[5:]:
#                intervals[place].append(ScheduleInterval.make_si(days.index(day), hours[place]['default_hours']['weekend'], 1))
#        for day in days:
#            if day in hours[place]['default_hours']:
#                intervals[place].append(ScheduleInterval.make_si(days.index(day), hours[place]['default_hours'][day], 2))
#
#interval_trees = {}
#for place in hours:
#    interval_trees[place] = IntervalTree(intervals[place])

app = Flask(__name__)

def gen_info():
    ''' Generate static-ish info'''
    info = {}
    start = datetime.date(2012, 06, 2)
    info['days'] = (datetime.date.today() - start).days
    info['area_order'] = ['oncampus', 'prfe', 'krogerville', 'plymouth']
    return info

#def is_open(itree, d, t):
#    curtime = ScheduleInterval.minutes_since_monday_midnight(d, t)
#    res = itree.find(curtime, curtime + 1)
#    if len(res) == 0:
#        return False
#    best_p = res[0].priority
#    state = res[0].state
#    for ival in res:
#        if ival.priority >= best_p:
#                best_p = ival.priority
#                state = ival.state
#    return state == State.OPEN

ig = InfoGatherer()

@app.route('/', methods=['GET',])
def run():
    if 'lang' in request.args and request.args['lang'] in lang:
        selected_lang = request.args['lang']
    elif 'lang' in request.cookies and request.cookies['lang'] in lang:
        selected_lang = request.cookies['lang']
    else:
        selected_lang = 'en'

    values = {}
    noon = datetime.time(12, 0)
    tenpm = datetime.time(22, 0)
    values['test'] = 'Hello, world!'
    status = ig.get_statuses()
    #values['test'] = 'open' if is_open(interval_trees['panda'], 3, noon) else 'closed'
    trans = make_translator(lang[selected_lang], lang['en'])
    resp = make_response(render_template('main.html', values=values, info=gen_info(), places=status, translate=trans))
    resp.set_cookie('lang', selected_lang)
    return resp

if __name__ == "__main__":
    app.run(debug=True, port=5001)
