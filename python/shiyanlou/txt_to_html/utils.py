#!/usr/bin/env python
# coding=utf-8
# Author: 
# Mail: 
# Created Time: 2019年08月01日 星期四 14时36分05秒



def lines(self):
    '''
    生成器,在文本最后加最后一空行
    '''
    for line in file:yield line
    yield '\n'


def blocks(file):
    '''
    生成器,生成单独的文本块
    '''
    blocks = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
