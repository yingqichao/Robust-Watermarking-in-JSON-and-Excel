import sys

import sampler
import json
import re
import Util
import hamming


class encode:
    def __init__(self,f_bytes,log=None,blocksize=1, seed=1, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA , numpacks=30):
        self.log = log
        self.blocksize, self.seed, self.c , self.delta , self.numpacks = 1,1,sampler.DEFAULT_C,sampler.DEFAULT_DELTA,30
        self.f_bytes = f_bytes.replace("\n","")
        # get file blocks
        self.filesize, self.blocks = self._split_file(self.f_bytes)

        # init stream vars
        K = len(self.blocks)
        self.prng = sampler.PRNG(params=(K, self.delta, self.c))


    def _split_file(self,f_bytes):
        """Block file byte contents into blocksize chunks, padding last one if necessary
        """
    
        blocks = [int(ord(f_bytes[i])-ord('a'))
                for i in range(0, len(f_bytes), self.blocksize)]
        return len(f_bytes), blocks

    
    def modify(self,key, data, prng):
    
        key1,first,ori_data = key,'',data
        #对于数字，首位不嵌入信息
        if isinstance(key, int):
            first = str(key)[0]
            key1 = str(key)[1:]
        elif isinstance(key, float):
            first = str(key)[0]
            key1 = str(key)[1:]
            index = key1.find(".")
            key1 = key1.replace(".","")

        s1, Set, ind = list(key1), set(), 0

        #Generate bitstream and sent it to the CRC
        text = bin(data).replace('0b', '')
        crc_text = '0'*(5-len(text)) + text + hamming.crc_remainder(text)

        while ind < len(crc_text):
            num = prng.get_next() % len(key1)
            if ind==0:
                buffer = num
            if num not in Set:
                Set.add(num)
                ori = ord(s1[num])
                if (ori >= 97 and ori <= 122) or (ori >= 65 and ori <= 90):
                    # 对于小写大写字母：统一向上取结果
                    s1[num] = chr(ori + ori % 2 - ord(crc_text[ind]) + ord('0'))
                elif ori >= 48 and ori <= 57:
                    # 对于数字：统一向下取结果
                    s1[num] = chr(ori - ori % 2 + ord(crc_text[ind]) - ord('0'))
                # data = int(data/2)
                ind += 1
    
        key1 = ''.join(s1)
    
        if isinstance(key, int):
            key1 = first + key1
            key1 = int(key1)
        elif isinstance(key, float):
            key1 = key1[0:index]+"."+key1[index:len(key1)]
            key1 = first + key1
            key1 = float(key1)
    
        self.log.write("Debug Embed: " + str(ori_data) + " " + str(buffer) + " " + str(key1))
        return key1
    
    
    def encoder(self,key,value):
        """Generates an infinite sequence of blocks to transmit
        to the receiver
        """

        # block generation loop
        # for key in JSON:
            # Every Key has its unique Seed according to its alphabet
        seed = Util.BKDRHash(key)
        self.prng.set_seed(seed)
        blockseed, d, ix_samples = self.prng.get_src_blocks()
        block_data = 0
        for ix in ix_samples:
            block_data ^= self.blocks[ix]

        #根据结果修改JSON
        return self.modify(value, block_data, self.prng)
        # return JSON

    def dec2alpha(self, dec):
        dec += 1
        res = ""
        while dec != 0:
            alp = dec % 26
            res += chr(ord('A') - 1 + dec)
            dec = int(dec / 26)

        return res

    def eliminateLevels(self, ori_dict, pre, minlen=9):
        sum, valid = 0, 0
        if not isinstance(ori_dict, dict):
            return ori_dict, 1, 0
        for key in ori_dict:
            key_m = ''.join(re.findall(r'[A-Za-z0-9]', key))
            if isinstance(ori_dict[key], dict):
                _, s, v = self.eliminateLevels(ori_dict[key], pre + key_m)
                sum += s
                valid += v
            elif isinstance(ori_dict[key], list):
                for ind,item in enumerate(ori_dict[key]):
                    _, s, v = self.eliminateLevels(item, pre + key_m + str(self.dec2alpha(ind)))
                    sum += s
                    valid += v
            elif not isinstance(ori_dict[key], bool) and isinstance(ori_dict[key], (int, str, float)):
                sum += 1
                temp = str(ori_dict[key])
                if len(''.join(re.findall(r'[A-Za-z0-9]', temp))) > minlen and temp[0] != '{':
                    # conduct embedding
                    ori_dict[key] = self.encoder(pre + key_m,ori_dict[key])
                    valid += 1

        return ori_dict, sum, valid
    
    
    
    def run(self, JSON):
        self.log.write("-----------------------------Embedding---------------------------------------")


        block, sum, valid = self.eliminateLevels(JSON, "")
        # self.log.write(json.dumps(modified_json))
        self.log.write("Sum of KEYS: " + str(sum) + ". Sum of Valid: " + str(valid))
    
        # block = self.encoder(f_bytes, modified_json, blocksize,  c, delta)
        json_str = json.dumps(block)
        with open('target.txt', 'w') as rf:
            rf.writelines(json_str)
        self.log.write('-----------------Embedding was conducted successfully...--------------------')

        return block


if __name__ == '__main__':
    pass
    # run(fn="text.txt", blocksize=1, seed=1, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA, numpacks=20)

