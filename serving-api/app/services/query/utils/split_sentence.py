# -*- coding:utf-8 -*-
# @Time   :2022/1/11 2:39 下午
# @Author :Mengqi Li
# @FileName:split_sentence.py
import re

SEPARATOR = r"@"
RE_SENTENCE = re.compile(r"(\S.+?[.!?])(?=\s+|$)|(\S.+?)(?=[\n]|$)", re.UNICODE)
AB_SENIOR = re.compile(r"([A-Z][a-z]{1,2}\.)\s(\w)", re.UNICODE)
AB_ACRONYM = re.compile(r"(\.[a-zA-Z]\.)\s(\w)", re.UNICODE)
UNDO_AB_SENIOR = re.compile(r"([A-Z][a-z]{1,2}\.)" + SEPARATOR + r"(\w)", re.UNICODE)
UNDO_AB_ACRONYM = re.compile(r"(\.[a-zA-Z]\.)" + SEPARATOR + r"(\w)", re.UNICODE)


def replace_with_separator(text, separator, regexs):
    replacement = r"\1" + separator + r"\2"
    result = text
    for regex in regexs:
        result = regex.sub(replacement, result)
    return result


def split_sentence(text, best=True):
    """
    选用的是hanlp中提供的基于规则的分句子方法（还有一种基于模型分句）
    :param text: 待分句的字符串
    :param best:
    :return:
    """
    text = re.sub("([。！？\?])([^”’])", r"\1\n\2", text)
    text = re.sub("(\.{6})([^”’])", r"\1\n\2", text)
    text = re.sub("(\…{2})([^”’])", r"\1\n\2", text)
    text = re.sub("([。！？\?][”’])([^，。！？\?])", r"\1\n\2", text)
    for chunk in text.split("\n"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if not best:
            yield chunk
            continue
        processed = replace_with_separator(chunk, SEPARATOR, [AB_SENIOR, AB_ACRONYM])
        for sentence in RE_SENTENCE.finditer(processed):
            sentence = replace_with_separator(
                sentence.group(), r" ", [UNDO_AB_SENIOR, UNDO_AB_ACRONYM]
            )
            yield sentence
