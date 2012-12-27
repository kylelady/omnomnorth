#!/usr/bin/env python

from datetime import time, date, datetime, timedelta
import math

from restaurant import Restaurant, State


class Dominos(Restaurant):
    h_monwed = {'open':  {'hour': 10, 'min': 0},
                'close': {'hour': 23, 'min': 59}}
    h_thusat = {'open':  {'hour': 10, 'min': 0},
                'close': {'hour': 23, 'min': 59}}
    h_sun    = {'open':  {'hour': 10, 'min': 0},
                'close': {'hour': 23, 'min': 59}}
    h_monwedn = {'open':  {'hour': 0, 'min': 0},
                'close': {'hour': 3, 'min': 0}}
    h_thusatn = {'open':  {'hour': 0, 'min': 0},
                'close': {'hour': 4, 'min': 0}}
    h_sunn    = {'open':  {'hour': 0, 'min': 0},
                'close': {'hour': 2, 'min': 0}}

    def get_hours(self, dt):
        if dt.time() < time(5):
            today = ([self.h_sunn] + [self.h_monwedn]*3 + [self.h_thusatn]*3)[dt.weekday()]
        else:
        	today = ([self.h_monwed]*3 + [self.h_thusat]*3 + [self.h_sun])[dt.weekday()]
        return {'open':  time(today['open']['hour'],
                              today['open']['min'], 0),
                'close': time(today['close']['hour'],
                              today['close']['min'], 0)}


if __name__ == '__main__':
    print 'Open: %i' % State.OPEN
    print 'Opening Soon: %i' % State.OPENING_SOON
    print 'Closed: %i' % State.CLOSED
    print 'Closing Soon: %i' % State.CLOSING_SOON
    test = datetime(2012, 12, 28, 3, 30)
    p = Dominos()
    print p.get_hours(test)
    print p.get_status(test)
