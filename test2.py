from transformers import BertForQuestionAnswering, BertTokenizer
import torch
#/media/stas/56a32429-e1e2-4e4c-b3c2-e2a4e74942b1/site-pakage
def answer_question1(text, question):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    print(0,1)
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    print(1)
    inputs = tokenizer(question, text, return_tensors='pt')
    print(2)
    logits = model(**inputs)
    print(3)
    start_index = torch.argmax(logits['start_logits'])
    print(4)
    end_index = torch.argmax(logits['end_logits']) + 1
    print(5)

    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][start_index:end_index]))
    return answer

text = """ТЕХНИЧЕСКОЕ ЗАДАНИЕ НА ВЫПОЛНЕНИЕ ПРОЕКТНЫХ РАБОТ по созданию и внедрению системы обеспечения информационной безопасности в части соблюдения соответствия законодательству о защите персональных данных для клиента ПАО «Ростелеком» 1. Основные цели Работ Полное наименование Работ – «создание и внедрение системы обеспечения \n
информационной безопасности в части соблюдения соответствия законодательству о
защите персональных данных для клиента ПАО «Ростелеком»»
Краткое название Работ – «Создание СЗПДн».
Заказчик Работ – ПАО «Ростелеком» (далее – Компания).
"""
question = "кто заказчик работ?"

answer = answer_question1(text, question)
print(answer)

from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch

from transformers import GPT2LMHeadModel, GPT2Tokenizer

def answer_question2(context, question):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    input_text = context + " Question: " + question + " Answer:"

    input_ids = tokenizer.encode(input_text, return_tensors="pt")


    max_length = 660  # Максимальная длина ответа
    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1, no_repeat_ngram_size=2)

    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return response

# Пример текста и вопроса для тестирования
context = """ТЕХНИЧЕСКОЕ ЗАДАНИЕ НА ВЫПОЛНЕНИЕ ПРОЕКТНЫХ РАБОТ по созданию и внедрению системы обеспечения информационной безопасности в части соблюдения соответствия законодательству о защите персональных данных для клиента ПАО «Ростелеком» 1. Основные цели Работ Полное наименование Работ – «создание и внедрение системы обеспечения \n
информационной безопасности в части соблюдения соответствия законодательству о
защите персональных данных для клиента ПАО «Ростелеком»»
Краткое название Работ – «Создание СЗПДн».
Заказчик Работ – ПАО «Ростелеком» (далее – Компания).
"""
question = "кто заказчик работ?"

# answer = answer_question2(context, question)
# print(answer)

from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch

def answer_question3(context, question):
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased')

    encoding = tokenizer.encode_plus(question, context, return_tensors='pt')
    print(encoding)
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    logits = model(input_ids, attention_mask=attention_mask)
    start_index = torch.argmax(logits['start_logits'])
    end_index = torch.argmax(logits['end_logits'])

    answer_tokens = input_ids[0][start_index: end_index + 1]
    answer = tokenizer.decode(answer_tokens)

    return answer


context = """ТЕХНИЧЕСКОЕ ЗАДАНИЕ НА ВЫПОЛНЕНИЕ ПРОЕКТНЫХ РАБОТ по созданию и внедрению системы обеспечения информационной безопасности в части соблюдения соответствия законодательству о защите персональных данных для клиента ПАО «Ростелеком» 1. Основные цели Работ Полное наименование Работ – «создание и внедрение системы обеспечения \n
информационной безопасности в части соблюдения соответствия законодательству о
защите персональных данных для клиента ПАО «Ростелеком»»
Краткое название Работ – «Создание СЗПДн».
Заказчик Работ – ПАО «Ростелеком» (далее – Компания).
"""
question = "заказчик работ?"

# context = "DistilBERT is a small, fast and light Transformer model for NLP."
# question = "What is DistilBERT?"

# answer = answer_question3(context, question)
# print("Answer:", answer)
