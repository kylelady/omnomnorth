#!/usr/bin/env python

from datetime import time, date, datetime, timedelta
import math

from restaurant import Restaurant, State


class Songbird(Restaurant):
    h_mon    = {'open':  {'hour':  7, 'min': 30},
                'close': {'hour': 18, 'min': 0}}
    h_tuefri = {'open':  {'hour':  7, 'min': 30},
                'close': {'hour': 22, 'min': 0}}
    h_sat    = {'open':  {'hour':  8, 'min': 0},
                'close': {'hour': 22, 'min': 0}}
    h_sun    = {'open':  {'hour':  8, 'min': 0},
                'close': {'hour': 18, 'min': 0}}

    def get_hours(self, dt):
        today = ([self.h_mon] + [self.h_tuefri]*4 + [self.h_sat] + [self.h_sun])[dt.weekday()]
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
