import spacy
from spacy.lang.ru.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from src.processings.document_processing import document2text


def summarize(text, sentence_number=5):
    nlp = spacy.load('ru_core_news_sm')
    doc = nlp(text)
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
    summary = nlargest(sentence_number, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)
    return summary


def summarize_file(filename, sentence_number=5):
    text = document2text(filename)
    text = text.replace('HYPERLINK', '')
    text = text.replace('_', '')
    text = ' '.join(text.split())
    text = summarize(text, sentence_number)
    return text
