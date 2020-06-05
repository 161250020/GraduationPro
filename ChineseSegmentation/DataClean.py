import re
from ChineseSegmentation import FileController as fc


# 去除非中文字符
def clean_regular(content):
    string = re.sub(r"[^\u4e00-\u9fff]", " ", content)
    string = re.sub(r"\s{2,}", " ", content)
    return string.strip()


def clean_symbol(content):
    return re.split('（|）|，|。|；|·|！|？|\n', content)


def clean_stop_word(content):
    stop_words = fc.get_stop_words()
    result = ""
    i = 0
    for word in content:
        if word not in stop_words:
            if i > 0:
                result = result + " " + word
            else:
                result = result + word
            i = i + 1
    return result
