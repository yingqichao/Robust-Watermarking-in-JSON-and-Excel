import sys
from random import randint
from struct import pack

import sampler

def _split_file(f, blocksize):
    """Block file byte contents into blocksize chunks, padding last one if necessary
    """

    f_bytes = f.read()
    blocks = [int.from_bytes(f_bytes[i:i+blocksize].ljust(blocksize, b'0'), sys.byteorder)
            for i in range(0, len(f_bytes), blocksize)]
    return len(f_bytes), blocks


def encoder(f, blocksize, seed, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA):
    """Generates an infinite sequence of blocks to transmit
    to the receiver
    """

    # Seed Must be Provided!
    # if seed is None:
    #     seed = randint(0, 1 << 31 - 1)

    # get file blocks
    filesize, blocks = _split_file(f, blocksize)

    # init stream vars
    K = len(blocks)
    prng = sampler.PRNG(params=(K, delta, c))
    prng.set_seed(seed)

    # block generation loop
    while True:
        blockseed, d, ix_samples = prng.get_src_blocks()
        block_data = 0
        for ix in ix_samples:
            block_data ^= blocks[ix]

        # Generate blocks of XORed data in network byte order
        block = str(filesize)+','+str(blocksize)+','+str(blockseed)+','+str(block_data)+'\n' #int.to_bytes(block_data, blocksize, sys.byteorder))
        yield block#pack('!III%ss'%blocksize, *block)


def run(fn="text.txt", blocksize=1, seed=1, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA , numpacks=20):

    with open(fn, 'rb') as f:
        block = encoder(f, blocksize, seed, c, delta)
        with open('target.txt', 'w') as rf:
            for i in range(numpacks):
                buff = next(block)
                rf.writelines(buff)
                print(buff)
    print('Embedding was conducted successfully...')


if __name__ == '__main__':

    run(fn="text.txt", blocksize=1, seed=1, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA, numpacks=20)

