'''
为了小说排序
让中文数字转换成
阿拉伯数字
没有考虑千万的转换
因为小说章节并没有那么多章节
'''


numDic = {
    '零': '0',
    '一': '1',
    '二': '2',
    '三': '3',
    '四': '4',
    '五': '5',
    '六': '6',
    '七': '7',
    '八': '8',
    '九': '9',
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
}


def Ch2Num(name):
    num = ''
    for char in name:
        if char in numDic.keys():
            num += numDic[char]
    return num



chs_arabic_map = {u'零':0, u'一':1, u'二':2, u'三':3, u'四':4,
        u'五':5, u'六':6, u'七':7, u'八':8, u'九':9,
        u'十':10, u'百':100, u'千':10 ** 3, u'万':10 ** 4,
        u'〇':0, u'壹':1, u'贰':2, u'叁':3, u'肆':4,
        u'伍':5, u'陆':6, u'柒':7, u'捌':8, u'玖':9,
        u'拾':10, u'佰':100, u'仟':10 ** 3, u'萬':10 ** 4,
        u'亿':10 ** 8, u'億':10 ** 8, u'幺': 1,
        u'０':0, u'１':1, u'２':2, u'３':3, u'４':4,
        u'５':5, u'６':6, u'７':7, u'８':8, u'９':9}

def C2Num (chinese_digits):
    

    result  = 0
    tmp     = 0
    hnd_mln = 0
    for count in range(len(chinese_digits)):
        curr_char  = chinese_digits[count]
        curr_digit = chs_arabic_map.get(curr_char, None)
        # meet 「亿」 or 「億」
        if curr_digit == 10 ** 8:
            result  = result + tmp
            result  = result * curr_digit
            # get result before 「亿」 and store it into hnd_mln
            # reset `result`
            hnd_mln = hnd_mln * 10 ** 8 + result
            result  = 0
            tmp     = 0
        # meet 「万」 or 「萬」
        elif curr_digit == 10 ** 4:
            result = result + tmp
            result = result * curr_digit
            tmp    = 0
        # meet 「十」, 「百」, 「千」 or their traditional version
        elif curr_digit >= 10:
            tmp    = 1 if tmp == 0 else tmp
            result = result + curr_digit * tmp
            tmp    = 0
        # meet single digit
        elif curr_digit is not None:
            tmp = tmp * 10 + curr_digit
        else:
            return result
    result = result + tmp
    result = result + hnd_mln
    return result

print (C2Num('三千三百三十六'))