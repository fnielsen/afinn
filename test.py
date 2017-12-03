# -*- coding: utf-8 -*-
import sys
from afinn import Afinn

# https://stackoverflow.com/questions/6625782
if sys.version_info[0] == 2:
    import codecs

    u = lambda s: codecs.unicode_escape_decode(s)[0]
elif sys.version_info[0] == 3:
    u = lambda s: s

afinn = Afinn(language='tr')
score = afinn.score('kar')
print score

score = afinn.score(u('\xe7ok iyi'))
print score

print u('i\u011Fren\u00E7')
print u('\xe7ok k\xf6t\xfc')
score = afinn.score(u('\xe7ok k\xf6t\xfc'))
print score
