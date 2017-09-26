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

In Swedish:

	>>> afinn = Afinn(language='sv')
	>>> afinn.score('det är inte bra')
	-2.0

With emoticons:

    >>> afinn = Afinn(emoticons=True)
    >>> afinn.score('I saw that yesterday :)')
    2.0

With multiple sentences (here with data from an Austen novel available in Gutenberg):

    >>> from afinn import Afinn
    >>> from nltk.corpus import gutenberg
    >>> import textwrap
    >>> afinn = Afinn()
    >>> sentences = (" ".join(wordlist) for wordlist in gutenberg.sents('austen-sense.txt'))
    >>> scored_sentences = ((afinn.score(sent), sent) for sent in sentences)
    >>> sorted_sentences = sorted(scored_sentences)
    >>> print("\n".join(textwrap.wrap(sorted_sentences[0][1], 70)))
    To attach myself to your sister , therefore , was not a thing to be
    thought of ;-- and with a meanness , selfishness , cruelty -- which no
    indignant , no contemptuous look , even of yours , Miss Dashwood , can
    ever reprobate too much -- I was acting in this manner , trying to
    engage her regard , without a thought of returning it .-- But one
    thing may be said for me : even in that horrid state of selfish vanity
    , I did not know the extent of the injury I meditated , because I did
    not THEN know what it was to love .

Citation
--------
If you as a scientist use the wordlist or the code please cite this one:

* Finn Årup Nielsen, "A new ANEW: evaluation of a word list for sentiment analysis in microblogs", Proceedings of the ESWC2011 Workshop on 'Making Sense of Microposts': Big things come in small packages. Volume 718 in CEUR Workshop Proceedings: 93-98. 2011 May. Matthew Rowe, Milan Stankovic, Aba-Sah Dadzie, Mariann Hardey (editors)

Paper with supplement: http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6006/pdf/imm6006.pdf

See also
--------
* http://neuro.compute.dtu.dk/wiki/AFINN - Brede Wiki entry on AFINN with pointers to many scientific papers
* https://github.com/darenr/afinn - Sentiment analysis in Javascript with AFINN word list


Travis et al.
-------------

.. image:: https://travis-ci.org/fnielsen/afinn.svg?branch=master
    :target: https://travis-ci.org/fnielsen/afinn

.. image:: https://coveralls.io/repos/fnielsen/afinn/badge.svg?branch=master :target: https://coveralls.io/github/fnielsen/afinn?branch=master

.. image:: https://www.quantifiedcode.com/api/v1/project/0bcc1cd5b8f54a0fbd2f2e6f226cfa4f/badge.svg
  :target: https://www.quantifiedcode.com/app/project/0bcc1cd5b8f54a0fbd2f2e6f226cfa4f
  :alt: Code issues

.. image:: https://img.shields.io/pypi/dm/afinn.svg?style=flat
   :target: https://pypi.python.org/pypi/afinn
   :alt: Downloads

.. image:: https://www.openhub.net/p/afinn/widgets/project_thin_badge.gif
   :target: https://www.openhub.net/p/afinn
   :alt: Open Hub
