import re

def clean_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_sentences(text):
    sentences = text.split('.')
    return [s.strip() for s in sentences if len(s.split()) > 5]
