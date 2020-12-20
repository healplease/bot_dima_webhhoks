import random
import time
import os
import string
import socket
import zipfile

from flask import Flask, request

import telebot
from telebot import types

import markovify

TOKEN = '877244637:AAE9Lb-xRSB26BM4vS8j8cxeWxpKrb3eYB4'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

with open('user.txt', 'r', encoding='utf-8') as f:
    model = markovify.NewlineText(f.read())

def generate_answer(chat_id, words):
    answer = ''
    t = 0
    while not answer and t < 5:
        bot.send_chat_action(chat_id, 'typing')
        answer = model.make_sentence_with_start(random.choice(words), strict=False)
        t += 1
    
    if not answer:
        bot.send_chat_action(chat_id, 'typing')
        answer = model.make_sentence()

    return answer

def generate_story(chat_id, words):
    sentences = random.randint(6, 12)
    story = f'<b>{words.capitalize()}:</b>\n\n'
    last_sentence = model.make_sentence().capitalize() + '. '
    for _ in range(sentences):
        #bot.send_chat_action(chat_id, 'typing')
        story += last_sentence
        words = list(map(lambda x: x.strip(string.punctuation).lower(), last_sentence.split()))
        last_sentence = model.make_sentence().capitalize() + '. '

    story = story + '\n\n<i>Вывод: ' + model.make_sentence() + '.</i>'
    return story

@bot.message_handler(content_types=['text'])
def _(message):
    try:
        try:
            print(f'({message.chat.type})[{message.message_id}] {message.chat.username}: {message.text}')
        except AttributeError:
            pass

        words = []

        if not message.text.lower().startswith('дим') and message.chat.type != 'private':
            return

        elif message.text.lower().startswith('дим') and message.chat.type != 'private':
            words = list(map(lambda x: x.strip(string.punctuation), message.text.lower().split()[1:]))

        elif message.chat.type == 'private':
            words = list(map(lambda x: x.strip(string.punctuation), message.text.lower().split()))
        
        if not words:
            answer = model.make_sentence()
        
        else:
            answer = generate_answer(message.chat.id, words)

        if 'скажи' in message.text.lower():
            words = list(map(lambda x: x.strip(string.punctuation), message.text.lower().split()))
            w = 0
            for i in range(len(words)):
                if 'скажи' in words[i]:
                    w = i
            words = words[w:]

            answer = generate_story(message.chat.id, ' '.join(words))


        print(f'answer to {message.chat.username}: {answer}')
        bot.send_message(message.chat.id, answer, parse_mode='HTML')
        return
    
    except Exception as e:
        if getattr(message.chat, 'username', None):
            if message.chat.username == 'healplease':
                bot.send_message(message.chat.id, e.with_traceback())


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '!', 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://dimasik-bot.herokuapp.com/' + TOKEN)
    return '!', 200


if __name__ == '__main__':
    app.run(host=socket.gethostbyname(socket.gethostname()))