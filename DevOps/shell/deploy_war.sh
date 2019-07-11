#!/usr/bin/env bash

#set tomcat webapps path
tomcat_webapps_path=/usr/local/tomcat-8.5.31/webapps

# get the absoluth path of current file
cur_dir=$(cd "$(dirname "$0")"; pwd)
files=$(find  $cur_dir -maxdepth 1  -name '*.war')

# fix for loop splits on all whitespace
IFS=$'\n' 
for f in ${files}; 
do 
 echo copy "${f}" into $tomcat_webapps_path ...  
 sudo copy "${f}" $tomcat_webapps_path
done
unset IFS
