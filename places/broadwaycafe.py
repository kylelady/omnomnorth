#!/usr/bin/env python

from datetime import time, date, datetime, timedelta
import math

from restaurant import Restaurant, State


class BroadwayCafe(Restaurant):
    h_monfri = {'open':  {'hour': 10, 'min': 30},
                'close': {'hour': 19, 'min': 0}}
    h_sat    = {'open':  {'hour': 10, 'min': 30},
                'close': {'hour': 15, 'min': 0}}
    h_sun    = {'open':  {'hour': 0, 'min': 0},
                'close': {'hour': 0, 'min': 0}}

    def get_hours(self, dt):
    	today = ([self.h_monfri]*5 + [self.h_sat] + [self.h_sun])[dt.weekday()]
        return {'open':  time(today['open']['hour'],
                              today['open']['min'], 0),
                'close': time(today['close']['hour'],
                              today['close']['min'], 0)}
