#!/usr/bin/env python
# coding=utf-8
# Author: 
# Mail: 
# Created Time: 2019年08月01日 星期四 17时25分27秒

import sys,re
from handlers import *
from utils import *
from rules import *



class Parser:
    def __init__(self,handler):
        self.handler = handler
        self.rules = []
        self.filters = []


    def addRule(self,rule):
        self.rules.append(rule)


    def addFilter(self,pattern,name):
        def filter(block,handler):
            return re.sub(pattern,handler.sub(name),block)
        self.filters.append(filter)


    def parse(self,file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block,self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block,self.handler)
                    if last: break
        self.handler.end('document')



class BasicTextParser(Parser):
    def __init__(self,handler):
        Parser.__init__(self,handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilter(r'\*(.+?)\*','emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)','url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)','mail')



headler = HTMLRenderer()
parser = BasicTextParser(handler)
parser.parse(sys.stdin)

