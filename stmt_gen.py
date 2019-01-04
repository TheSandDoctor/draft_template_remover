#!/usr/bin/env python3.6
text = """
    Template:Cite sources section
    Template:Nocite section
    Template:Noref section
    Template:Noref-section
    Template:Ref needed section
    Template:References-s
    Template:Section ref needed
    Template:Section unsourced
    Template:Section-unsourced
    Template:Uncited section
    Template:Uncited-section
    Template:UncitedSection
    Template:Unref Sect
    Template:Unref sect
    Template:Unref section
    Template:Unref-sect
    Template:Unref-section
    Template:Unreferenced list
    Template:Unreferenced Section
    Template:Unreferenced section
    Template:Unreferenced-sect
    Template:Unreferenced-section
    Template:Unreferencedsec
    Template:Unreferencedsect
    Template:UnreferencedSection
    Template:Unreferencedsection
    Template:Unrefs
    Template:Unrefsec
    Template:Unrefsect
    Template:Unrefsection
    Template:Unrs
    Template:Unsourced section
    Template:Unsourced-section
    Template:Unsourcedsect
    Template:Unsourcedsection
    Template:Urs"""
text = text.split()
def remove_temp(s):
    return s[9:]    # strips "Template:"
text = [remove_temp(s) for s in text]
for i in text:
    print("or template.name.matches(\"" + i + "\") ")
