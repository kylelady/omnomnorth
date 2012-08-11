#!/usr/bin/env python

from datetime import time, date, datetime, timedelta
import math

from restaurant import Restaurant, State

class Kroger(Restaurant):
    reg_hours = {'open': {'hour': 6, 'min': 0}, 'close': {'hour': 23, 'min': 59}}
    reg_night_hours = {'open': {'hour': 0, 'min': 0}, 'close': {'hour': 1, 'min': 0}}

    def get_hours(self, dt):
        if dt.time() < time(4):
            return {'open': time(self.reg_night_hours['open']['hour'],
                            self.reg_night_hours['open']['min'], 0),
                    'close': time(self.reg_night_hours['close']['hour'],
                            self.reg_night_hours['close']['min'], 0)}
        return {'open': time(self.reg_hours['open']['hour'],
                        self.reg_hours['open']['min'], 0),
                'close': time(self.reg_hours['close']['hour'],
                        self.reg_hours['close']['min'], 0)}


if __name__ == '__main__':
    print 'Open: %i' % State.OPEN
    print 'Opening Soon: %i' % State.OPENING_SOON
    print 'Closed: %i' % State.CLOSED
    print 'Closing Soon: %i' % State.CLOSING_SOON
    test = datetime(2012,5,18,10,15)
    p = Kroger()
    print p.get_hours(test)
    print p.get_status(test)
