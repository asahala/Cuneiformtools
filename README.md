# Cuneiformtools
Tools for processing cuneiform languages

## alphabet.py

Contains alphabetic definitions and sign order in Adam Anderson's sign list. This should not be modified called unless you encounter undefined characters using sort-function in Cuneiformtools.CuneiformSorter() module.

## ogsl.py

Contains tools for performing variety of searches from the OGSL sign list:

#### ct.from_ascii(string)
Return (str) standard Unicode representation for ´string´ in ASCII: e.g. "RE2" -> "RE₂"

#### get_name(reading)
Return (str) sign name for ´reading´: e.g. "lil₂" -> "KID"
    
#### get_values(sign, sort)
Return (list) of readings for ´sign´, e.g. ZI --> se₂, si₂ ṣe₂ ṣi₂ ze ... Set ´sort´ to True to sort the values.

#### get_homophones(string, sort)              
Return (list) of phonetic sequences like ´string´. For example, *an* returns:

    ('an', 'AN')
    ('anₓ', 'DIŠ')
    ('anₓ', '|EZEN×BAD|')
    ('an₂', '|GIŠ%GIŠ|')

#### get_abstract(pattern)              
Return (list) of values that have a given phonetic/syllabic shape. ´pattern´ is a string that may consist of the following special symbols:

    C = any consonant
    V = any vowel
    : = length marker
    . = any single sound
    * = 0 or more anything

For example: "\*C:\*" will get all readings with that contain any geminate.

#### contains_sign(sign, position)   
Return (list) of compound signs that contain ´sign´. The argument ´position´ may be: "final", "initial", "middle" or "any". E.g. PA with position flag "initial" will find PA.TE.SI, PA.LU
    
#### get_number(string, source)        
Return (str) Borger, Labat and OBO number for ´string´ that can be either sign name or a reading value. Agument ´source´ must be "Borger", "Labat" or "OBO".

## cuneiformtools.py

Basic functionalities for processing cuneiform languages

#### CuneiformSorter().sort(list, sort_index)
Sort input list according to the alphabet used in Assyriology. Takes into account indices and special symbols that the built-in sort functions do incorrectly.

#### CuneiformSorter().validate(input)
Validate ´input´ that can be either a single string or a list or tuple of strings. Reveals if the text has characters not defined in the custom alphabet.

#### Tokenizer().separate(string)
Tokenizes Oracc cuneiform transliteration given as a ´string´ into signs.
