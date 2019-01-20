#!/data/project/deprecated-fixer-bot/www/python/venv/bin/python3
# -*- coding: utf-8 -*-
import mwclient,json, configparser
from pprint import pprint
from collections import OrderedDict
from mwclient import errors
def getRedirects(site,page,page_id,sleep_duration = None,extra=""):
    cont = None;
    pages = []
    i = 1
    while(1):
        result = site.api('query',prop='redirects',titles=str(page),rdcontinue=cont,rdlimit=500,rdnamespace=10,format='json')
        #print("got here")
        encoded_hand = json.dumps(result)
        decoded = json.loads(encoded_hand)
        #page_id = int(list(decoded.get('query').get("pages").keys())[0])
        if sleep_duration is (not None):
            time.sleep(sleep_duration)
        #res2 = result['query']['embeddedin']
        for res in decoded.get('query').get('pages').get(page_id).get('redirects'):
            print('append ' + res.get('title'))
            pages.append(res.get('title'))
            i +=1
        try:
            cont = decoded['continue']['rdcontinue']
            print("cont")
        except NameError:
            print("Namerror")
            return pages
        except Exception as e:
            print("Other exception" + str(e))
            #    print(pages)
            return pages


if __name__ == "__main__":
    results = []
    pages = {}
    site = mwclient.Site(('https','en.wikipedia.org'), '/w/')
    config = configparser.RawConfigParser()
    config.read('/data/project/thesandbot/testing/credentials.txt')
    try:
        #pass
        site.login(config.get('enwiki_sandbot','username'), config.get('enwiki_sandbot', 'password'))
    except errors.LoginError as e:
        print(e)
        raise ValueError("Login failed.")
    #res = []
    with open("/data/project/thesandbot/testing/redirects_exist_filtered.txt",mode='r',encoding='utf-8') as f:
        pages = json.load(f,object_pairs_hook=OrderedDict)
    #pages = {k:v for k,v in pages.items() if v != False}
    #with open("./redirects_exist_filtered.txt",mode='w',encoding='utf-8') as f:
    #    f.write(json.dumps(pages,sort_keys=True,indent=4))
    #pprint(res)
    for k,_ in pages.items():
        #need to split
        temp = k.split("|")
        results.append(getRedirects(site,temp[1],temp[0]))
    with open("/data/project/thesandbot/testing/redirects_final_filtered.txt",mode='wt',encoding='utf-8') as f:
        for _list in results:
            for _string in _list:
                #f.seek(0)
                f.write(str(_string) + '\n')
        # f.write('\n'.join(str(line) for line in results))
