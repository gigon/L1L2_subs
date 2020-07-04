# Borrowed and modified from https://github.com/elaisasearch/categorizer

import json
import os
import sys

from textblob import TextBlob
from textacy import preprocessing
import textacy as textacy

# this is required just so pyinstaller includes this module used by spacy:
import en_core_web_sm

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(os.path.dirname(__file__))+"\\..\\"))
    return os.path.join(base_path, relative_path)

# These lines are just for issue with pyinstaller
# https://stackoverflow.com/questions/37144170/how-to-use-pyinstaller-to-completely-pack-all-the-necessary-library
# I had to copy nltk_data from %appdata%/roaming/nltk_data to ../resources/nltk_data
# and add these lines: 
data_path = resource_path("resources\\nltk_data")
import nltk
nltk.data.path.append(data_path)
#-------------

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]
# we can explicitly make assignments on this
this.cefr_data = None
this.spacy_en = None

def loadSpacyLangEn():
    spacy_en = textacy.load_spacy_lang("en_core_web_sm", disable=("parser",))
    return spacy_en

def loadCefrList():
    # open CEFR vocabulary file for english
    cefr_json_file_path = resource_path('resources\\cefr\\cefr_vocab_en.json')
    cefr_file = open(cefr_json_file_path)
    cefr_json = json.load(cefr_file)
    cefr_file.close()
    return cefr_json

# Adapted from https://pypi.org/project/py-readability-metrics
# That library requires a >= 100 words text and I want to ignore that
def calcFleshKincadeGrade(avg_words_per_sentence, avg_syllables_per_word):
    return round((0.38 * avg_words_per_sentence + 11.8 * avg_syllables_per_word) - 15.59)

def analyzeSubLevel(input_text: str):
    """
    :Returns: highest CEFR of word in input_text, flesh_kincade_level, number of words
    """

    if (not(isinstance(input_text, str)) or (len(input_text) <= 0)):
        return ""

    if (this.cefr_data is None):
        this.cefr_data = loadCefrList()

    # TBD make static
    if (this.spacy_en is None):
        this.spacy_en = loadSpacyLangEn()

    # normalize text with NLP
    input_text = processText(input_text)

    doc = textacy.make_spacy_doc(input_text, lang=this.spacy_en)
    ts = textacy.TextStats(doc)
    
    flesh_kincade_level = calcFleshKincadeGrade(ts.n_words, ts.n_syllables / ts.n_words)

    # store words of text lowercase in list
    words: list = [item.lower() for item in input_text.split()]
    max_level = getMaxWordLevelForWordsSet(set(words), this.cefr_data)

    return max_level, flesh_kincade_level, ts.n_words

def getMaxWordLevelForWordsSet(words, cefr_data):
    """
    Input: words set, CEFR data (json)
    Output: The highest CEFR level (A1 - C2, unknown) of any word in the set
    """
    maxLevel = ""    
    for w in words:
        # find the CEFR level info for the current word
        for data in cefr_data:
            if data["word"] == w:
                if data["level"]:
                    if data["level"] != "unknown" and data["level"] > maxLevel:
                        maxLevel = data["level"]        
    return maxLevel

def processText(text):

    preprocessedText = preprocessing.normalize.normalize_unicode(text)
    preprocessedText = preprocessing.normalize.normalize_quotation_marks(preprocessedText)
    
    preprocessedText = preprocessing.remove.remove_accents(preprocessedText)
    preprocessedText = preprocessing.remove.remove_punctuation(preprocessedText)

    preprocessedText = preprocessing.replace.replace_emails(preprocessedText, "")
    preprocessedText = preprocessing.replace.replace_phone_numbers(preprocessedText, "")
    #preprocessedText = preprocessing.replace.replace_contractions(preprocessedText)

    # lemmatize the entire text
    # first, split the text to a list of words
    words = TextBlob(preprocessedText).words
    # then, lemmatize each word
    lemmatizedText = ""
    for w in words:
        lemmatizedText += "{} ".format(w.lemmatize())

    # normalize the whitespaces for texts which include s.l. 'Title    And I am ...'
    return preprocessing.normalize_whitespace(lemmatizedText)
