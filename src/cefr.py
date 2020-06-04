# Borrowed and modified from https://github.com/elaisasearch/categorizer

import json
import os
import sys

from textblob import TextBlob
from textacy import preprocessing

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]
# we can explicitly make assignments on this
this.cefr_data = None

def loadCefrList():
    # open CEFR vocabulary file for english
    scriptDir = os.path.dirname(__file__) 
    relPath = "../resources/cefr/cefr_vocab_en.json"
    cefr_file = open(os.path.join(scriptDir, relPath))
    cefr_json = json.load(cefr_file)
    cefr_file.close()
    return cefr_json

def getCefrLevel(input_text: str):
    """
    :Returns: highest CEFR of word in input_text
    """

    if (not(isinstance(input_text, str)) or (len(input_text) <= 0)):
        return ""

    if (this.cefr_data is None):
        this.cefr_data = loadCefrList()

    # normalize text with NLP
    input_text = processText(input_text)
    
    # store words of text lowercase in list
    words: list = [item.lower() for item in input_text.split()]
    max_level = getMaxWordLevelForWordsSet(set(words), this.cefr_data)
    return max_level

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
