import json
import re
import types

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
    with open('original.txt', 'r') as f:
        JSON = json.load(f)

    for key in JSON:

        print(key+" "+str(isinstance(JSON[key],dict)))
        # print(JSON)

    # #用re只保留英文字母
    # st = "hello,world!!%[545]你好234世界。。。"
    # result = ''.join(re.findall(r'[A-Za-z]', st))
    # print(result)

