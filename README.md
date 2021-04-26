# Cuneiformtools
Tools for processing cuneiform languages

## AA_signlist.json
Borger, Labat and OBO numbers based on Adam Anderson's spreadsheet

## oracc-sign-distribution.json
Sign distributions collected from Oracc.

    {"dialect|period":
        { "sign_name": 
           {"reading": freq, ...}
        ... }
    ... }

## alphabet.py

Contains alphabetic definitions and sign order in Adam Anderson's sign list. This should not be modified called unless you encounter undefined characters using sort-function in Cuneiformtools.CuneiformSorter() module.

## ogsl.py

Contains tools for performing variety of searches from the OGSL sign list:

#### ct.from_ascii(string)
Return (str) standard Unicode representation for ASCII ´string´: e.g. "RE2" -> "RE₂"

#### get_name(reading)
Return (str) sign name for ´reading´.

    get_name('an')
    >>> AN
    
#### get_values(sign, sort)
Return (list) of readings for ´sign´Set ´sort´ to True to sort the values.

    get_values('RI', sort=True)
    >>> ['bagₓ', 'bakₓ', 'dal', 'dala', 'de₅', 'degₓ', 'di₅' ...]
    
#### get_homophones(string, sort)              
Return (list) of phonetic sequences like ´string´. 

    get_homophones('an', sort=True)
    >>> [('an', 'AN'),
         ('an₂', '|GIŠ%GIŠ|'),
         ('anₓ', 'DIŠ'),
         ('anₓ', '|EZEN×BAD|')]

#### get_abstract(pattern)              
Return (list) of values that have a given phonetic/syllabic shape. ´pattern´ is a string that may consist of the following special symbols:

    C = any consonant
    V = any vowel
    : = length marker
    . = any single sound
    * = 0 or more anything

For example: get all readings with two geminata:
 
    get_abstract("*C:*C:*") 
    >>> ('abbununna', '|UD.HU.HI.NUN|')
        ('abbununnaₓ', '|UD.HU.HI.NUN|')
        ('abbununnu', '|UD.HU.HI.NUN|')
        ('abbununnuₓ', '|UD.HU.HI.NUN|')
        ('ibbanunna', '|UD.HU.HI.NUN|')
        ('ibbanunnaₓ', '|UD.HU.HI.NUN|')
        ('illamma', '|LAGAB×IM|')

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
Tokenizes Oracc cuneiform transliteration given as a ´string´ into signs. TODO: Determinatives, phonetic complements.

## download_corpora.py

Contains tools for downloading sign lists from different corpora and checking their contents against OGSL.

## parse-oracc-vrt.py

Builds dialect/period-wise sign list based on Oracc data. Supports the Korp (korp.csc.fi) VRT input only (file not included). Produces sub-sign lists form the oracc-sign-distribution.json
