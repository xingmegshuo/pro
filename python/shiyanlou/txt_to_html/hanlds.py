#!/usr/bin/env python
# coding=utf-8
# Author: 
# Mail: 
# Created Time: 2019年08月01日 星期四 14时51分58秒


class Handler:
    '''
    处理程序父类
    '''
    def callback(self,prefix,name,*args):
        method = getattr(self,prefix+name,None)
        if callable(method):return method(*args)


    def start(self,name):
        self.callback('strat_',name)


    def end(self,name):
        self.callback('end_',name)


    def sub(self,name):
        def substitution(match):
            result = self.callback('sub_',name,match)
            if result is None: result = match.group(0)
            return result
        return substitution


class HTMLRenderer(Handler):
    '''
    HTML处理程序，给文本块加相应的HTML
    '''
    def start_document(slef):
        print('<html><head><title>what</title></head><body>')


    def end_doucument(self):
        print('</body></html>')


    def start_paragraph(self):
        print('<p style="color:#444">;')


    def end_paragraph(self):
        print('</p>')


    def start_heading(self):
        print('<h2 style="color:#68BE5D;">')


    def end_heading(self):
        print('</h2>')


    def start_list(self):
        print('<ul style="color:#363736;">')


    def end_list(slef):
        print('</ul>')


    def start_listitem(self):
        print('<li>')


    def end_listitem(self):
        print('</li>')


    def start_title(self):
        print('<h1 style="color:#1ABC9C;">')


    def end_title(self):
        print('</h1>')


    def sub_emphasis(self,match):
        return('<em>{}</em>'.format(match.group(1)))


    def sub_url(self,match):
        return('<a target="_blank" stytle="text-decoration:none;color:#BC1A4B;"herf="%s">%s</a>'%(match.group(1),match.group(1)))


    def sub_mail(self,match):
        return('<a stytle="text-decoration:none;color:#BC1A4B;"herf="mailto:%s">%s</a>'%(match.group(1),match.group(1)))


    def feed(self,data):
        print(data)

