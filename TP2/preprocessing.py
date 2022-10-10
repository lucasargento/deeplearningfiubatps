import re
import unicodedata
import pandas as pd
import dask.dataframe as dd
from textacy import preprocessing
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ' '.join(self.fed)

    
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def remove_punctuation(text):
    punc = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{{|}}~"
    for ch in punc:
        text = text.replace(ch, " ")
    return text


def strip_accents(text):
    if not isinstance(text, str):
        text = str(text, "utf-8")
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
    return str(text)


def preprocess_text(text):
    
    if text:
        tmp = text
        
        tmp = strip_tags(text)
        
        tmp = str(tmp)

        #tmp = preprocessing.normalize_whitespace(tmp)
        tmp = preprocessing.normalize.whitespace(tmp)
        tmp = preprocessing.replace.emails(tmp)
        tmp = preprocessing.replace.phone_numbers(tmp)
        tmp = preprocessing.replace.urls(tmp)
        tmp = tmp.lower()
        tmp = remove_punctuation(tmp)
        tmp = strip_accents(tmp)

        tmp = tmp.strip()    
        tmp = ' '.join(tmp.splitlines())
        
        return tmp
    
    else:
        return ''
 
    
def dask_proc(s, col_text):
    return s.apply(lambda row: preprocess_text(row[col_text]), axis=1)