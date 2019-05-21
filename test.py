import json
import re
import types
import Util
from hamming import encode, decode
from bitarray import bitarray


def genSeed(key):
    seed,i,res = [0]*5,0,0
    for ch in key:
        seed[i % 5] += ord(ch)-ord('a')
        i += 1
    for i in range(5):
        seed[i] /= 5
        res += pow(26,i)*seed[i]

    return round(res)



if __name__ == '__main__':
    # with open('original.txt', 'r') as f:
    #     JSON = json.load(f)
    #
    # for key in JSON:
    #
    #     print(key+" "+str(isinstance(JSON[key],dict)))
        # print(JSON)

    # #用re只保留英文字母
    # st = "hello,world!!%[545]你好234世界。。。"
    # result = ''.join(re.findall(r'[A-Za-z]', st))
    # print(result)

    # print(Util.BKDRHash("UserInfoALocationType"))
    # print(Util.BKDRHash("UserInfoBLocationType"))

    data = bitarray('1010')
    data_with_parity = encode(data)
    print(data_with_parity)
    data_with_parity[3] = not data_with_parity  # data now has a single bit in error..
    print(decode(data_with_parity)) # but Hamming codes can correct it!

