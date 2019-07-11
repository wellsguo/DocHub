#coding: utf-8

with open ("colorTable.txt", "r") as text:
    for l in text.readlines():
        fileds = l.split("|")
        append = '<button style="background-color: #{0}; \
color: #FF0000; border: none">\
{0}</button>'.format(fileds[1].strip().replace("#",""))

        print(l.strip("\n")+ append)


