#!/usr/bin/env python3.6
import mwclient,mwparserfromhell,sys,json
def getPageID(site,page):
    result = site.api('query',prop='redirects',titles="Template:" + str(page),rdcontinue=None,rdlimit=0,format='json')
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
        if(decoded.get("query").get("pages").get(str(page_id)).get("redirects") == None):
            return None
        else:
            return True
        for res in decoded.get("query").get("pages").get(str(page_id)).get("redirects"):
            #print('append ' + res.get('title')[9:])
            pages.append(res.get('title')[9:])
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
if __name__ == "__main__":
    site = mwclient.Site(('https','en.wikipedia.org'), '/w/')
    stub_types = []
    redirects_exist = []
    count = 0
    lines = []
    base_names = {}
    with open("stub_types.txt",mode='r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        base_names[getPageID(site,line)] = line
        print("Working with " + line)
        count += 1
        #if count == 50:
        #    break
    with open("t.txt",mode='w') as f:
        f.write(json.dumps(base_names))
    from sys import exit
    exit(0)


    for page in site.Categories['Stub message templates']:
        if(str(page.name)[:9] == "Template:"):
            stub_types.append(str(page.name)[9:])
            redirects = getRedirects(site,str(page.name))
            if redirects != None:
                redirects_exist.append(str(page.name))
                #for i in redirects:
                #    stub_types.append(str(i))
            print(str(page.name)[9:])
        #with open(str(page.name)[46:] + ".txt",mode='a+',encoding='utf-8') as f:
    # f.write('\n*'.join(stub_types))
    #stub_types = []
    with open("stub_types.txt",mode='a+',encoding='utf-8') as f:
        f.write('\n'.join(stub_types))
    with open("stub_types_redirects_exist.txt",mode='a+',encoding='utf-8') as f:
        f.write('\n'.join(redirects_exist))
