#/usr/bin/env python

from datetime import datetime

import places
import timezones


class InfoGatherer(object):
    _places = {
        'oncampus': {
            'commons': places.CommonsCafe(),
            'mujo': places.Mujo(),
            'panda': places.PandaExpress(),
            'quiznos': places.Quiznos(),
            'ugos': places.Ugos()
        }, 'prfe': {
            'bagelfragel': places.BagelFragel(),
            'biggby': places.Biggby(),
            'cafemarie': places.CafeMarie(),
            'greatplains': places.GreatPlains(),
            'jetspizza': places.JetsPizza(),
            'lucky': places.LuckyKitchen(),
            'marcos': places.MarcosPizza(),
            'nagomi': places.Nagomi(),
            'nothai': places.NoThai(),
            'qdoba': places.Qdoba(),
            'saica': places.Saica(),
            'seoulst': places.SeoulStreet(),
            'subway': places.CourtyardSubway(),
            'syrianbakery': places.SyrianBakery()
        }, 'krogerville': {
            'espresso': places.EspressoRoyale(),
            'jj': places.JimmyJohns(),
            'kroger': places.Kroger(),
            'zoup': places.Zoup()
        }, 'plymouth': {
            'buschs': places.Buschs(),
            'olgas': places.Olgas(),
            'sweetwaters': places.Sweetwaters(),
            'umi' : places.Umi()
        }, 'west': {
            'broadwaycafe' : places.BroadwayCafe(),
            'cottageinn' : places.CottageInn(),
            'northsidegrill': places.NorthsideGrill()
        }
    }

    def get_statuses(self):
        res = {}
        now = datetime.now()
        for area, places in self._places.iteritems():
            res[area] = []
            for name, place in places.iteritems():
                res[area].append(
                    {
                        'id': name,
                        'status': place.get_status(
                            datetime.now(timezones.Eastern))
                    })
        return res

if __name__ == '__main__':
    p = places.PandaExpress()
    print 'Hi!'
    ig = InfoGatherer()
    print ig.get_statuses()
