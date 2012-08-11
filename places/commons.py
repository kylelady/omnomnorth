#!/usr/bin/env python

from datetime import time, date, datetime, timedelta
import math

from restaurant import Restaurant, State


class CommonsCafe(Restaurant):
    summer_start = {'month': 5, 'day': 1}
    summer_end = {'month': 8, 'day': 31}
    summer_hours = {'open': {'hour': 11, 'min': 0},
                    'close': {'hour': 14, 'min': 0}}
    reg_hours = {'open': {'hour': 11, 'min': 0},
                 'close': {'hour': 14, 'min': 0}}

    def get_hours(self, dt):
        summer = {'start': date(dt.year, self.summer_start['month'],
                                self.summer_start['day']),
                  'end': date(dt.year, self.summer_end['month'],
                              self.summer_end['day'])}
        if dt.date() >= summer['start'] and dt.date() <= summer['end']:
            if dt.weekday() >= 5:
                return None
            return {'open': time(self.summer_hours['open']['hour'],
                                 self.summer_hours['open']['min'], 0),
                    'close': time(self.summer_hours['close']['hour'],
                                  self.summer_hours['close']['min'], 0)}
        else:
            if dt.weekday() >= 5:
                return None
            return {'open': time(self.reg_hours['open']['hour'],
                                 self.reg_hours['open']['min'], 0),
                    'close': time(self.reg_hours['close']['hour'],
                                  self.reg_hours['close']['min'], 0)}


if __name__ == '__main__':
    print 'Open: %i' % State.OPEN
    print 'Opening Soon: %i' % State.OPENING_SOON
    print 'Closed: %i' % State.CLOSED
    print 'Closing Soon: %i' % State.CLOSING_SOON
    test = datetime(2012, 8, 11, 1, 11)
    print test.weekday()
    p = CommonsCafe()
    print p.get_hours(test)
    print p.get_status(test)
