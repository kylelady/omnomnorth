#!/usr/bin/env python

from datetime import timedelta
import math

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

State = enum('OPEN', 'OPENING_SOON', 'CLOSED', 'CLOSING_SOON')

class Restaurant(object):
    def get_status(self, dt):
        raise NotImplementedError()

    def get_status(self, dt):
        onehour = timedelta(hours=1)
        hours = self.get_hours(dt)
        if hours == None:
            return State.CLOSED
        if hours['open'] > dt.time():
            if self.timediff(hours['open'], dt.time()) <= onehour:
                return State.OPENING_SOON
            return State.CLOSED
        elif hours['close'] > dt.time():
            if self.timediff(hours['close'], dt.time()) <= onehour:
                return State.CLOSING_SOON
            return State.OPEN
        return State.CLOSED

    @staticmethod
    def timediff(t1, t2):
        time1 = t1.hour + float(t1.minute) / 60
        time2 = t2.hour + float(t2.minute) / 60
        diff = abs(time1 - time2)
        hours = math.trunc(diff)
        res = timedelta(hours=hours, minutes=math.trunc((diff - hours) * 60))
        return res
