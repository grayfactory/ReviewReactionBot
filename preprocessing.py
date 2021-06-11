import pandas as pd
import pickle
from pathlib import Path, PurePath
import re
import numpy as np

from soynlp.normalizer import emoticon_normalize, repeat_normalize, remove_doublespace

def emoji_regex(text):
    # 이모티콘 제거
    emoji_pattern = re.compile("[" 
        u"\U0001F600-\U0001F64F" # emoticons 
        u"\U0001F300-\U0001F5FF" # symbols & pictographs 
        u"\U0001F680-\U0001F6FF" # transport & map symbols 
        u"\U0001F1E0-\U0001F1FF" # flags (iOS) 
        u"\U00010000-\U0010FFFF"
            "]+", flags=re.UNICODE)

    text = emoji_pattern.sub(r'',text)

    return text

def clean_punc(text):

    # 특수문자, 등 제거
    punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&' 
    punct_mapping = {"‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", 
                    "√": " sqrt ", "×": "x", "²": "2", "—": "-", "–": "-", "’": "'", 
                    "_": "-", "`": "'", '“': '"', '”': '"', '“': '"', "£": "e", '∞': 'infinity', 
                    'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 
                    'β': 'beta', '∅': '', '³': '3', 'π': 'pi', }
  
    text = re.sub(r'[A-Za-z\\**]+[님]', '', text) # user id 언급 삭제
    for p in punct_mapping: 
        text = text.replace(p, punct_mapping[p]) 

    # special case & extra emoji
    specials = {'\u200b': ' ', '…': ' ... ', '\ufeff': '', 'करना': '', 'है': '', 
                '❣':'', '❤':'','๑˃̵ᴗ˂̵':'','☆':'', '♥':'','⭐':'','❤️':''} 
    for s in specials: 
        text = text.replace(s, specials[s]) 
    
    return text.strip()

def clean_text(texts): 
  # corpus = [] 
  # for i in range(0, len(texts)): 
  # review = re.sub(r'[@%\\*=()/~#&\+á?\xc3\xa1\-\|\.\:\;\!\-\,\_\~\$\'\"]', '',texts) #remove punctuation
  review = re.sub(r'[@%\\*=()/#&\+á?\xc3\xa1\-\|\:\-\_\$\'\"\^]', '',texts) 
  # review = re.sub(r'\d+','', texts)# remove number 
  review = review.lower() #lower case
  review = re.sub(r'\s+', ' ', review) #remove extra space 
  review = re.sub(r'<[^>]+>','',review) #remove Html tags 
  review = re.sub(r'\s+', ' ', review) #remove spaces 
  review = re.sub(r"^\s+", '', review) #remove space from start 
  review = re.sub(r'\s+$', '', review) #remove space from the end 
    
  return review


def pre_processing_text(text):
    if text is None:
        return None
    text = emoji_regex(text)
    text = clean_text(text)
    text = emoticon_normalize(text, num_repeats=2)
    text = clean_punc(text)

    return text
