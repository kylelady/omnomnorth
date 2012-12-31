#!/usr/bin/env python

from datetime import time, date, datetime, timedelta
import math

from restaurant import Restaurant, State


class NorthsideGrill(Restaurant):
    h = {'open':  {'hour': 7, 'min': 0},
         'close': {'hour': 15, 'min': 0}}

    def get_hours(self, dt):
        return {'open':  time(self.h['open']['hour'],
                              self.h['open']['min'], 0),
                'close': time(self.h['close']['hour'],
                              self.h['close']['min'], 0)}
