#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools
import re
import json
import sys
import cuneiformtools as ct

""" =================================================================

                                                    Aleksi Sahala 2020
                                                            2020-02-06

  Thanks:
      Stephen Tinney for OGSL (https://github.com/oracc/ogsl)
      Niek Veldhuis for providing me with OGSL in JSON format
      Adam Anderson for his AA list with Labat, Borger and OBO numbers.


This script contains tools for exploring the OGSL. It offers same
basic functionalities as the old ePSD sign search, and some more.

ct.from_ascii(x)             Return (str) in UTF-8 from ASCII, e.g.
                             E2 returns E₂

get_name(x)                  Return (str) sign name for reading x
get_values(x)                Return (list) values for sign X
get_homonyms(x)              Return (list) of phonetic sequences like x
get_abstract(x)              Return (list) of values that have a given
                             phonetic/syllabic shape.

                               C = any consonant
                               V = any vowel
                               : = length marker
                               . = any single sound
                               * = 0 or more anything

                             e.g. *C:* will get all readings with that
                             contain any geminate.

contains_sign(x, position)   Return (list) of compound signs that contain
                             sign x; ´position´ may be set "final",
                             "initial" or "middle". If not specified any
                             position will be accepted.

get_number(x, source)        Return (str) number for sign or value x.
                             ´source´ must be "Borger", "Labat" or "OBO"
                             
================================================================= """

def readfile(filename):
    with open(filename, 'r', encoding="utf-8", errors="replace") as data:
        if filename.endswith('.json'):
            return json.load(data)
        else:
            return data.read().splitlines()    

class Signs:
        
    def __init__(self):
        self.AA_list = readfile('AA-signlist.json')
        self.list = {}
        self._parse_ogsl(readfile('ogsl-sl.json'))
        
    def _parse_ogsl(self, data):
        """ Transform JSON into dict and remove empty values """
        for key in data['signs'].keys():
            values = data['signs'][key].get('values', None)
            if values is not None:
                self.list.setdefault(key, values)

    def _collect_phonemic(self, phonemic):
        for key, values in self.list.items():
            for value in values:
                if re.match('^%s$' % phonemic, ct.remove_index(value)):
                    yield (value, key)

    def _set_sort_key(self, sort_index):
        """ Set sorting key by given string """
        return sort_index != 'value'    
    
    def sort(self, array, sort_index=0, sort=True):
        """ Check if results should be sorted """
        if sort:
            return ct.CuneiformSorter().sort(array, sort_index)
        else:
            return array     
    
    def get_name(self, value):
        """ Return sign name by value """
        for k, v in self.list.items():
            if value in v:
                return k

    def get_values(self, name, sort=False):
        """ Return values by sign name """
        if name.islower():
            name = self.get_name(name)
        values = self.list.get(name, None)
        return self.sort(values, 0, sort)
    
    def get_homonyms(self, reading, sort_by='value', sort=False):
        """ Get signs that have same phonetic value """
        sort_by = self._set_sort_key(sort_by)
        phonemic = ct.remove_index(reading)
        found = list(self._collect_phonemic(phonemic))
        return self.sort(found, sort_by, sort)

    def get_abstract(self, sign, sort=False):
        """ Get all signs that have a given phonetic shape """
        found = []
        C = 'bdfgĝŋhḫjklmnpqrřȓsšśṣtṭvwxyz'
        V = 'aiueo'
        chars = {'V': '([%s])' % V,
                 'C': '([%s])' % C,
                 ':': r'\_',
                 '.': '([%s%s])' % (C, V),
                 '*': '([%s%s-])*' % (C, V)}
        regex = ''
        """ Set regex back-references """
        group = 0
        for c in ''.join([chars.get(c, c) for c in sign]):
            if c == ')':
                group += 1
            elif c == '_':
                c = str(group)
            regex += c
        found = list(self._collect_phonemic(regex))
        return self.sort(found, 0, sort)
    
    def contains_sign(self, sign, position='', sort=False):
        """ Return signs that contain given sign """
        initial = '|' + sign + '.' 
        middle = '.' + sign + '.'
        final = '.' + sign + '|'
        
        if position == 'initial':        
            array = [key for key in self.list.keys()
                     if key.startswith(initial)]
        elif position == 'final':
            array = [key for key in self.list.keys()
                     if key.endswith(final)]
        elif position == 'middle':
            array = [key for key in self.list.keys()
                     if (middle) in key]
        else:
            array = [key for key in self.list.keys()
                     if (initial) in key
                     or (middle) in key
                     or (final) in key]
            
        return self.sort(array, 0, sort)

    def get_number(self, sign, source=''):
        if source not in ('Labat', 'Borger', 'OBO'):
            print('argument source must be ´Labat´, ´Borger´ or ´OBO´')
            sys.exit()
            
        if sign.islower():
            sign = self.get_name(sign)

        key = self.AA_list.get(sign, None)
        if key is not None:
            return key.get(source, None)
            
ogsl = Signs()
def demo():
    #print(x)
    #x = ogsl.get_abstract('*C:*C:*', sort=True)
    #x = ogsl.contains_sign('LAGAB', position='initial')
    #x = ogsl.get_homonyms('an')
    if isinstance(x, str):
        print(x)
    else:
        for v in x:
            print(v)
