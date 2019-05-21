import random
import re

def randomattack(JSON,total=0.5,core=0.8):
    # "total" defines the total scale of truncated keys
    # "core" defines the scale of truncated used keys
    remove_valid, remain_valid, remove_invalid, remain_invalid = 0, 0, 0, 0
    if not isinstance(JSON, dict):
        return JSON,0,0,0,1
    keys = list(JSON.keys())
    for key in keys:
        if isinstance(JSON[key], dict):
            _, rmv_v, rmn_v,rmv_iv, rmn_iv = randomattack(JSON[key], total,core)
            remove_valid += rmv_v
            remain_valid += rmn_v
            remove_invalid += rmv_iv
            remain_invalid += rmn_iv
        elif not isinstance(JSON[key], bool) and isinstance(JSON[key], (int, str, float)):
            temp = str(JSON[key])
            if len(''.join(re.findall(r'[A-Za-z0-9]', temp))) > 5 and temp[0] != '{':
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
                _, rmv_v, rmn_v, rmv_iv, rmn_iv = randomattack(item, total, core)
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


def randommodification(JSON,total=0.5,core=0.8):
    remove_valid, remain_valid, remove_invalid, remain_invalid = 0, 0, 0, 0
    if not isinstance(JSON, dict):
        return JSON, 0, 0, 0, 1
    keys = list(JSON.keys())
    for key in keys:
        if isinstance(JSON[key], dict):
            _, rmv_v, rmn_v, rmv_iv, rmn_iv = randomattack(JSON[key], total, core)
            remove_valid += rmv_v
            remain_valid += rmn_v
            remove_invalid += rmv_iv
            remain_invalid += rmn_iv
        elif not isinstance(JSON[key], bool) and isinstance(JSON[key], (int, str, float)):
            temp = str(JSON[key])
            if len(''.join(re.findall(r'[A-Za-z0-9]', temp))) > 5 and temp[0] != '{':
                # valid key
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
            for ind, item in enumerate(JSON[key]):
                _, rmv_v, rmn_v, rmv_iv, rmn_iv = randomattack(item, total, core)
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
