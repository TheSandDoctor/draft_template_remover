#!/usr/bin/env python3.6
import mwclient,mwparserfromhell,sys,json
site = mwclient.Site(('https','en.wikipedia.org'), '/w/')
stub_types = []
redirects_exist = []
for page in site.Categories['Stub message templates']:
    if(str(page.name)[:9] == "Template:"):
        stub_types.append(str(page.name))
with open("stub_types.txt",mode='w',encoding='utf-8') as f:
    f.write('\n'.join(stub_types))
