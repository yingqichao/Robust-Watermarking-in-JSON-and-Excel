import random
import re

def randomattack(JSON,minlen=9,total=0.5,core=0.8):
    # "total" defines the total scale of truncated keys
    # "core" defines the scale of truncated used keys
    remove_valid, remain_valid, remove_invalid, remain_invalid = 0, 0, 0, 0
    if not isinstance(JSON, dict):
        return JSON,0,0,0,1
    keys = list(JSON.keys())
    for key in keys:
        if isinstance(JSON[key], dict):
            _, rmv_v, rmn_v,rmv_iv, rmn_iv = randomattack(JSON[key], minlen, total,core)
            remove_valid += rmv_v
            remain_valid += rmn_v
            remove_invalid += rmv_iv
            remain_invalid += rmn_iv
        elif not isinstance(JSON[key], bool) and isinstance(JSON[key], (int, str, float)):
            temp = str(JSON[key])
            if len(''.join(re.findall(r'[A-Za-z0-9]', temp))) > minlen and temp[0] != '{':
                #valid key
                if random.random() > core:
                    del JSON[key]
                    remove_valid += 1
                else:
                    remain_valid += 1
            else:
                # invalid key
                if random.random() > total:
                    del JSON[key]
                    remove_invalid += 1
                else:
                    remain_invalid += 1
        elif isinstance(JSON[key], list):
            for ind,item in enumerate(JSON[key]):
                _, rmv_v, rmn_v, rmv_iv, rmn_iv = randomattack(item, minlen,total, core)
                remove_valid += rmv_v
                remain_valid += rmn_v
                remove_invalid += rmv_iv
                remain_invalid += rmn_iv
        else:
            # invalid key
            if random.random() > total:
                del JSON[key]
                remove_invalid += 1
            else:
                remain_invalid += 1

    return JSON, remove_valid, remain_valid, remove_invalid, remain_invalid


# _, rmv_v, rmn_v, rmv_iv, rmn_iv = randomattack(JSON[key], total, core)

def randommodification(JSON,minlen=9,total=0.5,core=0.8,modifystrength = 0.2):
    remove_valid, remain_valid, remove_invalid, remain_invalid = 0, 0, 0, 0
    if not isinstance(JSON, dict):
        return JSON, 0, 0, 0, 1
    keys = list(JSON.keys())
    for key in keys:
        if isinstance(JSON[key], dict):
            _, rmv_v, rmn_v, rmv_iv, rmn_iv = randommodification(JSON[key], minlen,total, core)
            remove_valid += rmv_v
            remain_valid += rmn_v
            remove_invalid += rmv_iv
            remain_invalid += rmn_iv
        elif not isinstance(JSON[key], bool) and isinstance(JSON[key], (int, str, float)):
            temp = str(JSON[key])
            if len(''.join(re.findall(r'[A-Za-z0-9]', temp))) > minlen and temp[0] != '{':
                # valid key
                if random.random() > core:
                    JSON[key] = modification(JSON[key],modifystrength)
                    remove_valid += 1
                else:
                    remain_valid += 1
            else:
                # invalid key
                if random.random() > total:
                    JSON[key] = modification(JSON[key],modifystrength)
                    remove_invalid += 1
                else:
                    remain_invalid += 1
        elif isinstance(JSON[key], list):
            for ind, item in enumerate(JSON[key]):
                _, rmv_v, rmn_v, rmv_iv, rmn_iv = randommodification(JSON[key], minlen,total, core)
                remove_valid += rmv_v
                remain_valid += rmn_v
                remove_invalid += rmv_iv
                remain_invalid += rmn_iv
        else:
            # invalid key
            if random.random() > total:
                JSON[key] = modification(JSON[key],modifystrength)
                remove_invalid += 1
            else:
                remain_invalid += 1

    return JSON, remove_valid, remain_valid, remove_invalid, remain_invalid

def modification(value,modifystrength=0.2):
    sr = list(str(value))
    for id,ch in enumerate(sr):
        if random.random() < modifystrength:
            sr[id] = chr(ord(sr[id]) + 1)

    return ''.join(sr)



