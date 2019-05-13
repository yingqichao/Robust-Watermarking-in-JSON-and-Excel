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


def encoder(f, blocksize, seed=None, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA):
    """Generates an infinite sequence of blocks to transmit
    to the receiver
    """

    # Generate seed if not provided
    if seed is None:
        seed = randint(0, 1 << 31 - 1)

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


def run(fn, blocksize, seed, c, delta,numpacks=20):
    """Run the encoder until the channel is broken, signalling that the
    receiver has successfully reconstructed the file
    """

    with open(fn, 'rb') as f:
        block = encoder(f, blocksize, seed, c, delta)
        with open('target.txt', 'w') as rf:
            for i in range(numpacks):
                buff = next(block)
                rf.writelines(buff)
                sys.stdout.buffer.write(buff)
    print('Embedding was conducted successfully...')


if __name__ == '__main__':
    # parser = argparse.ArgumentParser("encoder")
    # parser.add_argument('file', help='the source file to encode')
    # parser.add_argument('blocksize', metavar='block-size',
    #                     type=int,
    #                     help='the size of each encoded block, in bytes')
    # parser.add_argument('seed', type=int,
    #                     nargs="?",
    #                     default=2067261,
    #                     help='the initial seed for the random number generator')
    # parser.add_argument('c', type=float,
    #                     nargs="?",
    #                     default=sampler.DEFAULT_C,
    #                     help='degree sampling distribution tuning parameter')
    # parser.add_argument('delta', type=float,
    #                     nargs="?",
    #                     default=sampler.DEFAULT_DELTA,
    #                     help='degree sampling distribution tuning parameter')
    # args = parser.parse_args()
    #
    # if not os.path.exists(args.file):
    #     print("File %s doesn't exist. Try again." % args.file, file=sys.stderr)
    #     sys.exit(1)

    # file, blocksize, seed, c, delta

    # try:
    run("text.txt", blocksize=1, seed=1, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA,numpacks=20)
    # except (GeneratorExit, IOError):
    #     print("Decoder has cut off transmission. Fountain closed.", file=sys.stderr)
    #     sys.stdout.write = lambda s: None
    #     sys.stdout.flush = lambda: None
    #     sys.exit(0)
