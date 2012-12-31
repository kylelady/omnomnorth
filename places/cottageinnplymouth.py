#!/usr/bin/env python

from datetime import time, date, datetime, timedelta
import math

from restaurant import Restaurant, State


class CottageInn(Restaurant):
    h_sunthur = {'open':  {'hour': 10, 'min': 0},
                 'close': {'hour': 23, 'min': 59}}
    h_frisat  = {'open':  {'hour': 10, 'min': 0},
                 'close': {'hour': 1, 'min': 0}}

    def get_hours(self, dt):
    	today = ([self.h_sunthur]*4 + [self.h_frisat]*2 + [self.h_sunthur])[dt.weekday()]
        return {'open':  time(today['open']['hour'],
                              today['open']['min'], 0),
                'close': time(today['close']['hour'],
                              today['close']['min'], 0)}
