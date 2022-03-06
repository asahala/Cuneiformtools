#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Aleksi Sahala 2020 -- Assyriological alphabet definitions """

mixed_uppercase = False # set True to aAbB order instead of abAB

""" Define custom alphabetic order for Assyriological symbols.
If you encounter errors while sorting, add new characters here. """

DELIMITERS = '}{.:-' # includes determinative borders
NONALPHANUMERIC = "×!@#&%–-_[{⸢<()>⸣}].:;',?/\*`~$^+=“⁻ "
ZERO = 'Ø'
NUMERIC = "0123456789"
INDEX = "₀₁₂₃₄₅₆₇₈₉"
X_INDEX = "ₓ"
ALEPH = "ʾˀ"
ALPHA = "aáàâābcdeéèêēfgĝŋhḫiíìîījklmnoóòōôpqrřȓsšṣtṭuúùûūvwxyz"
CONSONANT = "bdfgĝŋhḫjklmnpqrřȓsšśṣtṭvwxyz" + ALEPH
VOWEL = "aiueo"
PIPE = "|"
ALPHANUMERIC = ALPHA + NUMERIC
BRACKETS = '[⸢⸣]'

ALLNUMBERS = ''.join([j for i in zip(list(NUMERIC),
                                     list(INDEX)) for j in i])

if mixed_uppercase:
    ALLALPHA = ''.join([j for i in zip(list(ALPHA),
                                       list(ALPHA.upper())) for j in i])
else:
    ALLALPHA = ALPHA + ALPHA.upper()
        
ALPHABET = NONALPHANUMERIC + ZERO +\
           ALLNUMBERS + X_INDEX + ALEPH + ALLALPHA + PIPE

""" Define index remover """
INDICES = INDEX + X_INDEX
REMOVE_INDEX = str.maketrans(INDICES, "_"*len(INDICES))

""" Define index ASCIIfier """
ASCII_INDEX = str.maketrans(NUMERIC + 'x', INDEX + X_INDEX)
