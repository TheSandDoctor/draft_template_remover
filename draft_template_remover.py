#!/usr/bin/env python3.6
import mwclient, configparser, mwparserfromhell, argparse,re, pathlib, json
from time import sleep
from mwclient import errors

def getTransclusions(site,page,sleep_duration = None,extra=""):
    cont = None;
    pages = []
    i = 1
    while(1):
        result = site.api('query',list='embeddedin',eititle=str(page),eicontinue=cont,eilimit=500,format='json')
        #print("got here")
        if sleep_duration is (not None):
            time.sleep(sleep_duration)
        #res2 = result['query']['embeddedin']
        for res in result['query']['embeddedin']:
            if res['title'][0:6] == "Draft:":
                print('append ' + res['title'])
                pages.append(res['title'])
                i +=1
        try:
            cont = result['continue']['eicontinue']
            print("cont")
        except NameError:
            print("Namerror")
            return pages
        except Exception as e:
            print("Other exception" + str(e))
            #    print(pages)
            return pages
def getPageID(site,page):
    result = site.api('query',prop='redirects',titles=str(page),rdcontinue=cont,rdlimit=1,format='json')
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

def call_home(site):
    h_page = site.Pages['User:TheSandBot/status']
    text = h_page.text()
    return bool(json.loads(text)["run"]["draft_na_template_remover"])

def save_edit(page, utils, text):
    config,site,dry_run = utils
    original_text = text

    code = mwparserfromhell.parse(text)

    if not call_home(site):#config):
        raise ValueError("Kill switch on-wiki is false. Terminating program.")
    time = 0
    edit_summary = """Removed [[Template:Orphan]], [[Template:Uncategorized]], [[Template:Unreferenced]], and/or [[Template:Underlinked]] (N/A in the draft namespace) using [[User:""" + config.get('enwiki_sandbot','username') + "| " + config.get('enwiki_sandbot','username') + """]]. Questions? [[User talk:TheSandDoctor|msg TSD!]] Please mention that this is task #2! ([[WP:Bots/Requests for approval/TheSandBot 2|BRFA]])"""
    while True:
        if time == 1:
            """
            There was an edit error (probably an edit conflict),
            so best to refetch the page and rerun.
            """
            text = site.Pages[page.page_title].text()
        try:
            content_changed, text = process_page(original_text,dry_run)
        except ValueError as e:
            """
            To get here, there must have been an issue figuring out the
            contents for the parameter colwidth.

            At this point, it is safest just to print to console,
            record the error page contents to a file in ./errors and append
            to a list of page titles that has had
            errors (error_list.txt)/create a wikified version of error_list.txt
            and return out of this method.
            """
            print(e)
            pathlib.Path('./errors').mkdir(parents=False, exist_ok=True)
            title = get_valid_filename(page.page_title)
            text_file = open("./errors/err " + title + ".txt", "w")
            text_file.write("Error present: " +  str(e) + "\n\n\n\n\n" + text)
            text_file.close()
            text_file = open("./errors/error_list.txt", "a+")
            text_file.write(page.page_title + "\n")
            text_file.close()
            text_file = open("./errors/wikified_error_list.txt", "a+")
            text_file.write("#[[" + page.page_title + "]]" + "\n")
            text_file.close()
            return
        try:
                page.save(text, summary=edit_summary, bot=True, minor=True)
                print("Saved page")
                f = open("changes.txt",'a+')
                f.write(page.name + "\n")
                f.close()
        except errors.EditError:
            print("Error")
            time = 1
            sleep(5)   # sleep for 5 seconds before trying again
            continue
        except errors.ProtectedPageError:
            print('Could not edit ' + page.page_title + ' due to protection')
        break
def get_valid_filename(s):
    """
    Turns a regular string into a valid (sanatized) string that is safe for use
    as a file name.
    Method courtesy of cowlinator on StackOverflow
    (https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename)
    @param s String to convert to be file safe
    @return File safe string
    """
    assert(s is not "" or s is not None)
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def figure_type(template):
    """
    Figure out the type (name) of the template in question. This was originally
    in process_page(), but it became unwieldy.
    Returns false if the template is none of the ones we are looking for.
    """
    if template.name.matches("orphan") or template.name.matches("Do-attempt") or template.name.matches("Lonely") or template.name.matches("Orp") or template.name.matches("Orphaned articles"):
        return "orphan"
    elif template.name.matches("uncategorized") or template.name.matches("+cat") or template.name.matches("cat needed") or template.name.matches("categories needed") or template.name.matches("categories requested") or template.name.matches("categorise") or template.name.matches("categorize") or template.name.matches("category needed") or template.name.matches("category requested") or template.name.matches("categoryneeded") or template.name.matches("categorizeame") or template.name.matches("catneeded") or template.name.matches("ncat") or template.name.matches("needs cat") or template.name.matches("needs categories") or template.name.matches("needs cats") or template.name.matches("no categories") or template.name.matches("no category") or template.name.matches("no cats") or template.name.matches("noc") or template.name.matches("nocat") or template.name.matches("nocategory") or template.name.matches("nocats") or template.name.matches("uncat") or template.name.matches("uncategorised"):
        return "uncategorized"
    elif template.name.matches("underlinked") or template.name.matches("+L") or template.name.matches("add links") or template.name.matches("few links") or template.name.matches("internal links") or template.name.matches("internal links needed") or template.name.matches("internallinks") or template.name.matches("link up") or template.name.matches("linkage") or template.name.matches("linkme") or template.name.matches("linkup") or template.name.matches("more links") or template.name.matches("not enough links") or template.name.matches("too few links") or template.name.matches("under-linked") or template.name.matches("underlink") or template.name.matches("Underlinked section") or template.name.matches("unlinked") or template.name.matches("wikilinks"):
        return "underlinked"
    elif template.name.matches("unreferenced") or template.name.matches("citesources") or template.name.matches("needs references") or template.name.matches("no ref") or template.name.matches("no reference") or template.name.matches("no references") or template.name.matches("no refs") or template.name.matches("no sources") or template.name.matches("noref") or template.name.matches("noreference") or template.name.matches("noreferences") or template.name.matches("norefs") or template.name.matches("nosources") or template.name.matches("nr") or template.name.matches("ref needed") or template.name.matches("references") or template.name.matches("references needed") or template.name.matches("refsneeded") or template.name.matches("uncited article") or template.name.matches("uncited-article") or template.name.matches("unr") or template.name.matches("unref") or template.name.matches("unref'd") or template.name.matches("unrefarticle") or template.name.matches("unreferences article") or template.name.matches("unreferenced stub") or template.name.matches("unreferencedarticle") or template.name.matches("unrf") or template.name.matches("unsourced") or template.name.matches("unverified"):
        return "unreferenced"
    elif (template.name.matches("Unreferenced section") or template.name.matches("Cite")
    or template.name.matches("Nocite")
    or template.name.matches("Noref")
    or template.name.matches("Noref-section")
    or template.name.matches("Ref")
    or template.name.matches("References-s")
    or template.name.matches("Section")
    or template.name.matches("Section")
    or template.name.matches("Section-unsourced")
    or template.name.matches("Uncited")
    or template.name.matches("Uncited-section")
    or template.name.matches("UncitedSection")
    or template.name.matches("Unref")
    or template.name.matches("Unref")
    or template.name.matches("Unref")
    or template.name.matches("Unref-sect")
    or template.name.matches("Unref-section")
    or template.name.matches("Unreferenced")
    or template.name.matches("Unreferenced")
    or template.name.matches("Unreferenced")
    or template.name.matches("Unreferenced-sect")
    or template.name.matches("Unreferenced-section")
    or template.name.matches("Unreferencedsec")
    or template.name.matches("Unreferencedsect")
    or template.name.matches("UnreferencedSection")
    or template.name.matches("Unreferencedsection")
    or template.name.matches("Unrefs")
    or template.name.matches("Unrefsec")
    or template.name.matches("Unrefsect")
    or template.name.matches("Unrefsection")
    or template.name.matches("Unrs")
    or template.name.matches("Unsourced")
    or template.name.matches("Unsourced-section")
    or template.name.matches("Unsourcedsect")
    or template.name.matches("Unsourcedsection")
    or template.name.matches("Urs")):
        return "unreferenced section"
    else:
        return False

def process_page(text,dry_run):
    wikicode = mwparserfromhell.parse(text)
    templates = wikicode.filter_templates()
    content_changed = False

    code = mwparserfromhell.parse(text) # parse WikiCode on page
    for template in code.filter_templates():
        type = figure_type(template)
        if(type):
            try:
                code.remove(template)
                print(str(template) + " removed")
            except ValueError:
                raise   # deal with this at a higher level
    return [content_changed, str(code)] # get back text to save

def category_run(utils, site, offset,limited_run,pages_to_run):
    if utils is None:
        raise ValueError("Utils cannot be empty!")
    if site is None:
        raise ValueError("Site cannot be empty!")
    if offset is None:
        raise ValueError("Offset cannot be empty!")
    if limited_run is None:
        raise ValueError("limited_run cannot be empty!")
    if pages_to_run is None:
        raise ValueError("""Seriously? How are we supposed to run pages in a
        limited test if none are specified?""")
    counter = 0
    pageList = getTransclusions(site,"Template:Orphan")
    pageList2 = getTransclusions(site,"Template:Underlinked")
    pageList3 = getTransclusions(site,"Template:Uncategorized")
    pageList4 = getTransclusions(site,"Template:Unreferenced")
    joined_list = [y for x in [pageList, pageList2, pageList3, pageList4] for y in x]
    del pageList
    del pageList2
    del pageList3
    del pageList4
    print(joined_list)
        #with open('temp.txt', 'w') as f:
        #for item in joined_list:
            #print(item)
            #   f.write(str(item) + "\n")
            #return
    for page1 in joined_list:#joined_list:#site.Categories[cat_name]:
        if offset > 0:
            offset -= 1
            print("Skipped due to offset config")
            continue
        #if page1 == "":
        #   print("PAGE BLANK")
        #   continue
        page = site.Pages[page1]
        print("Working with: " + page.name + " " + str(counter))
        if page.name == "":
            print("PAGE BLANK")
            f = open("blank titles.txt",'a+')
            f.write(page.name + "\n")
            f.close()
        #  counter+=1
        #continue
        else:
            text = page.text()
            try:
                save_edit(page, utils, text)
            except ValueError as err:
                print(err)
    return
def main():
    dry_run = False
    pages_to_run = 7
    offset = 0
    #category = "Dts templates with deprecated parameters"
    limited_run = True

    parser = argparse.ArgumentParser(prog='DeprecatedFixerBot Music infobox fixer', description='')
    parser.add_argument("-dr", "--dryrun", help="perform a dry run (don't actually edit)",
                    action="store_true")
    args = parser.parse_args()
    if args.dryrun:
        dry_run = True
        print("Dry run")

    site = mwclient.Site(('https','en.wikipedia.org'), '/w/')
    if dry_run:
        pathlib.Path('./tests').mkdir(parents=False, exist_ok=True)
    config = configparser.RawConfigParser()
    config.read('credentials.txt')
    try:
        #pass
        site.login(config.get('enwiki_sandbot','username'), config.get('enwiki_sandbot', 'password'))
    except errors.LoginError as e:
        print(e)
        raise ValueError("Login failed.")

    utils = [config,site,dry_run]
    try:
        category_run(utils, site, offset,limited_run,pages_to_run)
    except ValueError as e:
        print("\n\n" + str(e))

if __name__ == "__main__":
    main()
