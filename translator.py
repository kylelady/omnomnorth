#!/usr/bin/env python


def make_translator(lang, fallback):
    def translate(key):
        s = str(key)
        if s in lang:
            return lang[s]
        elif s in fallback:
            return fallback[s]
        else:
            return s
    return translate
