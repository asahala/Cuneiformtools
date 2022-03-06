import time
import re
import cuneiformtools.ogsl as ogsl
import cuneiformtools.util as util
import cuneiformtools.norm as norm

a = ogsl.get_readings('DA', sort=False)
#print(a)




#a = ogsl.get_name('kar')
#print(a)


#x = util.sort([('a3', '[unk]'), ('a', 'water'), ('a₂', 'arm')], sort_index=1)

#a = ogsl.get_homophones('e', sort_by='reading', sort=True)
#print(a)


#a = ogsl.get_abstract('*C:*C:*', sort_by='name', sort=True)


#a = ogsl.contains_sign('AN', position='final')

#a = ogsl.get_number('AN')
#print(a)

a = util.sort({'a': '1'})
print(a)


i = 0
while i < 1:
    a = ogsl.get_signs('{ŋeš}numun₂-na')
    i += 1


""" =========================================================
=== Some tests for various tools ============================
========================================================= """


def eval_(source, target, output):

    if output == target:
        return 0
    print('-----------------------------')
    print(source, target, output, sep='\n')
    return 1

def msg(errors, tests):
    if not errors:
        print(f'   All {tests} tests passed')
    else:
        print(f'   {errors} tests failed out of {tests}')
    

def unit_test_norm():

    print('> Testing harmonize_all()')
    pairs = [('lu-lú-lùl-sa4', 'lu-lu₂-lul₃-sa₄', True),
             ('lu-lú-[lù]l-sa44', 'lu-lu₂-[lu]l₃-sa₄₄', True),
             ('lu-lú(|DUR6.Á|)-lùl#-sa14', 'lu-lu₂(|DUR₆.A₂|)-lul₃#-sa₁₄', True),
             ('lu-lú(|DÚR+Á|){KI}-lùl-sa4', 'lu-lu₂(|DUR₂+A₂|){ki}-lul₃-sa₄', True),
             ('lu-l[ú(|DÚR%%Á|)-lù]l-sa4', 'lu-l[u₂(|DUR₂%%A₂|)-lu]l₃-sa₄', True),
             ('lu111-lu2(|DUR2%%Á|)-lul3-sa4', 'lu₁₁₁-lu₂(|DUR₂%%A₂|)-lul₃-sa₄', True),
             ('lu#-lú(|DÚR×Á.U|)-{URÙDA}lùl-sa4', 'lu#-lu₂(|DUR₂×A₂.U|)-{uruda₃}lul₃-sa₄', True),
             ('lu-{[d]}lú(|DUR6×Á|)-lùl-sa4#', 'lu-{[d]}lu₂(|DUR₆×A₂|)-lul₃-sa₄#', True),
             ('<lú(|DU16%%DU3|)>-{t[ú]g}lùl{+lu-ul}', '<lu₂(|DU₁₆%%DU₃|)>-{t[u]g₂}lul₃{+lu-ul}', True),
             ('{D}30', '{d}30', True),
             ('60-x', '60-x', True),
             ('EN+60', 'EN+60', True),
             ('6.4.0.1(DIŠ)', '6.4.0.1(DIŠ)', True),
             ('{M}da-da', '{M}da-da', False),
             ('{F}da-da', '{f}da-da', True),
             ('f.da-da', '{f}da-da', True),
             ('m.da-d.da{+da-a} [...]-a{KI}', '{m}da-{d}da{+da-a} [...]-a{ki}', True),
             ('f.am.mu.ud.da', '{f}am.mu.ud.da', True),
             ('f.am.mu.ud.d.da', '{f}am.mu.ud.{d}da', True),
             ('f.am.mu3.ud44.d.da', '{f}am.mu₃.ud₄₄.{d}da', True),
             ('{1}da-da0', '{m}da-da₀', True),
             ('{M}{d}da-da', '{m}{d}da-da', True),
             ('kirix(|DA.DU|)-{d}MÚ{+mu!(BÁ)}', 'kiriₓ(|DA.DU|)-{d}MU₂{+mu!(BA₂)}', True),
             ('{dug}kirix(|DA.DU|){KI}-{d}MÚ{+mu!(BÁ)}', '{DUG}kiriₓ(|DA.DU|){KI}-{d}MU₂{+mu!(BA₂)}',
              False),
             ('á-ma %eg ($ERASURE$) nà{KI} ra-a!(|Á.DÙ|)', 'a₂-ma %eg ($ERASURE$) na₃{ki} ra-a!(|A₂.DU₃|)', True),
             ('á#-nà#{ki2#}', 'a₂#-na₃#{ki₂#}', True),
             ('MIN<(á-dá)> {{ná}} {{KA}} DU3*-mú*-<<á>>', 'MIN<(a₂-da₂)> {{na₂}} {{KA}} DU₃*-mu₂*-<<a₂>>', True),
             ('GÁN@t GÁN@g GÁN@v GÁN+GÁN GÁN&GÁN', 'GAN₂@t GAN₂@g GAN₂@v GAN₂+GAN₂ GAN₂&GAN₂', True)]

    tests = len(pairs)
    errors = 0
    
    for source, target, det in pairs:
        output = norm.harmonize_all(source, lower_dets=det)
        errors += eval_(source, target, output)
    msg(errors, tests)


def unit_test_bracket():

    b = norm.BracketMover()

    print('> Testing move_brackets() legacy half-brackets')
    pairs = [('l[u-lu₂-l]u[l₃-s]a₄', '[lu-lu₂-lul₃-sa₄]'),
             ('lu-l[u₂!](DU)-[lul₃-s]a₄₄', 'lu-[lu₂!(DU)]-[lul₃-sa₄₄]'),
             ('lu-[l]u₂(|DUR₆.A₂|)-[l]u[l₃]-sa₁₄', 'lu-[lu₂(|DUR₆.A₂|)]-[lul₃]-sa₁₄'),
             ('lu-[l]ú(|DUR6.Á|)-[l]ù[l]-sa14', 'lu-[lú(|DUR6.Á|)]-[lùl]-sa14'),
             ('lu-lu₂(|DUR₂+A₂|){k[i]}-lul₃-sa₄', 'lu-lu₂(|DUR₂+A₂|){[ki]}-lul₃-sa₄'),
             ('lu-l[u₂(|DUR₂%%A₂|)-lul₃-s]a₄', 'lu-[lu₂(|DUR₂%%A₂|)-lul₃-sa₄]'),
             ('l[u₁₁₁.l]u₂(|DUR₂.A₂|)-lul₃-sa₄', '[lu₁₁₁.lu₂(|DUR₂.A₂|)]-lul₃-sa₄'),
             ('lu-l[u₂(|DUR₂×A₂.U|)-{uru]da₃}lul₃-sa₄', 'lu-[lu₂(|DUR₂×A₂.U|)-{uruda₃]}lul₃-sa₄'),
             ('a-[(na ba)]-b[a %eg <ka> n]a*', 'a-[(na ba)]-[ba %eg <ka> na*]'),
             ('lug⸢al MIN<(lugal)> %eg $ERASURE$ ga⸣l!(SAL)', '⸢lugal MIN<(lugal)> %eg $ERASURE$ gal!(SAL)⸣'),
             ('lug⸢al MI⸣N<(lugal)> %eg $ERASURE$ gal!(SAL)', '⸢lugal MIN<(lugal)>⸣ %eg $ERASURE$ gal!(SAL)'),
             ('lug⸢al {{a i u⸣ e}} $ERASURE$ gal!(SAL)', '⸢lugal {{a i u⸣ e}} $ERASURE$ gal!(SAL)')]

    tests = len(pairs)
    errors = 0
    for source, target in pairs:
        output = b.move_brackets(source)
        errors += eval_(source, target, output)
    msg(errors, tests)

    print('> Testing move_brackets() hashed half-brackets')
    pairs = [('l[u-lu₂-l]ul₃-⸢sa₄ %es ma⸣-al', '[lu-lu₂-lul₃]-sa₄# %es ma#-al'),
             ('lu-l⸢u₂!⸣(DU)-[lul₃-s]a₄₄', 'lu-lu₂!(DU)#-[lul₃-sa₄₄]'),
             ('lu-[l]u₂(|DUR₆.A₂|)-⸢lu⸣l₃-sa₁₄', 'lu-[lu₂(|DUR₆.A₂|)]-lul₃#-sa₁₄'),
             ('lu-lu₂(|DUR₂+A₂|){k⸢i⸣}-lu[l₃-s]a₄', 'lu-lu₂(|DUR₂+A₂|){ki#}-[lul₃-sa₄]'),
             ('lu-l⸢u₂(|DUR₂%%A₂|)-lul₃-s⸣a₄', 'lu-lu₂(|DUR₂%%A₂|)#-lul₃#-sa₄#'),
             ('l[u₁₁₁.l]u₂(|DUR₂.A₂|)-⸢lu⸣l₃-sa₄⸣', '[lu₁₁₁.lu₂(|DUR₂.A₂|)]-lul₃#-sa₄'),
             ('lu-l⸢u₂(|DUR₂×A₂.U|)-{uru⸣da₃}lul₃-sa₄', 'lu-lu₂(|DUR₂×A₂.U|)#-{uruda₃#}lul₃-sa₄'),
             ('lug⸢al MIN<(lugal)> %eg $ERASURE$ ga⸣l!(|SAL.DI|)', 'lugal# MIN<(lugal)># %eg $ERASURE$ gal!(|SAL.DI|)#'),
             ('lug⸢al MI⸣N<(lugal)> %eg $ERASURE$ gal!(SAL)', 'lugal# MIN<(lugal)># %eg $ERASURE$ gal!(SAL)'),
             ('lug⸢al {{a i⸣ u e}} $ERASURE$ gal!(SAL)', 'lugal# {{a# i# u e}} $ERASURE$ gal!(SAL)'),
             ('lúg⸢al {{a è⸣ u e}} $ERASURE$ gal!(SAL)', 'lúgal# {{a# è# u e}} $ERASURE$ gal!(SAL)'),
             ('lu-l⸢ú!⸣(DU)-[lùl-s]a44', 'lu-lú!(DU)#-[lùl-sa44]'),]

    tests = len(pairs)
    errors = 0
    for source, target in pairs:
        output = b.move_brackets(source, hash_notation=True)
        errors += eval_(source, target, output)
    msg(errors, tests)


def unit_test_replace():

    b = norm.BracketMover()

    print('> Testing transducer(sign=False)')
    pairs = [('inana', 'inannak', '{d}ina[na]', '{d}inann[ak]'),
             ('an ', 'AN ', 'a[n su₃]', 'A[N su₃]'),
             ('an sù', 'dingir sud', 'a[n! sù]', 'di[ngir! sud]'),
             ('an sù', 'dingir sud', 'a[n] sù', 'di[ngir] sud'),
             ('an sù', 'dingir sud', '[an] sù', '[dingir] sud'),
             ('dingir', 'an', 'din[gir! sud]', 'a[n! sud]'),
             ('{DIŠ}', '{m}', '{D[IŠ}b]a-ba {DIŠ#}ba-ba', '{[m}b]a-ba {m#}ba-ba'),
             ('NAM LUGAL-LA', 'NAM-LUGAL-LA', 'NAM? LU[GAL]-LA#', 'NAM?-LU[GAL]-LA#'),
             ('dù', 'rú', 'mu-[na-d]ù!(NI)', 'mu-[na-r]ú!(NI)'),
             ('zir', 'zi', 'zir#(|DI.DA|)-do', 'zi#(|DI.DA|)-do'),
             ('zir', 'zi', 'z[ir(|DI.DA|)]-do', 'z[i(|DI.DA|)]-do'),
             ('en {d}MUŠ', 'umun {d}inanna', 'e[n? {d}M]UŠ', 'um[un? {d}inan]na')]

    tests = len(pairs)
    errors = 0
    
    for rs, rt, input_, target in pairs:
        #input_ = (b.move_brackets(input_))
        output = util.replace(rs, rt, input_, ignore='?!#*')
        errors += eval_(input_, target, output)
        
    msg(errors, tests)

    print('\n> Testing transducer(sign=True)')
    pairs = [('inana', 'inannak', '{d}ina[na]', '{d}inann[ak]'),
             ('an', 'AN', 'a[n su₃]', 'A[N su₃]'),
             ('an', 'dingir', 'a[n! sù]', 'din[gir! sù]'),
             ('dingir', 'an', 'din[gir! sud]', 'a[n! sud]'),
             ('DU', 'kurₓ(DU)', 'e₂-[a mu-na-D]U', 'e₂-[a mu-na-kurₓ(DU)]')]

    tests = len(pairs)
    errors = 0
    
    for rs, rt, input_, target in pairs:
        #input_ = (b.move_brackets(input_))
        output = util.replace(rs, rt, input_, sign=True, ignore='?!#*')
        errors += eval_(input_, target, output)
        
    msg(errors, tests)

    def broken_tele():
        """ Broken telephone test """
        pairs = [('ri-mut', 'lullu lellu'),
                 ('kur', 'mâtu'),
                 ('ban', 'ping'),
                 ('ša₂', 'šušu')]

        xlit = '[ša₂ {m}ri]-mut* A-šu₂? ša₂# {m}ku[r-ba]n-{d}AMAR-UTU'
        print('\n')
        print(xlit)
        for rs, rt in pairs:
            #input_ = (b.move_brackets(input_))
            xlit = util.replace(rs, rt, xlit, ignore='?!#*')
            print(rs, rt, xlit, sep='\t')    

    def check_chunker():
        """ Sanity check for chunking algorith;
        if silent, all is well. """
        i = 1
        while i < 60:
            s = 'a'*i
            j = 1
            while j < 120:
                t = 'j'*(j+i)
                j += 1
                util.replace(s, t, '')
            i += 1

    #check_chunker()
    #broken_tele()
                

    
#unit_test_norm()  
#unit_test_bracket()
#unit_test_replace()


def unit_test_zip():

    pairs = [('l[u-lu₂-l]ul₃-sa₄-[...-a]', '[lu-lu₂-lul₃]-<<ZU:AB>>'),
             ('lu-l[u₂!](DU)-[lul₃-s]a₄₄', '{f}{d}lu-[lu₂!(DU)]-[lul₃-sa₄₄]-[...-a]'),
             ('lu-[l]u₂(|DUR₆.A₂|)-lul₃#-sa₁₄{+sa-a}', 'lu-[lu₂(|DUR₆.A₂|)]-lul₃#-sa₁₄{+sa-a}'),
             ('lu-lu₂(|DUR₂+A₂|){k[i]}-lul₃-sa₄', 'lu-lu₂(|DUR₂+A₂|){[ki]}-lul₃-sa₄'),
             ('lu-l[u₂(|DUR₂%%A₂|)-lul₃-s]a₄', 'lu-[lu₂(|DUR₂%%A₂|)-lul₃-sa₄]'),
             ('l[u₁₁₁.l]u₂(|DUR₂.A₂|)-lul₃-sa₄', '[lu₁₁₁.lu₂(|DUR₂.A₂|)]-lul₃-sa₄'),
             ('lu-l[u₂(|DUR₂×A₂.U|)-{uru]da₃}lul₃-sa₄', 'lu-[lu₂(|DUR₂×A₂.U|)-{uruda₃]}lul₃-sa₄')]
    
    for source, target in pairs:
        a, b = util.unzip_xlit(target)
        print(target == util.zip_xlit(a, b))
        #print(target, util.zip_word(a,b), sep='\n')
        
#unit_test_zip()



