#!/data/project/deprecated-fixer-bot/www/python/venv/bin/python3
# -*- coding: utf-8 -*-
import mwclient,json, configparser
from pprint import pprint
from collections import OrderedDict
num_split = 500
def getRedirects(site,page_list,sleep_duration = None,extra=""):
    cont = None;
    #pages = []
    titles = "|".join(str(value) for _,value in page_list.items()) #titles cannot contain pipes, so don't need to worry about that
    #pprint(page_list)
    page_ids = []
    [page_ids.append(key) for key,_ in page_list.items()] #titles cannot contain pipes, so don't need to worry about that
    #while(1):
    result = site.api('query',prop='redirects',titles=str(titles),rdcontinue=cont,rdlimit=5000,rdnamespace=10,format='json')
    #print("got here")
    encoded_hand = json.dumps(result)
    decoded = json.loads(encoded_hand)
    #pprint(decoded)
    #page_id = int(list(decoded.get('query').get("pages").keys())[0])
    if sleep_duration is (not None):
        time.sleep(sleep_duration)
        #res2 = result['query']['embeddedin']
    dict = {}
    #pprint(titles)
    for id in page_ids:
        if(decoded.get("query").get("pages").get(id).get("redirects") == None):
            dict[str(id) + "|" + decoded.get("query").get("pages").get(id).get("title")] = False
        else:
            dict[str(id) + "|" + decoded.get("query").get("pages").get(id).get("title")] = True
    return dict


if __name__ == "__main__":
    pages = {}
    site = mwclient.Site(('https','en.wikipedia.org'), '/w/')
    config = configparser.RawConfigParser()
    config.read('credentials.txt')
    try:
        #pass
        site.login(config.get('enwiki_sandbot','username'), config.get('enwiki_sandbot', 'password'))
    except errors.LoginError as e:
        print(e)
        raise ValueError("Login failed.")
    with open("./formatted_page_ids.txt",mode='r',encoding='utf-8') as f:
        pages = json.load(f,object_pairs_hook=OrderedDict)
    counter = 0
    temp_list = {}
    res = {}
    abs_count = 0
    num_items = len(pages.items())
    print(num_items)
    #count = 0
    #exit()
    for id,name in pages.items(): #id: key, name: value
        #if (num_items - abs_count) <= 58:
        #    temp_list[id] = "Template:" + name
            #counter += 1
        #    abs_count += 1
        #    res.update(getRedirects(site,temp_list))
        #    temp_list.clear()
        #    print("LESS " + str(num_items - abs_count))
        #    continue
        # edge case
        temp_list[id] = "Template:" + name
        res.update(getRedirects(site,temp_list))
        temp_list.clear()
        continue
        if (num_items - abs_count) < 500 and (num_items - abs_count) > 0 and num_split != 1:# and counter < 500 and (num_items - abs_count) > 0 and num_items != abs_count:
            num_split = 1
            temp_list[id] = "Template:" + name
            #counter += 1
            abs_count += 1
            res.update(getRedirects(site,temp_list))
            temp_list.clear()
            print("Last time " + "NUM ITM " + str(num_items) + " " + str(abs_count) + " REM " + str(num_items - abs_count))
        #elif num_items == abs_count - 1: #or num_items < abs_count: # edge case
        #    print("EQL")
        #    res.update(getRedirects(site,temp_list))
        #    temp_list.clear()
        #    break

        elif counter < num_split:  # normal
            #print("F")
            temp_list[id] = "Template:" + name
            counter += 1
            abs_count += 1
        #elif counter > 50:
        #    break
        else:   # make request
            print("NORM")
            print(abs_count)
            counter = 0
        #    if(count > 2):
        #        counter = 51
        #        continue
        #    count += 1
            res.update(getRedirects(site,temp_list))
            temp_list.clear()
        print("D")
        #    break
            #getRedirects(site,"".join(str(value) for _,value in temp_list.items()))
    print("Done")
    with open("./redirects_exist.txt",mode='w',encoding='utf-8') as f:
        f.write(json.dumps(res,sort_keys=True,indent=4))
    #pprint(res)
