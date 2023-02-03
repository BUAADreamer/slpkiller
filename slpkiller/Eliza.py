#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

data = [
    (re.compile(r'.*我很(难受|伤心|开心|高兴).*'), '为什么你会{}'),
    (re.compile(r'.*我感到(难受|伤心).*'), '很遗憾你感到{}'),
    (re.compile(r'.*我经常(.*)[。？！，：；]*'), '能举个你{}的例子嘛？')
]


def eliza(text: str):
    for pattern, answer in data:
        res = re.search(pattern, text)
        if res:
            key = res.group(1)
            answer = answer.format(key)
            return answer
    return '好的'


if __name__ == '__main__':
    print('我是中文eliza，开始和我对话吧')
    while True:
        try:
            s = input()
            ans = eliza(s)
            print(ans)
        except EOFError:
            break
