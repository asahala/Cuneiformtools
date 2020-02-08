#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Aleksi Sahala 2020 -- Assyriological alphabet definitions """

mixed_uppercase = False # set True to aAbB order instead of abAB

""" Define custom alphabetic order for Assyriological symbols.
If you encounter errors while sorting, add new characters here. """

NONALPHANUMERIC = "×!@#&%()–-_[{}].:;',?/\*`~$^+=<>“⁻ "
ZERO = 'Ø'
NUMERIC = "0123456789"
INDEX = "₀₁₂₃₄₅₆₇₈₉"
X_INDEX = "ₓ"
ALEPH = "ʾˀ"
ALPHA = "aáàâābcdeéèêēfgĝŋhḫiíìîījklmnoóòōôpqrřȓsšṣtṭuúùûūvwxyz"
PIPE = '|'
ALLNUMBERS = ''.join([j for i in zip(list(NUMERIC), list(INDEX)) for j in i])

if mixed_uppercase:
    ALLALPHA = ''.join([j for i in zip(list(ALPHA), list(ALPHA.upper())) for j in i])
else:
    ALLALPHA = ALPHA + ALPHA.upper()
        
ALPHABET = NONALPHANUMERIC + ZERO +\
           ALLNUMBERS + X_INDEX + ALEPH + ALLALPHA + PIPE

""" Define index remover """
INDICES = INDEX + X_INDEX
REMOVE_INDEX = str.maketrans(INDICES, "_"*len(INDICES))

""" Define index ASCIIfier """
ASCII_INDEX = str.maketrans(NUMERIC + 'x', INDEX + X_INDEX)

""" Adam Anderson Sign list order """
AA = ["A", "A₂", "AB", "|AB×AŠ₂|", "AB₂", "AD", "ZA@t", "AK", "|NINDA₂×NE|",
      "DUN₃@g@g", "|IGI.DUB|", "|HI×NUN|", "|GAD.TAK₄.SI|", "", "AL", "ALAN",
      "|GIR₃×(A.IGI)|", "|GUD×KUR|", "|GA₂×AN|", "AMAR", "|DAG.KISIM₅×(LU.MAŠ₂)|",
      "AN", "ANŠE", "APIN", "|IGI.RI|", "ARAD", "|ARAD×KUR|", "|GA₂×SAL|",
      "AŠ", "", "AŠ₂", "6(DIŠ)", "|URU×IGI|", "AŠGAB", "|EZEN×LAL₂|", "|EZEN×A|",
      "|PIRIG×ZA|", "BA", "BAD", "|EZEN×BAD|", "BAHAR₂", "BAL", "BALAG", "1(BAN₂)",
      "|URU×URUDA|", "BAR", "BARA₂", "BI", "NE@s", "|HI×ŠE|", "BU", "|BU&BU.AB|",
      "|LAGAB×(U.U.U)|", "BULUG", "|PAP.PAP|", "|KA×IM|", "BUR", "BUR₂", "|EN×GAN₂@t|",
      "BURU₅", "DA", "DAG", "|MU&MU|", "|MAŠ.GU₂.GAR₃|", "DAM", "|GA₂×GAN₂@t|", "DAR",
      "DARA₃", "DARA₄", "|UMUM×KASKAL|", "DI", "DIB", "|SAG×ŠID|", "DIM", "LU₂@s",
      "|MA₂.MUG|", "DIN", "|SI.A|", "DIŠ", "DU", "LAGAR@g", "", "DUB", "DUB₂", "DUG",
      "DUGUD", "|U.TUG₂|", "SAG@g", "DUN₄", "DUN₄", "|GU₂×KAK|", "E", "E₂", "EDIN",
      "|SAL.EŠ₂|", "EGIR", "EL", "|KA×ME|", "EN", "|LAGAB×HAL|", "EREN", "ERIN₂",
      "|URU×GAR|", "|U.U.U|", "|DIŠ.DIŠ.DIŠ|", "|AŠ.AŠ.AŠ|", "|GA₂×ŠE|", "",
      "|LAGAB×KUL|", "EZEN", "|EZEN×GUD|", "|EZEN×KU₃|", "|EZEN×LA|", "GA", "GA₂",
      "GABA", "GAD", "KAK", "|U.DIM×ŠE|", "|U.DIM|", "GAL", "GALAM", "|GA₂×GAR|",
      "GAM", "KAM₄", "GAN", "GAN₂", "|GA₂×NUN|", "GA@g", "GAR₃",
      "|(ŠE.NUN&NUN)&(ŠE.NUN&NUN).GAD&GAD.GAR&GAR|", "|GUM×ŠE|", "|SAL.KUR|",
      "GEŠTIN", "GI", "GI₄", "|ŠU₂.AŠ₂|", "GIDIM", "GIG", "|LU₂@LU₂|", "|LAGAB×BAD|",
      "|GI%GI|", "DIM₂", "DUN₃@g", "HA@g", "|GIR₃×GAN₂@t|", "GIR₂", "GIR₃", "|U.AD|",
      "GIŠ", "GISAL", "|URU×MIN|", "GU", "GU₂", "GUD", "|KA×GAR|", "|HI×NUN.ME|", "|ZA.GUL|",
      "LU₃", "GUL", "GUR", "GUR₇", "TE@g", "GURUN", "HA", "|KI×U|", "HAL", "|HI×AŠ₂|", "MA@g",
      "HI", "|HI×(U.U.U)|", "|HI×(U.U)|", "|HI×U|", "HU", "|HUB₂×UD|", "HUB₂", "|IGI.UR|", "HUL₂",
      "|HI.GIR₃|", "I", "|I.A|", "5(DIŠ)", "IB", "|GU₂.GAR₃|", "IG", "IGI", "IL", "IL₂", "ILIMMU",
      "|KASKAL.KUR|", "IM", "IMIN", "IN", "IR", "IŠ", "|UD×(U.U.U)|", "|GA₂×MI|", "KA", "|KA×BALAG|",
      "|KA×GA|", "|KA×GAN₂@t|", "|KA×NE|", "|KA×SAR|", "|KA×ŠE|", "|KA×EŠ₂|", "|KA×ŠID|", "KA₂", "KAB",
      "KAD₂", "KAD₃", "KAD₄", "KAD₅", "KAL", "|HI×BAD|", "|TE.A|", "GAN₂@t", "|UŠ×A|", "DU@s",
      "KASKAL", "KASKAL", "|KA×(AD.KU₃)|", "", "", "|KA×GUR₇|", "", "", "|KA×GIŠ%GIŠ|",
      "", "|KA×PI|", "|KA×RU|", "|KA×LI|", "", "|KA×U₂|", "|KA×UD|", "|KA×UŠ|",
      "|ŠU₂.AN.HI×GAD|", "KEŠ₂", "KI", "|GIŠ%GIŠ|", "KID", "TAK₄", "KIN",
      "|GAD&GAD.GAR&GAR|", "|AB₂×GAN₂@t|", "KIŠ", "KISAL", "SAG@n", "|DAG.KISIM₅×(U₂.GIR₂)|",
      "|DAG.KISIM₅×(U₂.GIR₂)|", "KU", "KU₄", "KU₇", "KU₃", "GUM", "KUN", "|ŠU₂.3×AN|", "|ŠU₂.AN|",
      "KUR", "|U.PIRIG|", "KUŠU₂", "LA", "LAGAB", "", "LAGAR", "|DU&DU|", "|NUNUZ.AB₂×LA|", "LAL",
      "", "|TA×HI|", "LAM", "LI", "|IGI.EŠ₂|", "|AB₂×ŠA₃|", "LIL", "LIMMU", "LIMMU₂", "LIŠ", "LU",
      "LU₂", "|LU₂×BAD|", "|LU₂×GAN₂@t|", "|LU₂×NE|", "", "LUGAL", "LUH", "LUL", "LUM", "MA", "MA₂",
      "MAH", "|U.U|", "MAR", "MAŠ", "MAŠ₂", "|PA.DU|", "ME", "|AK×ERIN₂|", "|GA₂×(ME.EN)|", "MES",
      "|ME.U.U.U|", "MI", "MIN", "DUN₃@g@g", "MU", "|HU.HI|", "MUG", "|3×AN|", "|DIM×ŠE|", "MUNSUB",
      "SAL", "|SAL.HUB₂|", "MURGU₂", "MURUB₄", "MUŠ", "MUŠ₃@g", "MUŠ₃", "NA", "NA₂", "|NI.UD|",
      "|KA×A|", "NAGA", "NAGA", "NAGAR", "NAM", "NE", "NI", "|NI.TUK|", "|SAL.UR|", "GAR",
      "|LAGAB.LAGAB|", "NIM", "4(U)", "|SAL.TUG₂|", "|SAL.KU|", "|AB×HA|", "NINDA₂",
      "|LAGAB×GAR|", "|U&U.U&U.U|", "|NUN&NUN|", "NISAG", "NU", "KUL", "|ZI&ZI.LAGAB|",
      "NUN", "TAK₄", "", "NUN@t", "|KA×NUN|", "NUNUZ", "PA", "|PAP.E|", "|PAP.IŠ|", "PAD",
      "|IGI.RU|", "PAN", "PAP", "PEŠ₂", "|ŠA₃×A|", "PI", "PIRIG", "|KA×GAN₂@t|", "|PAP.HAL|",
      "RA", "LUGAL", "RI", "|MUŠ%MUŠ.A.NA|", "RU", "SA", "ŠA", "", "ŠA₃", "|ŠA₃×TUR|",
      "|HU.NA₂|", "ŠA₆", "SAG", "|SAG×KAK|", "|U.GAN|", "|U.SAG|", "ŠUBUR", "|URU×GA|",
      "|NINDA₂×ŠE|", "ŠANABI", "SAR", "|LAGAB×IGI@g|", "ŠE", "|ŠE.NAGA|", "EŠ₂",
      "|MUŠ₃.DI|", "ŠEG₉", "ŠEN", "ŠEŠ", "|ŠEŠ.KI|", "ŠEŠLAM", "SI", "|U.EN×GAN₂@t|",
      "ŠID", "SIG", "SIG₄", "|IGI.ERIN₂|", "IGI@g", "SIK₂", "SILA₃", "|GA₂×PA|",
      "|NUN.LAGAR×SAL|", "ŠIM", "|ŠIM×KUŠU₂|", "|ŠIM×GAR|", "ŠINIG", "ŠIR", "EZEN",
      "", "|AMAR×ŠE|", "ŠITA", "ŠITA₂", "SUD₂", "|U.KID|", "SU", "ŠU", "", "ŠU₂",
      "SI@g", "|KA×SA|", "|LAGAR×ŠE|", "ŠUBUR", "SUD", "|KA×ŠU|", "|LAGAB×A|",
      "|GU%GU|", "SUHUR", "DU@g", "GALAM", "DUN", "SUM", "SUR", "|HI×AŠ|", "SUR₉",
      "|LAGAB×(GUD&GUD)|", "ŠUŠANA", "TA", "TAB", "TAG", "|TAG×ŠU|", "TAR", "TE", "TI",
      "|ŠE.NUN&NUN|", "TU", "|KA×LI|", "TUG₂", "TUK", "|LAGAB×U|", "TUM", "|NIM×GAN₂@t|",
      "DUN₃", "TUR", "|NUN.LAGAR|", "U", "U₂", "|IGI.DIB|", "|HU.SI|", "|IGI.E₂|",
      "|LAGAB×(GUD&GUD)|", "UB", "|EZEN×KASKAL|", "|DAG.KISIM₅×GA|", "|DAG.KISIM₅×LU|",
      "UD", "UDUG", "|U.MU|", "|PIRIG×UD|", "|U.KA|", "|U.DAR|", "|UD.KUŠU₂|",
      "|URU×BAR|", "|URU×BAR|", "|LAL₂.DU|", "|U.GUD|", "UM", "|UM.ME|", "UMBIN",
      "|ŠID×A|", "UN", "AB@g", "UR", "UR₂", "|UR₂×NUN|", "|UR₂×U₂|", "|GA₂×NUN&NUN|",
      "UR₄", "|UR%UR|", "URI", "URI₃", "URU", "|URU×A|", "|URU×GU|", "|URU×GAN₂@t|",
      "|URU×TU|", "URUDA", "|AB×GAL|", "|URU×HA|", "|URU×ŠE|", "UŠ", "|UŠ×TAK₄|",
      "|KA×BAD|", "|GU₂×NUN|", "|NUNUZ.AB₂×AŠGAB|", "8(DIŠ)", "|LAL₂.SAR|", "|U.GA|",
      "|ŠE.HU|", "UZ₃", "UZU", "ZA", "|UD.KA.BAR|", "MUG@g", "ZAG", "|A×HA|",
      "|LAGAB×SUM|", "ZI", "", "|ZI&ZI.A|", "", "ZE₂", "ZIG", "ZU", "ZUM"]
