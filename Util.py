import re
from heapq import heappush,heappop
from collections import OrderedDict

def genSeed(key):
    seed , i , res = [0]*5 , 0 , 0
    for ch in key:
        if ord(ch)>=ord('a') and ord(ch)<=ord('z'):
            ans = ord('a')
        elif ord(ch)>=ord('A') and ord(ch)<=ord('Z'):
            ans = ord('A')
        else:
            ans = ord('0')
        seed[i % 5] += ord(ch)-ans
        i += 1
    for i in range(5):
        seed[i] /= 5
        res += pow(26,i)*seed[i]

    return round(res)


def eliminateLevels(modified_dict,ori_dict,pre, minlen=9):
    sum,valid = 0,0
    if not isinstance(ori_dict, dict):
        return modified_dict,1,0
    for key in ori_dict:
        key_m = ''.join(re.findall(r'[A-Za-z]', key))
        if isinstance(ori_dict[key], dict):
            _ ,s,v = eliminateLevels(modified_dict, ori_dict[key], pre+key_m)
            sum+=s
            valid+=v
        elif isinstance(ori_dict[key], list):
            for ind,item in enumerate(ori_dict[key]):
                _, s, v = eliminateLevels(modified_dict, item, pre + key_m + str(dec2alpha(ind)))
                sum += s
                valid += v

        elif not isinstance(ori_dict[key], bool) and isinstance(ori_dict[key], (int,str,float)):
            sum += 1
            temp = str(ori_dict[key])
            if len(''.join(re.findall(r'[A-Za-z0-9]', temp))) > minlen and temp[0] != '{':
                modified_dict[pre+key_m] = ori_dict[key]
                valid += 1

    return modified_dict,sum,valid


def dec2alpha(dec):
    dec += 1
    res = ""
    while dec != 0:
        alp = dec % 26
        res += chr(ord('A')-1+dec)
        dec = int(dec/26)

    return res

# 将字典变为Java的TreeMap
def toTreeMap(paramMap):
    "将paramMap转换为java中的treeMap形式.将map的keys变为heapq.创建有序字典."
    keys=paramMap.keys()
    heap=[]
    for item in keys:
        heappush(heap,item)

    sort=[]
    while heap:
        sort.append(heappop(heap))

    resMap=OrderedDict()
    for key in sort:
        resMap[key]=paramMap.get(key)

    return resMap


# // BKDR
# Hash
# Function
# unsigned
# int
# BKDRHash(char * str)
# {
#     unsigned
# int
# seed = 131; // 31
# 131
# 1313
# 13131
# 131313
# etc..
#     unsigned
# int
# hash = 0;
#
# while (*str)
#     {
#         hash = hash * seed + (*str + +);
#     }
#
#     return (hash & 0x7FFFFFFF);
# }
def BKDRHash(str,seed=131):
    # seed = 131
    hash = 0
    for ch in str:
        if ord(ch)>=ord('a') and ord(ch)<=ord('z'):
            ans = ord(ch)-ord('a')
        elif ord(ch)>=ord('A') and ord(ch)<=ord('Z'):
            ans = ord(ch)-ord('A')
        else:
            ans = ord(ch)-ord('0')
        hash = hash * seed + ans
        hash = hash & 0x7FFFFFFF

    return hash



