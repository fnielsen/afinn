afinn
=====

AFINN sentiment analysis in Python: Wordlist-based approach for sentiment analysis.

Examples
--------

    >>> from afinn import Afinn
    >>> afinn = Afinn()
    >>> afinn.score('This is utterly excellent!')
    3.0
    
In Danish:

    >>> afinn = Afinn(language='da')
    >>> afinn.score('Hvis ikke det er det mest afskyelige flueknepperi...')
    -6.0

Travis tests
------------

.. image:: https://travis-ci.org/fnielsen/afinn.svg?branch=master
    :target: https://travis-ci.org/fnielsen/afinn
