#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
from alphabet import INDEX, ALPHABET, REMOVE_INDEX, ASCII_INDEX, ZERO

""" C U N E I F O R M   T O O L S ================================

                                                Aleksi Sahala 2020
                                                2020-02-09

CuneiformSorter.sort(list, sort_index)

         Sorts transliteration and transcription in a list. List
         may consist of strings, tuples or lists. ´sort_index´
         defines by which element the nested lists are sorted.

============================================================== """

def remove_index(string):
    """ General tool for removing subscript indices from
    cuneifom transliteration """
    return string.translate(REMOVE_INDEX).replace('_', '')

def from_ascii(string):
    """ General tool for removing subscript indices from
    cuneifom transliteration """
    return string.translate(ASCII_INDEX)


class Tokenizer:

    def __init__(self, delimiters='-'):
        self.delimiters = delimiters
    
    def separate(self, string):
        string = re.sub('{.+?}', '', string)
        for d in self.delimiters:
            string = string.replace(d, '^')
        return string.split('^')


class CuneiformSorter:
    """ Sorts cuneiform transliteration and transcription taking in
    account special characters, indices etc. """

    def __init__(self):
        pass

    def validate(self, text):
        """ Sort input validator. Reveals undefined characters """
        def scan(string):
            for c in string:
                if c not in ALPHABET:
                    print('--> %s in <%s>' % (c, string))
        
        if isinstance(text, str):
            scan(text)
        if isinstance(text, (list, tuple)):
            for word in text:
                scan(word)
        else:
            print('validate() arg must be string or list/tuple of strings.')
       
    def sort(self, array, sort_index=0):

        if not array:
            return array

        def sort_alpha(array):
            array = [zero_fill(x) for x in array]
            try:
                return sorted(array, key=lambda item:
                              [ALPHABET.index(char) for char in item])
            except ValueError:
                print("Unable to sort due to unknown alphabet:")
                self.validate(array)
                print("Add symbols to alphabet.py definitions.")

        def un_zero_fill(string):
            return string.replace(ZERO, '')

        def zero_fill(string):
            """ Fill indices with leading zeros """
            outstring = ''
            i = len(string) - 1
            last = '_'
            for c in reversed(string):
                c_out = c
                if c in INDEX and last not in INDEX:
                    if string[i-1] not in INDEX:
                        c_out = c + ZERO
                outstring += c_out
                last = c
                i -= 1
            return outstring[::-1]
        
        if isinstance(array[0], str):
            array = [un_zero_fill(x) for x in sort_alpha(array)]
        if isinstance(array[0], (list, tuple)):
            order = {}
            for item in array:
                try:
                    order.setdefault(item[sort_index], []).append(item)
                except IndexError:
                    print('Cannot sort: sort_index (%i) exceeds longest sublist.' % sort_index)
                    sys.exit()
                    
            array = []
            for key in [un_zero_fill(x) for x in sort_alpha(order.keys())]:
                array.extend(order[key])
            
        return array
