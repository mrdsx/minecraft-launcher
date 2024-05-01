import json
import lang_dictionaries

with open('launch_options.json') as f:
    data = json.load(f)
    if data['language'] == 'en':
        lang_ = lang_dictionaries.en
    elif data['language'] == 'ru':
        lang_ = lang_dictionaries.ru
    elif data['language'] == 'zh':
        lang_ = lang_dictionaries.zh
    else:
        lang_ = lang_dictionaries.en
