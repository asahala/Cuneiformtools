#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import Counter
import json
import re
import cuneiformtools as ct
import ogsl
from alphabet import AA as AA_signlist

def readfile(filename):
    with open(filename, 'r', encoding="utf-8") as data:
        return data.read().splitlines()

def write_json(filename, data):
    with open(filename, 'w', encoding="utf-8") as fp:
        json.dump(data, fp)

def read_json(filename):
    with open(filename, 'r', encoding="utf-8") as data:
        return json.load(data)

def parse(vrt_file, verbose=False):

    def count_attested():
        pass

    OGSL = ogsl.Signs()
    sign_dict = {}

    i = 0

    oracc = readfile(vrt_file)
    for line in oracc:

        if i in range(0, len(oracc), 5000) and verbose:
            print(i, '/', len(oracc))
        
        if line.startswith('<text'):
            period = re.sub('.+period="(.+?)".+', r'\1', line)

        if not line.startswith('<'):
            data = line.split('\t')
            xlit = data[0]
            lang = data[8]
            sense = data[5]

            identifier = "%s|%s" % (lang, period)
            sign_dict.setdefault(identifier, {})
            signs = ct.Tokenizer().separate(xlit)
            
            for s in signs:
                if s in ('x', 'X', 'x.x'):
                    pass
                else:
                    if s.islower():
                        key = OGSL.get_name(s)
                    else:
                        key = s

                    if key is not None:
                        sign_dict[identifier].setdefault(key, []).append(s)
        i += 1

    """ Count sign frequencies """
    for identifier, signlist in sign_dict.items():
        for name, values in signlist.items():
            sign_dict[identifier][name] = Counter(sign_dict[identifier][name])

    #write_json('oracc-sign-distribution.json', sign_dict)

def build_signlist(language, period, sign_names):
    data = read_json('oracc-sign-distribution.json')

    def reformat_freqs(freqs):
        if freqs is not None:
            freqs = ["%s (%i)" % (value, freq) for value, freq in
                     sorted(freqs.items(), reverse=True,
                            key=lambda item: item[1])]
        else:
            freqs = []
        return '; '.join(freqs)

    def reformat_values(values):
        if values is not None:
            values = ct.CuneiformSorter().sort(list(values.keys()))
        else:
            values = []
        return '; '.join(values)
            
    for identifier, signlist in data.items():
        lang, per = identifier.split('|')
        if (language == lang or language == "any") and\
           (period == per or period == "any"):
            for sign in sign_names:
                content = signlist.get(sign, None)
                frequencies = reformat_freqs(content)
                values = reformat_values(content)

                print('%s\t%s\t%s' % (sign, values, frequencies))
                
                #values = ct.CuneiformSorter().sort(list(signlist[sign].keys()))
                #print(values)

build_signlist('arc', 'Achaemenid', AA_signlist)

#parse('ORACC.VRT')


"""
        
    

x = read_json('oracc-sign-distribution.json')
for k, v in x.items():
    if k.startswith('elx'):
        print(k.split('|'))
        freqs = x[k].get('DA', {})
        vals = list(x[k].get('DA', {'_': '_'}).keys())
        print(freqs)
        print(ct.CuneiformSorter().sort(vals))
        print('\n')"""
