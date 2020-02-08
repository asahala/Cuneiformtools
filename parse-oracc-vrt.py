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
    """ Build sign list from Oracc data containing separate
    lists for different dialects and time periods """

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

def build_signlist(languages=[], periods=[], sign_names=[]):
    """ Build sign list based on Oracc data that follows a
    given sign order for [languages] and [periods] for
    [sign_names]; if let empty, will combine all """

    data = read_json('oracc-sign-distribution.json')

    combined_list = {}

    def reformat_freqs(freqs):
        """ Reformat frequencies to ´value (freq)´ strings """
        if freqs is not None:
            freqs = ["%s (%i)" % (value, freq) for value, freq in
                     sorted(freqs.items(), reverse=True,
                            key=lambda item: item[1]) if value]
        else:
            freqs = []
        return '; '.join(freqs)

    def reformat_values(values):
        """ Reformat sign lists into strings """
        if values is not None:
            values = ct.CuneiformSorter().sort(list(values.keys()))
        else:
            values = []
        return '; '.join(values)

    def merge_dict(dict1, dict2):
       ''' Merge dictionaries and sum the sign frequencies '''
       combined = {**dict1, **dict2}
       for key, value in combined.items():
           if key in dict1 and key in dict2:
               combined[key] = value + dict1[key]
       return combined

    for identifier, signlist in data.items():
        lang, per = identifier.split('|')
        if (lang in languages or not languages) and\
           (per in periods or not periods):
            for sign in signlist.keys():
                content = signlist.get(sign, {})
                combined_list.setdefault(sign, {})
                combined_list[sign] = merge_dict(combined_list[sign], content)
                #combined_list.setdefault(sign, {'values': [], 'freqs': {}})
                  #combined_list[sign]['values'].extend(content)
                #combined_list[sign]['values'].extend(content)
                
                #print('%s\t%s\t%s' % (sign, values, frequencies))

    for sign in sign_names:
        content = combined_list.get(sign, {})
        values = reformat_values(content)
        freqs = reformat_freqs(content)
        print('%s\t%s\t%s' % (sign, values, freqs))

        
build_signlist(['akk-x-midbab', 'akk-x-mbperi-949', 'akk-x-mbperi'], [], AA_signlist)

#parse('ORACC.VRT', verbose=True)


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
