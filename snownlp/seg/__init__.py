# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import re

from . import seg as TnTseg

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'seg.marshal')
segger = TnTseg.Seg()
segger.load(data_path, True)
re_zh = re.compile('([\u4E00-\u9FA5]+)')


def seg(sent):
    """
    获得句子的单词？
    拆单词， 单个汉字为 + 相邻其他符号作为整体 组成的列表
    :param sent: 句子
    :return: 单个汉字为 + 相邻其他符号作为整体 组成的列表
    """
    words = []
    for s in re_zh.split(sent):
        s = s.strip()
        if not s:
            continue
        if re_zh.match(s):
            # 如果是汉字，把这个片段汉字作为一个列表加到 words 列表的后面
            words += single_seg(s)
        else:
            # 如果不是汉字， 作为一个整体添加到 words 后面
            for word in s.split():
                word = word.strip()
                if word:
                    words.append(word)
    return words


def train(fname):
    global segger
    segger = TnTseg.Seg()
    segger.train(fname)


def save(fname, iszip=True):
    segger.save(fname, iszip)


def load(fname, iszip=True):
    segger.load(fname, iszip)


def single_seg(sent):
    return list(segger.seg(sent))
