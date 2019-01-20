data = [line.strip() for line in open("./redirects_final_filtered.txt", 'r')]
data2 = ["Template:" + line.strip() for line in open("./stub_types.txt", 'r')]
#print(data2[0])
#for d in data2:
#    d = "Template:" + d
data = data + data2
with open("./temp.txt",mode='wt',encoding='utf-8') as f:
    for i in data:
        f.write(i + "\n")
        #f.write(i + "\n")
