import re
import json
from collections import Counter

""" Transliteration and lemmatization normalizer :: asahala 2021

                                              Version 2022-03-02

This script normalizes inconsistencies in Oracc transliteration.
XLITTools has the following methods:

  accent_to_index(string)
             Normalizes accented indices into unicode
             subscript numbers.
             
  unify_determinatives(string, lower)
             Normalize determinatives into uppercase. There are
             lots of dubious phonetic complements in Oracc not
             properly marked with precding +, these are not
             separated here. Korp Oracc version has also bugged
             phonetic complements with missing hyphens.

             Set `lower` to False if you want to have them in
             the upper case

  subscribe_indices(string)
             Converts numeric indices into subcripts, e.g.
             du11 --> du₁₁
             
  normalize_h(string)
             Removes diacritic from /h/.
             
  normalize_all(string)
             Apply all normalizations to string if they are
             relevant to it.

  get_signs(string)
             Get a "soft hash" of word in sign name notation,
             e.g. {d}en-lil₂-la₂-še₃' --> ^AN^EN^KID^LAL^EŠ₂

  compare_strings(string1, string2)
             Compares soft hashes of two transliterations.
             For example, this function returns True for
             a-ka₃-am-gim and a-ga-am-gin₇, because they both
             written with signs (A, GA, |GUD×KUR|, DIM₂)

             Use normalize_all() to to normalize the strings.
          
LemmaTools can be used to fix some incosistencies in Oracc
lemmatization.
             
"""

LOG = []

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def save_log(filename):
    if LOG:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('total changes: %i\n' % len(LOG))
            f.write('number\tchange\n')
            for entry, num in sorted(Counter(LOG).items()):
                f.write('%s\t%s\n' % (str(num), entry))
        print('> %i normalizations made, see %s' % (len(LOG), filename))
    else:
        print('Log is empty!')

def logger(orig, fix, id_=None):
    """ Collect all changes into log """
    if id_ is None:
        identifier = '_'
    else:
        identifier = id_
        
    if orig != fix:
        LOG.append('%s\t%s -> %s' % (identifier, orig, fix))


class XLITTools:

    def __init__(self, ogsl_file=None):
        self.two = frozenset('áéíúÁÉÍÚ')
        self.three = frozenset('àèìùÀÈÌÙ')
        self.accents = self.two.union(self.three)
        self.numbers = frozenset('0123456789x')
        self.deaccent = {'à': 'a', 'á': 'a',
                         'è': 'e', 'é': 'e',
                         'ì': 'i', 'í': 'i',
                         'ù': 'u', 'ú': 'u',
                         'À': 'A', 'Á': 'A',
                         'È': 'E', 'É': 'E',
                         'Ì': 'I', 'Í': 'I',
                         'Ù': 'U', 'Ú': 'U'}
        self.split = frozenset('.-– ×{}*?!()\t%+@')
        self.h = str.maketrans('ḫḪ', 'hH')
        self.digits = str.maketrans("0123456789x", "₀₁₂₃₄₅₆₇₈₉ₓ")
        self.ogsl = {}
        self.ogsl_file = ogsl_file
        self._parse_ogsl()


    def _parse_ogsl(self):
        if self.ogsl_file is not None:
            print("> reading OGSL...")
            """ Build a sign dictionary based on JSON file by mapping
            normalized sign values to value(SIGN) notation """
            with open(self.ogsl_file, 'r', encoding='utf-8') as f:
                ogsl = json.load(f)
                
            for sign in ogsl['signs'].keys():
                vals = ogsl['signs'][sign].get('values', None)
                if vals is not None:
                    for v in vals:
                        self.ogsl[v] = sign


    def _map_signs(self, xlit):
        """ Map all sign values in string to name representation, i.e.
        lugal-uru-da --> LUGAL^IRI^DA """
        
        def hyphenate(s):
            s = s.lower()
            s = s.replace('}', '-')
            s = s.replace('{', '-')
            s = s.replace('--', '-')
            return re.sub('[\.:-]', '-', s)
        
        return '^'.join([self.ogsl.get(sign, sign) for sign in hyphenate(xlit).split('-')])


    def compare_strings(self, string1, string2):
        """ Compare if transliterations contain the same signs.
        For example, {1}qú-ur-ru and {m}ku-ur-ru are indentical because
        KU stands for both, qú and ku, and DIŠ stands for {1} and {m} """     
        s1 = self._map_signs(self.normalize_all(string1))
        s2 = self._map_signs(self.normalize_all(string2))
        return s1 == s2


    def get_signs(self, string):
        """ Map signs into sign names, e.g. qú-ur --> KU^UR """
        return self._map_signs(self.normalize_all(string))


    def subscribe_indices(self, string):
        """ Convert digit-based indices into subscripts """
        last = ''
        last_is_subscript = False
        
        newstring = ''
        for e, c in enumerate(string):

            if e == len(string)-1:
                next_ = ''
            else:
                next_ = string[e+1]
                
            if c.isdigit() and last.isalpha():
                c = c.translate(self.digits)
                last_is_subscript = True
            elif last_is_subscript and c.isdigit():
                c = c.translate(self.digits)
            elif c == 'x' and next_ == '(' and last.isalpha():
                c = c.translate(self.digits)
            else:
                last_is_subscript = False
                
            last = c
            newstring += c
            
        return newstring
    
                        
    def accent_to_index(self, string):
        """ Convert accents into subscript indices """
        xlit = ''
        index = ''
        for c in string + ' ':
            if c in self.two:
                index = '₂'
            if c in self.three:
                index = '₃'
            if c in self.split:
                xlit += index + c
                index = ''
            else:
                xlit += self.deaccent.get(c, c)
        xlit = re.sub('([⌉\]>\|#])([₂₃])', r'\2\1', xlit)
        return xlit.rstrip()


    def unify_determinatives(self, string, lower=True):
        """ Lower/uppercase determinatives """
        norm = ''
        string = re.sub('(^|-|\.)([fmd])\.', r'\1{\2}', string)
        if '{' in string:
            upper = False
            i = 0
            for c in string:
                if c == '{':
                    upper = True
                elif c == '+' and string[i-1] == '{':
                    upper = False
                elif c == '}':
                    upper = False
                elif c in ('m', 'd', 'f', '1')\
                     and string[i-1] == '{' and string[i+1] == '}':
                    upper = False
                    if c == '1':
                        c = 'm'
                if upper:
                    if lower:
                        c = c.lower()
                    else:
                        c = c.upper()
                norm += c
                i += 1
            string = norm
        return string


    def normalize_h(self, string):
        norm = string.translate(self.h)
        return norm

    
    def normalize_all(self, string, id_=None):
        """ Run all relevant normalizations for string """
        norm = self.normalize_h(string)
        chars = set(norm)
        if chars.intersection(self.numbers):
            norm = self.subscribe_indices(norm)
        if chars.intersection(self.accents):
            norm = self.accent_to_index(norm)
        if '{' in norm:
            norm = self.unify_determinatives(norm)
        logger(string, norm, id_)
        return norm


class LemmaTools:

    def __init__(self, errorfile=None):
        self.fixdict = {}
        if errorfile is not None:
            self.make_dict(errorfile)

    def make_dict(self, filename):
        """ Initialize stuff to be corrected """
        for line in read_file(filename):
            if not line.startswith('#'):
                error, correct, pos = line.split('\t')
                self.fixdict[error + '+' + pos] = correct

    def fix_lemma(self, lemma, pos):
        key = '%s+%s' % (lemma, pos)
        norm = self.fixdict.get(key, lemma)
        logger(lemma, norm, 'lemma')
        return norm


def unit_test():

    status = [0,0] 
    XT = XLITTools(ogsl_file='ogsl-sl.json')

    print('> Running unit test...')
    pairs = [('lu-lú-lùl-sa4', 'lu-lu₂-lul₃-sa₄', True),
             ('lu-lú-[lù]l-sa44', 'lu-lu₂-[lu]l₃-sa₄₄', True),
             ('lu-lú(|DUR6.Á|)-lùl#-sa14', 'lu-lu₂(|DUR₆.A₂|)-lul₃#-sa₁₄', True),
             ('lu-lú(|DÚR+Á|){KI}-lùl-sa4', 'lu-lu₂(|DUR₂+A₂|){ki}-lul₃-sa₄', True),
             ('lu-l[ú(|DÚR%%Á|)-lù]l-sa4', 'lu-l[u₂(|DUR₂%%A₂|)-lu]l₃-sa₄', True),
             ('lu111-lu2(|DUR2%%Á|)-lul3-sa4', 'lu₁₁₁-lu₂(|DUR₂%%A₂|)-lul₃-sa₄', True),
             ('lu#-lú(|DÚR×Á.U|)-{URÙDA}lùl-sa4', 'lu#-lu₂(|DUR₂×A₂.U|)-{uruda₃}lul₃-sa₄', True),
             ('lu-{d}lú(|DUR6×Á|)-lùl-sa4#', 'lu-{d}lu₂(|DUR₆×A₂|)-lul₃-sa₄#', True),
             ('<lú(|DU16%%DU3|)>-{t[ú]g}lùl{+lu-ul}', '<lu₂(|DU₁₆%%DU₃|)>-{t[u]g₂}lul₃{+lu-ul}', True),
             ('{D}30', '{d}30', True),
             ('60-x', '60-x', True),
             ('EN+60', 'EN+60', True),
             ('6.4.0.1(DIŠ)', '6.4.0.1(DIŠ)', True),
             ('{M}da-da', '{M}da-da', False),
             ('{F}da-da', '{f}da-da', True),
             ('f.da-da', '{f}da-da', True),
             ('m.da-d.da', '{m}da-{d}da', True),
             ('f.am.mu.ud.da', '{f}am.mu.ud.da', True),
             ('f.am.mu.ud.d.da', '{f}am.mu.ud.{d}da', True),
             ('{1}da-da', '{m}da-da', True),
             ('{M}{d}da-da', '{m}{d}da-da', True),
             ('kirix(|DA.DU|)-{d}MÚ{+mu!(BÁ)}', 'kiriₓ(|DA.DU|)-{d}MU₂{+mu!(BA₂)}', True),
             ('{dug}kirix(|DA.DU|){KI}-{d}MÚ{+mu!(BÁ)}', '{DUG}kiriₓ(|DA.DU|){KI}-{d}MU₂{+mu!(BA₂)}', False)]
    
    for source, target, det in pairs:

        output = XT.unify_determinatives(source, lower=det)
        output = XT.subscribe_indices(output)
        output = XT.accent_to_index(output)

        if output == target:
            status[0] += 1
        else:
            status[1] += 1
            print(f'>fail: {source} \t {output} \t {target}')

    if not status[1]:
        print(f'> All {status[0]} tests passed')
    else:
        print(f'> {status[1]} tests failed out of {status[0]+status[1]}')

        
#unit_test()
