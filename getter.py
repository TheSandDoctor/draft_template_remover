#!/usr/bin/env python3.6
import mwclient,mwparserfromhell,sys
stub_types = ["Wikipedia:WikiProject_Stub_sorting/Stub_types/General",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/History",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/People",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/Science",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/Technology",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/Transport",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/Military_and_weaponry",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/Organizations",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/Miscellaneous",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/Leisure",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/Government,_law,_and_politics",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/Commerce",
"Wikipedia:WikiProject_Stub_sorting/Stub_types/Education"]

site = mwclient.Site(('https','en.wikipedia.org'), '/w/')
#pages = [site.Pages['Wikipedia:WikiProject_Stub_sorting/Stub_types/Science']]
pages = [site.Pages[i] for i in stub_types] # turn stub_types into page object list
stub_types = []
for page in pages:
    code = mwparserfromhell.parse(page.text())
    print("Adding all in " + page.name + "\n\n")
    for template in code.filter_templates():
        if (template.name.matches("tl") or
            template.name.matches("t") or
            template.name.matches("t1") or
            template.name.matches("temp") or
            template.name.matches("template") or
            template.name.matches("template link") or
            template.name.matches("templatelink") or
            template.name.matches("tl1") or
            template.name.matches("tmpl") or
            template.name.matches("tp")):
            stub_types.append(str(template.get(1).value))
            print(template.get(1).value)
    #with open(str(page.name)[46:] + ".txt",mode='a+',encoding='utf-8') as f:
# f.write('\n*'.join(stub_types))
#stub_types = []
with open("stub_types.txt",mode='a+',encoding='utf-8') as f:
    f.write('\n*'.join(stub_types))
print(len(stub_types) != len(set(stub_types)))
