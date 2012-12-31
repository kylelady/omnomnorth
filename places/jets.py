#!/usr/bin/env python

from datetime import time, date, datetime, timedelta
import math

from restaurant import Restaurant, State


class JetsPizza(Restaurant):
    h_monthur = {'open':  {'hour': 11, 'min': 0},
                 'close': {'hour': 22, 'min': 0}}
    h_frisat  = {'open':  {'hour': 11, 'min': 0},
                 'close': {'hour': 23, 'min': 59}}
    h_sun     = {'open':  {'hour': 12, 'min': 0},
                 'close': {'hour': 22, 'min': 0}}

    def get_hours(self, dt):
    	today = ([self.h_monthur]*4 + [self.h_frisat]*2 + [self.h_sun])[dt.weekday()]
        return {'open':  time(today['open']['hour'],
                              today['open']['min'], 0),
                'close': time(today['close']['hour'],
                              today['close']['min'], 0)}
