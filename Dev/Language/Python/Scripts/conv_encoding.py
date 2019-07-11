#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import codecs
import chardet
reload(sys) 
sys.setdefaultencoding('utf8')

files=[]

def list_file(path):
    """
    该程序用于遍历指定目录下的文件
    :param path:    文件路径
    :return:    满足条件的文件或文件夹
    """
    file_list = os.listdir(path)
    for f in file_list:
        file_path = os.path.join(path, f)
        if os.path.isdir(file_path):
            list_file(file_path)
        else:
            files.append(file_path)

    return files



def convert(file, in_enc="GBK", out_enc="UTF-8"):
    """
    该程序用于将目录下的文件从指定格式转换到指定格式，默认的是GBK转到utf-8
    :param file:    文件路径
    :param in_enc:  输入文件格式
    :param out_enc: 输出文件格式
    :return:
    """
    in_enc = in_enc.upper()
    out_enc = out_enc.upper()
    file_name = file.split('\\')[-1]
    try:
        print("Convert [{}] From {} To {}...".format(file_name, in_enc, out_enc))
        f = codecs.open(file, 'r', in_enc)
        content = f.read()
        codecs.open(file, 'w', out_enc).write(content)
    except IOError as err:
        sys.stderr.write("[Error] [{}] {}\n".format(file_name, err))
    except UnicodeDecodeError as uerr:
        sys.stderr.write("[Error] [{}] {}\n".format(file_name, uerr))
    except UnicodeEncodeError as ueerr:
        sys.stderr.write("[Error] [{}] {}\n".format(file_name, ueerr))
    else:
        pass

def main():
    parser = argparse.ArgumentParser(usage="\n\tpython2 "+ sys.argv[0] +" --path filepath --enc endcoding",
       description="Convert file's encoding.")
    parser.add_argument("--path", help="file's path.")
    parser.add_argument("--enc", default="UTF-8", help="[optional] the target encoding.")
    
    args = parser.parse_args() 
    
    if args.path:
        files = list_file(args.path)
        for item in files:
            with open(item, "rb") as f:
                data = f.read()
                codeType = chardet.detect(data)['encoding']
                if not codeType.upper() == args.enc:
                    convert(item, codeType, args.enc)
                else:
                    pass
        
if __name__ == '__main__':

    main()
        