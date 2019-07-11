#/usr/bin/env python
# -*- coding: UTF-8 -*-

import HTMLParser
import argparse
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

class BookMarkHTMLParser(HTMLParser.HTMLParser):  
    """
    使用 HtmlParser 解析 Google Chrome 导出的 BookMark，并输出 Markdown 格式的字符串
    """ 
    def __init__(self, writer):   
        HTMLParser.HTMLParser.__init__(self)   
        self.link = ""
        self.content = ""
        self.target_group_tag = "h3"
        self.target_group = False
        self.target = False
        self.target_tag = "a"
        self.writer = None
        if writer:
            self.writer = writer

    def handle_starttag(self, tag, attrs):   
        # print "Encountered the beginning of a %s tag" % tag   
        if tag.lower() == self.target_tag:  
            self.target = True
            if len(attrs) == 0:   
                pass   
            else:   
                for (variable, value) in attrs:   
                    if variable == "href":   
                        self.link = value
        
        if tag.lower() == self.target_group_tag: 
            self.target_group = True


    def handle_endtag(self, tag): 
        # print "Encountered the end of a %s tag" % tag
        if tag.lower() == self.target_tag: 
            self.target = False
        if tag.lower() == self.target_group_tag:
            self.target_group = False

    def handle_data(self, data): 
        if self.target is True:
            self.content = data.decode('utf-8') # python 2 unicode 中文字符源码输出解决
            if self.writer:
                self.writer.write("[{}]({})  \n".format(self.content, self.link))
            else:
                print "[{}]({})  ".format(self.content, self.link)
        if self.target_group is True:
            if self.writer:
                self.writer.write("## {}  \n".format(data.decode('utf-8')))
            else:
                print "## {}  ".format(data.decode('utf-8'))

def main():
    parser = argparse.ArgumentParser(usage="\n\tpython2 "+ sys.argv[0] +" --bookmark bookmark_file [--markdown markdown_file]",
       description="Convert chrome bookmark file to markdown file.")
    parser.add_argument("--bookmark", help="the source bookmark file export from Chrome.")
    parser.add_argument("--markdown", default="", help="[optional] the target markdown file.")
    
    args = parser.parse_args()
    
    with open(args.bookmark, 'r') as f:
        w = None
        try:
            w = open(args.markdown, 'w')
        except:
            pass
        
        html_code = f.read()
        hp = BookMarkHTMLParser(w)
        hp.feed(html_code)   
        hp.close()


if __name__ == "__main__":
    
    main()

