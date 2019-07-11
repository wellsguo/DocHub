#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

work_filepath = "#"
titles = []
imgs = []
max_length = 5

def gci(filepath):
  global work_filepath
  if filepath != work_filepath:
    print_md() 
    work_filepath = filepath
    print "## "+ work_filepath + "  "
    
  
  files = os.listdir(filepath)
  for fi in files:
    fi_d = os.path.join(filepath,fi)            
    if os.path.isdir(fi_d):
      gci(fi_d)                  
    else:
      if fi_d.endswith(".png") or fi_d.endswith(".jpg") or fi_d.endswith(".jpeg"):
        # print "|" + fi + "|  "
        # print "| :--: |  "
        # print "|<img src=\""+fi_d+"\" width=\"40px\" height=\"auto\"/>|  "
        # print "  "
        titles.append(fi)
        imgs.append(fi_d)
        
        if len(titles) %  max_length == max_length - 1 :
          print_md() 

def print_md():
  if not titles is None and len(titles) > 0:
    _titles = "|"
    _split = "|"
    _imgs =  "|"
    for i in range(len(titles)):
      _titles += titles[i] + "|"
      _split += " :--: |"
      _imgs += '<img src="'+imgs[i]+'" width="40px" height="auto"/>|'
      
    del titles[:]
    del imgs[:]
    
    print _titles + "  "
    print _split + "  "
    print _imgs + "  "
    print "  "
    
gci('./app/src/main/res')