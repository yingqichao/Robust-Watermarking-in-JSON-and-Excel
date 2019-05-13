import sys

import sampler
import json
import re


def _split_file(f_bytes, blocksize):
    """Block file byte contents into blocksize chunks, padding last one if necessary
    """

    blocks = [int.from_bytes(f_bytes[i:i+blocksize].ljust(blocksize, b'0'), sys.byteorder)
            for i in range(0, len(f_bytes), blocksize)]
    return len(f_bytes), blocks


def genSeed(key):
    seed , i , res = [0]*5 , 0 , 0
    for ch in key:
        seed[i % 5] += ord(ch)-ord('a')
        i += 1
    for i in range(5):
        seed[i] /= 5
        res += pow(26,i)*seed[i]

    return round(res)


def modify(key, data, prng):

    key1 = key
    if isinstance(key, int):
        key1 = str(key)
    elif isinstance(key, float):
        key1 = str(key)
        index = key1.find(".")
        key1 = key1.replace(".","")


    s1, Set, ind = list(key1), set(), 0
    while ind < 5:
        num = prng.get_next() % len(key1)
        if num not in Set:
            Set.add(num)
            ori = ord(s1[num])
            s1[num] = chr(ori - ori % 2 + data % 2)
            data = int(data/2)
            ind += 1

    key1 = ''.join(s1)

    if isinstance(key, int):
        key1 = int(key1)
    elif isinstance(key, float):
        key1 = key1[0:index-1]+"."+key1[index:len(key1)]
        key1 = float(key1)

    return key1


def encoder(f_bytes,JSON, blocksize,  c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA,):
    """Generates an infinite sequence of blocks to transmit
    to the receiver
    """


    # get file blocks
    filesize, blocks = _split_file(f_bytes, blocksize)

    # init stream vars
    K = len(blocks)
    prng = sampler.PRNG(params=(K, delta, c))


    # block generation loop
    for key in JSON:
        # Every Key has its unique Seed according to its alphabet
        seed = genSeed(key)
        prng.set_seed(seed)
        blockseed, d, ix_samples = prng.get_src_blocks()
        block_data = 0
        for ix in ix_samples:
            block_data ^= blocks[ix]

        #根据结果修改JSON
        JSON[key] = modify(JSON[key], block_data, prng)

    return JSON


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


def run(f_bytes, JSON, blocksize=1, seed=1, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA , numpacks=30):
    print("-----------------------------Embedding---------------------------------------")
    modified_json = {}
    modified_json, sum, valid = eliminateLevels(modified_json, JSON, "")
    print(modified_json)
    print("Sum of KEYS: " + str(sum) + ". Sum of Valid: " + str(valid))

    block = encoder(f_bytes, modified_json, blocksize,  c, delta)
    json_str = json.dumps(block)
    with open('target.txt', 'w') as rf:
        rf.writelines(json_str)
    print('-----------------Embedding was conducted successfully...--------------------')


if __name__ == '__main__':
    pass
    # run(fn="text.txt", blocksize=1, seed=1, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA, numpacks=20)

