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
    
With emoticons:

    >>> afinn = Afinn(emoticons=True)
    >>> afinn.score('I saw that yesterday :)')
    2.0

Citation
--------
If you as a scientist use the wordlist or the code please cite this one: 

* Finn Årup Nielsen, "A new ANEW: evaluation of a word list for sentiment analysis in microblogs" , Proceedings of the ESWC2011 Workshop on 'Making Sense of Microposts': Big things come in small packages 718 in CEUR Workshop Proceedings: 93-98. 2011 May. Matthew Rowe, Milan Stankovic, Aba-Sah Dadzie, Mariann Hardey (editors)

Paper with supplement: http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6006/pdf/imm6006.pdf

Travis tests
------------

.. image:: https://travis-ci.org/fnielsen/afinn.svg?branch=master
    :target: https://travis-ci.org/fnielsen/afinn
