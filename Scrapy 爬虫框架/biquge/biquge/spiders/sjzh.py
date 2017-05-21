'''
实现了中文向阿拉伯数字转换
用于从小说章节名提取id来排序
'''



chs_arabic_map = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
                  '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                  '十': 10, '百': 100, '千': 10 ** 3, '万': 10 ** 4,
                  '〇': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4,
                  '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
                  '拾': 10, '佰': 100, '仟': 10 ** 3, '萬': 10 ** 4,
                  '亿': 10 ** 8, '億': 10 ** 8, '幺': 1,
                  '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                  '7': 7, '8': 8, '9': 9}

num_list = ['1','2','4','5','6','7','8','9','0','一','二','三','四','五','六','七','八','九','十','零','千','百',]

def get_tit_num(title):
    result =''
    for char in title:
        if char in num_list:
            result+=char
    return result


def Cn2An(chinese_digits):

    result = 0
    tmp = 0
    hnd_mln = 0
    for count in range(len(chinese_digits)):
        curr_char = chinese_digits[count]
        curr_digit = chs_arabic_map[curr_char]
        # meet 「亿」 or 「億」
        if curr_digit == 10 ** 8:
            result = result + tmp
            result = result * curr_digit
            # get result before 「亿」 and store it into hnd_mln
            # reset `result`
            hnd_mln = hnd_mln * 10 ** 8 + result
            result = 0
            tmp = 0
        # meet 「万」 or 「萬」
        elif curr_digit == 10 ** 4:
            result = result + tmp
            result = result * curr_digit
            tmp = 0
        # meet 「十」, 「百」, 「千」 or their traditional version
        elif curr_digit >= 10:
            tmp = 1 if tmp == 0 else tmp
            result = result + curr_digit * tmp
            tmp = 0
        # meet single digit
        elif curr_digit is not None:
            tmp = tmp * 10 + curr_digit
        else:
            return result
    result = result + tmp
    result = result + hnd_mln
    return result
    

# test
print (Cn2An(get_tit_num('第一千三百九十一章 你妹妹被我咬了！')))