import json
import lang_dictionaries

with open('launch_options.json', 'r') as f:
    data = json.load(f)
    if data['language'] == 'ru':
        lang_ = lang_dictionaries.ru
    elif data['language'] == 'zh':
        lang_ = lang_dictionaries.zh
    else:
        lang_ = lang_dictionaries.en
