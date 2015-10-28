"""For packaging and installation."""

from setuptools import setup


setup(
    name='afinn',
    packages=['afinn'],
    version='0.0.1pre1',
    author='Finn Aarup Nielsen',
    author_email='faan@dtu.dk',
    description='AFINN sentiment analysis',
    license='GPL',
    keywords='sentiment analysis',
    url='https://github.com/fnielsen/afinn',
    package_data={'afinn': ['data/*.txt', 'data/LICENSE']},
    long_description='',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        ],
    )
