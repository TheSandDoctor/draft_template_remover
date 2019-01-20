import json
data = None
with open('redirects_exist.txt',mode='r') as f:
    data = json.load(f)
with open("formatted_redirects_exist.txt",mode='w') as f:
    f.write(json.dumps(data,sort_keys=True,indent=4))
