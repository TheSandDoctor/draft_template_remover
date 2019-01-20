#!/data/project/deprecated-fixer-bot/www/python/venv/bin/python3
# -*- coding: utf-8 -*-
import mwclient,json, configparser
from pprint import pprint
from collections import OrderedDict

if __name__ == "__main__":
    pages = {}
    with open("./redirects_exist2.txt",mode='r',encoding='utf-8') as f:
        pages = json.load(f,object_pairs_hook=OrderedDict)
    pages = {k:v for k,v in pages.items() if v != False}
    with open("./redirects_exist_filtered.txt",mode='w',encoding='utf-8') as f:
        f.write(json.dumps(pages,sort_keys=True,indent=4))
    #pprint(res)
