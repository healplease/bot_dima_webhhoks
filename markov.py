import os
import re
import json
import random

import markovify

def create_martinov():
    with open('user.json', 'r', encoding='utf-8') as f:
        model = markovify.Text.from_json('\n'.join(f.readlines()))

    return model

def prepare_model():
    with open('user.txt', 'r', encoding='utf-8') as f:
        model = markovify.NewlineText(f.read())
    with open('user.json', 'w+', encoding='utf-8') as f:
        f.write(model.to_json())

def analyze_chat(path:str, ids=[]):
    print(path)
    with open('user.txt', 'a+', encoding='utf-8') as out: 
        with open(path + '/result.json', 'r', encoding='utf-8') as f:
            chat = json.load(f)
            for message in chat['messages']:
                if not 'from_id' in message:
                    continue
                if message['from_id'] not in ids:
                    continue
                if 'forwarded_from' in message:
                    continue
                if message.get('text'):
                    if isinstance(message['text'], str):
                        text = message['text'].lower()
                        text = text.replace('\n', ' ')
                        out.write(text + '\n')

if __name__ == '__main__':
    analyze_chat(r'C:\Users\agava\Downloads\Telegram Desktop\ChatExport_2020-10-22', [4966219286, 5385278208])
    analyze_chat(r'C:\Users\agava\Downloads\Telegram Desktop\ChatExport_2020-10-22 (1)', [4966219286, 4813125551])
    
    prepare_model()