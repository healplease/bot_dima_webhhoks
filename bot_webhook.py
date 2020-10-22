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

with zipfile.ZipFile('user.zip') as archive:
    with archive.open('user.json', 'r') as f:
        model = markovify.Text.from_json(f.read().decode("utf-8"))

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


@bot.message_handler(content_types=['text'])
def _(message):
    try:
        print(f'({message.chat.type})[{message.message_id}] {message.chat.username}: {message.text}')
    except AttributeError:
        pass

    if not message.text.lower().startswith('дим') and message.chat.type != 'private':
        return

    elif message.text.lower().startswith('дим') and message.chat.type != 'private':
        words = list(map(lambda x: x.strip(string.punctuation), message.text.lower().split()[1:]))

    elif message.chat.type == 'private':
        words = list(map(lambda x: x.strip(string.punctuation), message.text.lower().split()))
    
    if not words:
        answer = model.make_sentence()
    
    answer = generate_answer(message.chat.id, words)
    print(f'answer to {message.chat.username}: {answer}')
    bot.send_message(message.chat.id, answer)
    return


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://dimasik-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host=socket.gethostbyname(socket.gethostname()))