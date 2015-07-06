"""Test of afinn."""

import sys

from afinn import Afinn

# https://stackoverflow.com/questions/6625782
if sys.version_info[0] == 2: 
    import codecs
    u = lambda s: codecs.unicode_escape_decode(s)[0]
elif sys.version_info[0] == 3:
    u = lambda s: s


def test_afinn():
    afinn = Afinn()
    assert isinstance(afinn, Afinn)


def test_find_all():
    afinn = Afinn()
    words = afinn.find_all("It is so bad")
    assert words == ['bad']


def test_score():
    afinn = Afinn()
    score = afinn.score('bad')
    assert score < 0


def test_score_language(language='en'):
    afinn = Afinn()
    score = afinn.score('bad')
    assert score < 0


def test_unicode():
    afinn = Afinn()
    score = afinn.score(u('na\xefve'))
    assert score < 0

