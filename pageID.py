#!/usr/bin/env python3.6
import mwclient,json
def getPageID(site,page):
    result = site.api('query',prop='redirects',titles=str(page),rdcontinue=None,rdlimit=0,format='json')
    encoded_hand = json.dumps(result)
    decoded = json.loads(encoded_hand)
    return int(list(decoded.get('query').get("pages").keys())[0])

site = mwclient.Site(('https','en.wikipedia.org'), '/w/')
#page = site.Pages["Template:Orphan"]
print(getPageID(site,"Template:Orphan"))
