"""Base for AFINN sentiment analysis."""


from __future__ import absolute_import, division, print_function

import codecs

import re

from os.path import dirname, join


LANGUAGE_TO_FILENAME = {
    'da': 'AFINN-da-32.txt',
    'en': 'AFINN-111.txt',
    'emoticons': 'AFINN-emoticon-8.txt',
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

    >>> afinn = Afinn(emoticons=True)
    >>> afinn.score('My reaction: :-)') > 0
    True

    >>> afinn = Afinn(language='da', emoticons=True)
    >>> afinn.score('Det er bare :-)))') > 0
    True

    """

    def __init__(self, language="en", emoticons=False, word_boundary=True):
        """Setup dictionary from data file.

        The language parameter can be set to English (en) or Danish (da).

        Parameters
        ----------
        language : 'en' or 'da', optional
            Specify language dictionary.
        emoticons : bool, optional
            Includes emoticons in the token list
        word_boundary : bool, optional
            Use word boundary match in the regular expression.

        """
        filename = LANGUAGE_TO_FILENAME[language]
        full_filename = self.full_filename(filename)
        if emoticons:
            # Words
            self._dict = self.read_word_file(full_filename)
            regex_words = self.regex_from_tokens(
                list(self._dict),
                word_boundary=True, capture=False)

            # Emoticons
            filename_emoticons = LANGUAGE_TO_FILENAME['emoticons']
            full_filename_emoticons = self.full_filename(filename_emoticons)
            emoticons_and_score = self.read_word_file(full_filename_emoticons)
            self._dict.update(emoticons_and_score)
            regex_emoticons = self.regex_from_tokens(
                list(emoticons_and_score), word_boundary=False,
                capture=False)

            # Combined words and emoticon regular expression
            regex = '(' + regex_words + '|' + regex_emoticons + ')'
            self._setup_pattern_from_regex(regex)

        else:
            self.setup_from_file(full_filename, word_boundary=word_boundary)

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

    def setup_from_file(self, filename, word_boundary=True):
        """Setup data from data file.

        Read the word file and setup the regular expression pattern for
        matching.

        Parameters
        ----------
        filename : str
            Full filename.

        """
        self._dict = self.read_word_file(filename)
        self._setup_pattern_from_dict(word_boundary=word_boundary)

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

    @staticmethod
    def regex_from_tokens(tokens, word_boundary=True, capture=True):
        r"""Return regular expression string from list of tokens.

        Parameters
        ----------
        tokens : List of str
            List of tokens/words to form a regex
        word_boundary : bool, optional
            Add word boundary match to the regular expression
        capture : bool, optional
            Add capture characters

        Returns
        -------
        regex : str
            String with regular expression

        Examples
        --------
        >>> afinn = Afinn()
        >>> afinn.regex_from_tokens(['good', 'bad'])
        '(\\b(?:good|bad)\\b)'

        >>> afinn.regex_from_tokens(['good', 'bad'], word_boundary=False,
        ...     capture=False)
        '(?:good|bad)'

        """
        tokens_ = tokens[:]

        # The longest tokens are first in the list
        tokens_.sort(key=lambda word: len(word), reverse=True)

        # Some tokens might contain parentheses or other problematic characters
        tokens_ = [re.escape(word) for word in tokens_]

        # Build regular expression
        regex = '(?:' + "|".join(tokens_) + ')'
        if word_boundary:
            regex = r"\b" + regex + r"\b"
        if capture:
            regex = '(' + regex + ')'

        return regex

    def _setup_pattern_from_regex(self, regex):
        """Set internal variable from regex string."""
        self._pattern = re.compile(regex, flags=re.UNICODE)

    def _setup_pattern_from_dict(self, word_boundary=True):
        """Pattern for identification of words from data files.

        Setup of regular expression pattern for matching phrases from the data
        files.

        Parameters
        ----------
        word_boundary : bool, optional
            Add word boundary match to the regular expression

        """
        regex = self.regex_from_tokens(
            list(self._dict),
            word_boundary=word_boundary)
        self._setup_pattern_from_regex(regex)

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

        >>> afinn = Afinn(emoticons=True)
        >>> afinn.find_all('It is wonderful :)')
        ['wonderful', ':)']

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

        The output is a float variable that if larger than zero indicates a
        positive sentiment and less than zero indicates negative sentiment.

        Parameters
        ----------
        text : str
            Text to be analyzed for sentiment.

        Returns
        -------
        score : float
            Sentiment analysis score for text

        """
        # TODO: ":D" is not matched
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
