import re

def extract_text_between_keywords(text, keyword1, keyword2):
    pattern = re.escape(keyword1) + r'(.*?)' + re.escape(keyword2)
    result = re.search(pattern, text, re.DOTALL)
    if result:
        return result.group(1).strip()
    else:
        return None

text = "Это пример текста, в котором мы хотим выделить фрагменты между ключевыми словами 'Python' и 'вырезать'."
keyword1 = "Python"
keyword2 = "вырезать"

# extracted_text = extract_text_between_keywords(text, keyword1, keyword2)
# print(extracted_text)

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


def summarize_text(text):
    nltk.download('stopwords')
    nltk.download('punkt')
    # Загружаем стоп-слова
    stop_words = set(stopwords.words("russian"))

    # Разбиваем текст на предложения
    sentences = sent_tokenize(text)
    # print(sentences)
    # Составляем список слов, учитывая их частоту встречаемости
    freq_table = dict()
    for sent in sentences:
        words = word_tokenize(sent)
        for word in words:
            if word not in stop_words:
                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1

    # Вычисляем вес каждого предложения
    sentence_weights = dict()
    for sent in sentences:
        for word, freq in freq_table.items():
            if word in sent.lower():
                if sent in sentence_weights:
                    sentence_weights[sent] += freq
                else:
                    sentence_weights[sent] = freq

    # Вычисляем средний вес предложения
    avg_weight = sum(sentence_weights.values()) / len(sentence_weights)

    # Формируем итоговую суммаризацию
    summary = ''
    for sent in sentences:
        if sent in sentence_weights and sentence_weights[sent] > (1.2 * avg_weight):
            summary += " " + sent
    return summary