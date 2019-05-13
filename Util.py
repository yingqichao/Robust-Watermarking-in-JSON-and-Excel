import re


def genSeed(key):
    seed , i , res = [0]*5 , 0 , 0
    for ch in key:
        seed[i % 5] += ord(ch)-ord('a')
        i += 1
    for i in range(5):
        seed[i] /= 5
        res += pow(26,i)*seed[i]

    return round(res)


def eliminateLevels(modified_dict,ori_dict,pre):
    sum,valid = 0,0
    for key in ori_dict:
        key_m = ''.join(re.findall(r'[A-Za-z]', key))
        if isinstance(ori_dict[key], dict):
            _ ,s,v = eliminateLevels(modified_dict, ori_dict[key], pre+key_m)
            sum+=s
            valid+=v
        elif not isinstance(ori_dict[key], bool) and isinstance(ori_dict[key], (int,str,float)):
            sum += 1
            temp = str(ori_dict[key])
            if len(''.join(re.findall(r'[A-Za-z0-9]', temp)))>=5 and temp[0] != '{':
                modified_dict[pre+key_m] = ori_dict[key]
                valid += 1

    return modified_dict,sum,valid