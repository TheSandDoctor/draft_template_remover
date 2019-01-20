#!/usr/bin/env python3.6
import mwclient,mwparserfromhell,sys,json
def getPageID(site,page):
    result = site.api('query',prop='redirects',titles=str(page),rdcontinue=None,rdlimit=0,format='json')
    encoded_hand = json.dumps(result)
    decoded = json.loads(encoded_hand)
    return int(list(decoded.get('query').get("pages").keys())[0])
def getRedirects(site,page,sleep_duration = None,extra=""):
    cont = None;
    pages = []
    i = 1
    while(1):
        result = site.api('query',prop='redirects',titles=str(page),rdcontinue=cont,rdlimit=500,rdnamespace=10,format='json')
        #print("got here")
        encoded_hand = json.dumps(result)
        decoded = json.loads(encoded_hand)
        page_id = int(list(decoded.get('query').get("pages").keys())[0])
        if sleep_duration is (not None):
            time.sleep(sleep_duration)
        #res2 = result['query']['embeddedin']
        for res in result['query']['pages'][str(page_id)]:
            print('append ' + res['title'])
            pages.append(res['title'])
            i +=1
        try:
            cont = result['continue']['rdcontinue']
            print("cont")
        except NameError:
            print("Namerror")
            return pages
        except Exception as e:
            print("Other exception" + str(e))
            #    print(pages)
            return pages
site = mwclient.Site(('https','en.wikipedia.org'), '/w/')
stub_types = []
for page in site.Categories['Stub message templates']:
    if(str(page.name)[:9] == "Template:"):
        print(getRedirects(site,str(page.name)))
        stub_types.append(str(page.name)[9:])
        stub_types.append(getRedirects(site,str(page.name)[9:]))
        print(str(page.name)[9:])
    #with open(str(page.name)[46:] + ".txt",mode='a+',encoding='utf-8') as f:
# f.write('\n*'.join(stub_types))
#stub_types = []
with open("stub_types.txt",mode='a+',encoding='utf-8') as f:
    f.write('\n'.join(stub_types))
