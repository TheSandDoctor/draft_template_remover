#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import mwclient, configparser, mwparserfromhell, argparse,re, pathlib, json
from time import sleep
from mwclient import errors
import fpaths

templates_set = set()
def getTransclusions(site,page,sleep_duration = None,extra=""):
    cont = None
    pages = []
    i = 1
    while(1):
        result = site.api('query',list='embeddedin',einamespace=118,eititle=str(page),eicontinue=cont,eilimit=500,format='json')
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

def call_home(site):
    h_page = site.Pages['User:TheSandBot/status']
    text = h_page.text()
    return bool(json.loads(text)["run"]["draft_na_template_remover"])

def save_edit(page, utils, text):
    config,site = utils
    original_text = text

    code = mwparserfromhell.parse(text)

    if not call_home(site):#config):
        raise ValueError("Kill switch on-wiki is false. Terminating program.")
    time = 0
    edit_summary = """Removed [[Template:Orphan]], [[Template:Uncategorized]], [[Template:Unreferenced]], and/or [[Template:Underlinked]] (N/A in the draft namespace). Questions? [[User talk:TheSandDoctor|msg TSD!]] Please mention that this is task #2! ([[WP:Bots/Requests for approval/TheSandBot 2|BRFA]])"""
    while True:
        if time == 1:
            """
            There was an edit error (probably an edit conflict),
            so best to refetch the page and rerun.
            """
            text = site.Pages[page.page_title].text()
        try:
            content_changed, text = process_page(original_text)
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
            pathlib.Path(fpaths.errors_record_dir).mkdir(parents=False, exist_ok=True)
            title = get_valid_filename(page.page_title)
            text_file = open(fpaths.errors_prefix + title + ".txt", "w")
            text_file.write("Error present: " +  str(e) + "\n\n\n\n\n" + text)
            text_file.close()
            text_file = open(fpaths.errors_list_txt_name, "a+")
            text_file.write(page.page_title + "\n")
            text_file.close()
            text_file = open(fpaths.errors_list_txt_name_wikified, "a+")
            text_file.write("#[[" + page.page_title + "]]" + "\n")
            text_file.close()
            return
        try:
            if content_changed:
                page.save(text, summary=edit_summary, bot=True, minor=True)
                print("Saved page")
                f = open(fpath.changes_txt_name,'a+')
                f.write(page.name + "\n")
                f.close()
        except errors.ProtectedPageError:
            print('Could not edit ' + page.page_title + ' due to protection')
        except errors.EditError:
            print("Error")
            time = 1
            sleep(5)   # sleep for 5 seconds before trying again
            continue
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

def process_page(text):
    wikicode = mwparserfromhell.parse(text)
    templates = wikicode.filter_templates()
    content_changed = False

    code = mwparserfromhell.parse(text) # parse WikiCode on page
    for template in code.filter_templates():
        #type = figure_type(template)
        #if(type):
        if template.name.lower() in templates_set:
            try:
                code.remove(template)
                print(str(template) + " removed")
                deb = open(fpaths.debug_path, "a+")
                deb.write(str(template) + "removed\n")
                deb.close()
                content_changed = True
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
    joined_list = []
    for temp in templates_set:
        joined_list.extend(getTransclusions(site, temp)
    #pageList = getTransclusions(site,"Template:Orphan")
    #pageList2 = getTransclusions(site,"Template:Underlinked")
    #pageList3 = getTransclusions(site,"Template:Uncategorized")
    #pageList4 = getTransclusions(site,"Template:Unreferenced")
   # pageList5 = []
 #   for stub in templates_set:
  #      pageList5.append(getTransclusions(site,stub))

    #joined_list = [y for x in [pageList, pageList2, pageList3, pageList4, pageList5] for y in x]
    #joined_list = [y for x in [pageList, pageList2, pageList3, pageList4] for y in x]
    #del pageList
    #del pageList2
    #del pageList3
    #del pageList4
    #del pageList5
    #print(joined_list)
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
            f = open(fpaths.blank_titles_txt_name,'a+')
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

def find_redirects(page):
    if len(list(page.backlinks(filterredir='redirects'))) == 0:
        templates_set.add(page.name.lower())
    else:
        for i in page.backlinks(filterredir='redirects'):
            find_redirects(i)


def main():
    pages_to_run = 7
    offset = 0
    #category = "Dts templates with deprecated parameters"
    limited_run = True
    templates_set = set(line.strip().lower() for line in open(fpaths.temp_types_path))
    #templates_set = set(line.strip().lower() for line in open('stub_types.txt'))
    #templates_temp = set(line.strip().lower()[9:] for line in open('redirects_final_filtered.txt'))
    #templates_set.update(templates_temp)
    #del templates_temp

    site = mwclient.Site(('https','en.wikipedia.org'), '/w/')
    config = configparser.RawConfigParser()
    config.read(fpaths.credentials_path)
    try:
        #pass
        site.login(config.get('enwiki_sandbot','username'), config.get('enwiki_sandbot', 'password'))
    except errors.LoginError as e:
        print(e)
        raise ValueError("Login failed.")

    utils = [config,site]
    try:
        category_run(utils, site, offset,limited_run,pages_to_run)
    except ValueError as e:
        print("\n\n" + str(e))

if __name__ == "__main__":
    main()
