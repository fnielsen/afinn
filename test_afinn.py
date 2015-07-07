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


def test_split():
    afinn = Afinn()
    words = afinn.split('Hello, World')
    assert words == ['Hello', 'World']

    words = afinn.split(u('Hell\xf8, \xc5rld'))
    assert words == [u('Hell\xf8'), u('\xc5rld')]


def test_score():
    afinn = Afinn()
    score = afinn.score('bad')
    assert score < 0

    score = afinn.score('')
    assert score == 0.0



def test_score_language():
    afinn = Afinn(language='en')
    score = afinn.score('bad')
    assert score < 0

    afinn = Afinn('en')
    score = afinn.score('bad')
    assert score < 0


def test_unicode():
    afinn = Afinn()
    score = afinn.score(u('na\xefve'))
    assert score < 0


def test_danish():
    afinn = Afinn(language='da')
    score = afinn.score('bedrageri')
    assert score < 0

    score = afinn.score(u('besv\xe6r'))
    assert score < 0


def test_score_with_pattern():
    afinn = Afinn(language='da')
    score = afinn.score('ikke god')
    assert score < 0

    score = afinn.score('ikke god.')
    assert score < 0

    score = afinn.score('IKKE GOD-')
    assert score < 0

    score = afinn.score('ikke   god')
    assert score < 0

    score = afinn.score('En tv-succes sidste gang.')
    assert score > 0

    score = afinn.score('')
    assert score == 0.0


def test_score_with_wordlist():
    afinn = Afinn()
    score = afinn.score('Rather good.')
    assert score > 0

    score = afinn.score('Rather GOOD.')
    assert score > 0


def test_score_with_wordlist_empty():
    afinn = Afinn()
    score = afinn.score('')
    assert score == 0.0
