#!/usr/bin/env python

from datetime import time, date, datetime, timedelta
import math

from restaurant import Restaurant, State

class Mujo(Restaurant):
    spring_start = {'month': 5, 'day': 1}
    spring_end = {'month': 6, 'day': 30}
    summer_start = {'month': 7, 'day': 1}
    summer_end = {'month': 8, 'day': 31}
    spring_hours = {'open': {'hour': 8, 'min': 0}, 'close': {'hour': 19, 'min': 0}}
    spring_fri_hours = {'open': {'hour': 8, 'min': 0}, 'close': {'hour': 18, 'min': 0}}
    summer_hours = {'open': {'hour': 8, 'min': 0}, 'close': {'hour': 18, 'min': 0}}
    summer_fri_hours = {'open': {'hour': 8, 'min': 0}, 'close': {'hour': 18, 'min': 0}}
    reg_hours = {'open': {'hour': 7, 'min': 0}, 'close': {'hour': 24, 'min': 0}}
    reg_night_hours = {'open': {'hour': 0, 'min': 0}, 'close': {'hour': 2, 'min': 0}}
    reg_sat_hours = {'open': {'hour': 12, 'min': 0}, 'close': {'hour': 18, 'min': 0}}
    reg_sun_hours = {'open': {'hour': 12, 'min': 0}, 'close': {'hour': 24, 'min': 0}}

    def get_hours(self, dt):
        spring = {'start': date(dt.year, self.spring_start['month'],
                                self.spring_start['day']),
                  'end': date(dt.year, self.spring_end['month'],
                                self.spring_end['day'])}
        summer = {'start': date(dt.year, self.summer_start['month'],
                                self.summer_start['day']),
                  'end': date(dt.year, self.summer_end['month'],
                                self.summer_end['day'])}

        if dt.date() >= spring['start'] and dt.date() <= spring['end']:
            if dt.weekday() >=5:
                return None
            if dt.weekday() == 4:
                    return {'open': time(self.spring_fri_hours['open']['hour'],
                                self.spring_fri_hours['open']['min'], 0),
                        'close': time(self.spring_fri_hours['close']['hour'],
                                self.spring_fri_hours['close']['min'], 0)}
            return {'open': time(self.spring_hours['open']['hour'],
                            self.spring_hours['open']['min'], 0),
                    'close': time(self.spring_hours['close']['hour'],
                            self.spring_hours['close']['min'], 0)}

        if dt.date() >= summer['start'] and dt.date() <= summer['end']:
            if dt.weekday() >= 5:
                return None
            if dt.weekday() == 4:
                return {'open': time(self.summer_fri_hours['open']['hour'],
                                self.summer_fri_hours['open']['min'], 0),
                        'close': time(self.summer_fri_hours['close']['hour'],
                                self.summer_fri_hours['close']['min'], 0)}
            return {'open': time(self.summer_hours['open']['hour'],
                            self.summer_hours['open']['min'], 0),
                    'close': time(self.summer_hours['close']['hour'],
                            self.summer_hours['close']['min'], 0)}

        else:
            if dt.time() < time(4): #late-night hours
                if 0 <= dt.weekday() - 1 <= 5:
                    return {'open': time(self.reg_night_hours['open']['hour'],
                                    self.reg_night_hours['open']['min'], 0),
                            'close': time(self.reg_night_hours['close']['hour'],
                                    self.reg_night_hours['close']['min'], 0)}
            if dt.weekday() == 5:
                return {'open': time(self.reg_sat_hours['open']['hour'],
                                self.reg_sat_hours['open']['min'], 0),
                        'close': time(self.reg_sat_hours['close']['hour'],
                                self.reg_sat_hours['close']['min'], 0)}
            if dt.weekday() == 6:
                return {'open': time(self.reg_sun_hours['open']['hour'],
                                self.reg_sun_hours['open']['min'], 0),
                        'close': time(self.reg_sun_hours['close']['hour'],
                                self.reg_sun_hours['close']['min'], 0)}
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
    p = Mujo()
    print p.get_hours(test)
    print p.get_status(test)
