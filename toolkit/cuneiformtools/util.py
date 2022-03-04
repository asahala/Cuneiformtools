#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
from cuneiformtools.alphabet import INDEX, ALPHABET, REMOVE_INDEX,\
     ASCII_INDEX, ZERO, DELIMITERS, PIPE


def sort(array, sort_index=0):
    """ Sorts cuneiform signs or transliterated/transcribed
    words alphabetically

    :param array             list to be sorted
    :param sort_index        if sorting list of lists, define
                             by which item the list is sorted

    :type array              list (of strings or lists/tuples)
    :type sort_index         int

    """

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
                print('Cannot sort: sort_index (%i) exceeds'\
                      ' longest sublist.' % sort_index)
                sys.exit(0)
                
        array = []
        for key in [un_zero_fill(x) for x in sort_alpha(order.keys())]:
            array.extend(order[key])
        
    return array    


def tokenize_line(line):
    return line.split(' ')


def unzip_word(word):
    """ Return signs and delimiters as separate lists

    :param word          input word in transliteration
    :type word           str

    """

    word = re.sub('\.\.+', '…', word)

    sign = ''
    signs = []
    delimiters = []

    pipe = ''
    for c in word:
        if c in DELIMITERS:
            if not pipe:
                signs.append(sign)
                delimiters.append(c)
                sign = ''
            else:
                sign += c
        elif c == PIPE:
            sign += c
            if not pipe:
                pipe = c
            else:
                pipe = ''
        elif c == '…':
            sign += '...'
        else:
            sign += c
    if sign:
        signs.append(sign)

    return signs, delimiters
        

def zip_word(signs, delimiters):
    """ Zip signs and delimiters back into words

    :param word          input word in transliteration
    :type word           str

    """
    
    word = ''
    for c in '_'.join(signs):
        if c == '_':
            word += delimiters.pop(0)
        else:
            word += c

    for d in delimiters:
        word += delimiters.pop(0)

    return word
