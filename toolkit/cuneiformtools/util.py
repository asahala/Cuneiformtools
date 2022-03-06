#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import textwrap
from cuneiformtools.alphabet import INDEX, ALPHABET, REMOVE_INDEX,\
     ASCII_INDEX, ZERO, DELIMITERS, PIPE, BRACKETS


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

    def validate(text):
        """ Sort input validator. Reveal undefined characters """
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

    def sort_alpha(array):
        array = [zero_fill(x) for x in array]
        try:
            return sorted(array, key=lambda item:
                          [ALPHABET.index(char) for char in item])
        except ValueError:
            print("Unable to sort due to unknown alphabet:")
            validate(array)
            print("Add symbols to alphabet.py definitions.")
            return array

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

    if not isinstance(array, (list, tuple)):
        print(f'Sort lists or tuples, not {type(array)}')
        return None
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


def tokenize(line):
    return line.split(' ')


def unzip_xlit(word, extra_delimiters=''):
    """ Return signs and delimiters as separate lists

    :param word          input word in transliteration
    :type word           str

    """

    delims_ = DELIMITERS + extra_delimiters

    word = re.sub('\.\.+', '…', word)

    sign = ''
    signs = []
    delimiters = []

    pipe = ''
    for c in word:
        if c in delims_:
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
        

def zip_xlit(signs, delimiters):
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


class Transducer:

    """ Transducer for bracket-insensitive substitutions.
    Consume input string character by character and either
    write or transduce them on the output tape;

    source and target must be interpolated or chunked to
    same length.

    E.g. a substitution pair {d}HAR : {d}SAGGAR will replace
    {d}HA[R-DU3] with {d}SAGG[AR-DU3], {[d}HA]R-DU3 with
    {[d}SAGG]AR-DU3 etc. """

    def __init__(self, ignore):
        self.ignore = ignore

    def _reset_tapes(self):
        self.tmp_out_tape = {'orig': [], 'trans': []}
        self.s_ = self.source.copy()
        self.t_ = self.target.copy()

    def _write_to_output_tape(self, tape):
        self.output_tape += tape
        self._reset_tapes()

    def interpolate(self):
        pass

    def chunk(self):
        pass

    def run(self, source, target, xlit, sign=False):

        if not xlit:
            return xlit

        self.output_tape = []

        if sign:
            self.xlit = '§' + xlit + '§'
            self.source = ['§'] + source + ['§']
            self.target = ['§'] + target + ['§']
        else:
            self.source = source
            self.target = target
            self.xlit = xlit

        self._reset_tapes()
        
        for c in self.xlit:

            if c in BRACKETS + self.ignore:
                self.tmp_out_tape['orig'].append(c)
                self.tmp_out_tape['trans'].append(c)
                continue
                
            self.tmp_out_tape['orig'].append(c)

            if c == self.s_[0]:
                """ Transduce from source alphabet to target
                alphabet """
                c_orig = c
                c_trans = self.t_.pop(0)
                self.s_.pop(0)
                #print(c, c_trans, '_',  self.tmp_out_tape, sep='\t')
                self.tmp_out_tape['trans'].append(c_trans)
            else:
                """ Reject output tape """
                #print(c, c, 'rej', self.tmp_out_tape, sep='\t')
                self._write_to_output_tape(self.tmp_out_tape['orig'])

            if not self.s_:
                """ Accept output tape """
                #print(c, c_trans, 'acc', self.tmp_out_tape, sep='\t')                        
                self._write_to_output_tape(self.tmp_out_tape['trans'])

        self._write_to_output_tape(self.tmp_out_tape['orig'] )

        """ Cleanup for free substitutions in case source and
        target differ a lot in length """
        stack = ''
        o = ''
        for c in ''.join(self.output_tape):
            if c == '§':
                continue
            if c in '!?#*':
                stack += c
            elif c in ' -(}':
                o += stack + c
                stack = ''
            else:
                o += c
        o += stack
        
        return o


def replace(source, target, xlit, sign=False, ignore=''):
    """ Replace strings in transliteration preserving
    bracket positions.
        
    :param source          what to replace
    :param target          replace with this
    :param xlit            input transliteration
    :param sign            constrain substitutions to full signs
    :param ignore          ignored characters

    :type source           str
    :type target           str
    :type xlit             str
    :type sign             bool
    :type ignore           str
    
    """

    tr = Transducer(ignore)

    def interpolate(string, longer):
        """ Interpolate source and target strings to same length,
        e.g. dingir : AN --> dingir : A^^^^N """
        
        out = [''] * longer
        shorter = len(string)
        for e, c in enumerate(string):
            out[e * (longer-1) // (shorter-1)] = c
        return out

    def chunk(string, shorter):
        """ Chunk target into multichar strings if source is
        shorter, e.g. AN : dingir --> AN : din^gir """
        
        string = list(tuple(target))
        k, m = divmod(len(string), shorter)
        return list(''.join(string[i*k+min(i, m):(i+1)*k+min(i+1, m)])
                 for i in range(shorter))

    """ Interpolate or chunk """
    if len(source) > len(target):
        target = interpolate(target, len(source))
    elif len(source) < len(target):
        target = chunk(target, len(source))
        if len(target) != len(source):
            print('Bad juju', source, target)
    else:
        target = list(tuple(target))
    source = list(tuple(source))

    if sign:
        """ Sign-level substitutions, e.g. en : X will change
        en-engar into X-engar """
        t, d = unzip_xlit(xlit, extra_delimiters=' ')
        parts = []
        for token in t:
            #tr = Transducer(source, target, token, ignore)
            parts.append(tr.run(source, target, token, sign))
        return (zip_xlit(parts, d))
    else:
        """ Free substitutions, e.g. en : X will change
        en-engar X-Xgar """
        #tr = Transducer(source, target, xlit, ignore)
        return tr.run(source, target, xlit, sign)
    
