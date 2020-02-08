#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
import re
import cuneiformtools as ct
import ogsl
from alphabet import ASCII_INDEX

"""
Aleksi Sahala 2020

Script for collecting data from various corpora for building
sign lists. 

"""

class Reformatter:

    """ General tools for harmonizing sign lists with OGSL """

    def __init__(self):
        self.psl_index = [('<sub>%s</sub>' % chr(k), chr(v))
                          for k, v in ASCII_INDEX.items()]
        self.psl_chars = [('&amp;', '&'), ('ĝ', 'ŋ')]

    def html_to_unicode(self, string):
        for source, target in self.psl_index + self.psl_chars:
            string = string.replace(source, target)
        return string


def readfile(filename):
    with open(filename, 'r', encoding="utf-8", errors="replace") as data:
        return data.read().splitlines()

def writefile(filename, content):
    with open(filename, 'wb') as data:
        data.write(content)   

def download(url, filename):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '\
                 'AppleWebKit/537.36 (KHTML, like Gecko) '\
                 'Chrome/35.0.1916.47 Safari/537.36'
    request = urllib.request.Request(url,
            headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(request)
    html = response.read()
    writefile(filename, html)


""" OBSOLETE:
Fetch and parse PSL list from ePSD and harmonize it with
the OGSL to find signs and values that are not in OGSL.
OGSL seems to have all PSL data except:

|ANŠE.IGI.DIB|        <dusuₓ> not found from OGSL
|ANŠE.KUR|            <sisiₓ> not found from OGSL
|URUDA.IŠ.URUDA|      <šeknuₓ> not found from OGSL

"""

rf = Reformatter()
OGSL = ogsl.Signs()
PSL =  {}

def parse_epsd(filename):
    for line in readfile(filename):
        line = line.lstrip()
        if '<title>' in line:
            s = line.replace('<title>', '').replace('</title>', '')
            sign_name = rf.html_to_unicode(s)
            PSL.setdefault(sign_name, [])
        if '<span class="psl-ahead">' in line:
            s = re.sub('.*?<span.+?>(.+?)<\/span>.*', r'\1', line)
            reading = rf.html_to_unicode(s)
            reading = reading.replace('(%s)' % sign_name, '')

            r1 = (OGSL.get_name(reading))
            if r1 is None:
                print('\n' + sign_name)
                print("<%s> not found from OGSL" % reading)
                ogsl_readings = OGSL.get_values(sign_name)
                if ogsl_readings is not None:
                    for x in ogsl_readings:
                        if ct.remove_index(reading) == ct.remove_index(x):
                            print("Sign %s in PSL <%s> --> OGSL <%s>" \
                                  % (sign_name, reading, x))
                print('\n')
                
            PSL.setdefault(sign_name, []).append(reading)

""" Collect sign lists from ePSD """
def scrape_epsd():
    epsd = readfile('source-epsd-signlist.txt')
    for url in epsd:
        print(url)
        filename = re.sub('http.+brief\/', '', url)
        download(url, './psl/' + filename)
        parse_epsd('./psl/' + filename)

#scrape_epsd()
