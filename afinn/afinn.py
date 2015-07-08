"""Base for AFINN sentiment analysis."""


from __future__ import absolute_import, division, print_function

import codecs

import re

from os.path import dirname, join


LANGUAGE_TO_FILENAME = {
    'da': 'AFINN-da-28.txt',
    'en': 'AFINN-111.txt'
    }


class Afinn(object):

    """Sentiment analyzer.

    The text input should be in Unicode.

    Examples
    --------
    >>> afinn = Afinn()
    >>> afinn.score('This is oh so bad.') < 0
    True

    >>> afinn = Afinn(language='da')
    >>> afinn.score('Det er bare vidunderlig!!!') > 0
    True

    """

    def __init__(self, language="en"):
        """Setup dictionary from data file.

        The language parameter can be set to English (en) or Danish (da).

        Parameters
        ----------
        language : 'en' or 'da', optional
            Specify language dictionary

        """
        filename = LANGUAGE_TO_FILENAME[language]
        full_filename = self.full_filename(filename)
        self.setup_from_file(full_filename)

        self._word_pattern = re.compile('\w+', flags=re.UNICODE)

    def data_dir(self):
        """Return directory where the text files are.

        The sentiment wordlists are distributed in a subdirectory.
        This function returns the path to that subdirectory.

        Returns
        -------
        path : str
             Pathname to data files.

        Examples
        --------
        >>> afinn = Afinn()
        >>> path = afinn.data_dir()
        >>> from os.path import split
        >>> split(path)[-1]
        'data'

        """
        return join(dirname(__file__), 'data')

    def full_filename(self, filename):
        """Return filename with full with data directory.

        Prepending the path of the data directory to the filename.

        Parameters
        ----------
        filename : str
            Filename without path for data file.

        Returns
        -------
        full_filename : str
            Filename with path

        Examples
        --------
        >>> afinn = Afinn()
        >>> filename = afinn.full_filename('AFINN-111.txt')
        >>> from os.path import split
        >>> split(filename)[-1]
        'AFINN-111.txt'

        """
        return join(self.data_dir(), filename)

    def setup_from_file(self, filename):
        """Setup data from data file.

        Read the word file and setup the regular expression pattern for
        matching.

        Parameters
        ----------
        filename : str
            Full filename.

        """
        self._dict = self.read_word_file(filename)
        self._setup_pattern()

    @staticmethod
    def read_word_file(filename):
        """Read data from tab-separated file.

        Parameters
        ----------
        filename : str
            Full filename for tab-separated data file.

        Returns
        -------
        word_dict : dict
            Dictionary with words from file

        """
        word_dict = {}
        with codecs.open(filename, encoding='UTF-8') as fid:
            for line in fid:
                word, score = line.strip().split('\t')
                word_dict[word] = int(score)
        return word_dict

    def _setup_pattern(self):
        """Pattern for identification of words from data files."""
        words = list(self._dict)

        # The longest words are first in the list
        words.sort(key=lambda word: len(word), reverse=True)

        # Some words might contain parentheses
        words = [re.escape(word) for word in words]

        # Setup compiled pattern
        self._pattern = re.compile(r"\b(" + "|".join(words) + r")\b",
                                   flags=re.UNICODE)

    def find_all(self, text, clean_whitespace=True):
        """Find all tokens in a text matching the dictionary.

        Words that do not match the dictionary is not returned in the wordlist.

        The text is automatically lower-cased.

        A simple regular expression match is used.

        Parameters
        ----------
        text : str
            String with text where words are to be found.
        clean_whitespace : bool, optional
            Change multiple whitespaces to a single.

        Returns
        -------
        words : list of str
            List of words

        Examples
        --------
        >>> afinn = Afinn()
        >>> afinn.find_all('It is wonderful!')
        ['wonderful']

        """
        if clean_whitespace:
            text = re.sub(r"\s+", " ", text)
        words = self._pattern.findall(text.lower())
        return words

    def split(self, text):
        """Split a string into words.

        Parameters
        ----------
        text : str
            String with text that should be split

        Returns
        -------
        wordlist : list of str
            List of words

        Examples
        --------
        >>> afinn = Afinn()
        >>> afinn.split('Hello, world!')
        ['Hello', 'world']

        """
        wordlist = self._word_pattern.findall(text)
        return wordlist

    def score_with_pattern(self, text):
        """Score text based on pattern matching.

        Performs the actual sentiment analysis on a text. It uses a regular
        expression match against the word list.

        Parameters
        ----------
        text : str
            Text to be analyzed for sentiment.

        Returns
        -------
        score : float
            Sentiment analysis score for text

        """
        words = self.find_all(text)
        word_scores = (self._dict[word] for word in words)
        score = float(sum(word_scores))
        return score

    def score_with_wordlist(self, text):
        """Score text based on initial word split.

        Performs the actual sentiment analysis on a text.

        Parameters
        ----------
        text : str
            Text to be analyzed for sentiment.

        Returns
        -------
        score : float
            Sentiment analysis score for text

        """
        words = self.split(text)
        word_scores = (self._dict.get(word.lower(), 0.0) for word in words)
        score = float(sum(word_scores))
        return score

    score = score_with_pattern
