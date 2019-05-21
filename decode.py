import io
import hamming
from collections import defaultdict

from math import ceil
import sampler
import re
from struct import unpack
import Util


# Check node in graph
class CheckNode(object):

    def __init__(self, src_nodes, check):
        self.check = check
        self.src_nodes = src_nodes


class BlockGraph(object):
    """Graph on which we run Belief Propagation to resolve
    source node data
    """

    def __init__(self, num_blocks):
        self.checks = defaultdict(list)
        self.num_blocks = num_blocks
        self.eliminated = {}

    def add_block(self, nodes, data):
        """Adds a new check node and edges between that node and all
        source nodes it connects, resolving all message passes that
        become possible as a result.
        """

        # We can eliminate this source node
        if len(nodes) == 1:
            to_eliminate = list(self.eliminate(next(iter(nodes)), data))

            # Recursively eliminate all nodes that can now be resolved
            while len(to_eliminate):
                other, check = to_eliminate.pop()
                to_eliminate.extend(self.eliminate(other, check))
        else:

            # Pass messages from already-resolved source nodes
            for node in list(nodes):
                if node in self.eliminated:
                    nodes.remove(node)
                    data ^= self.eliminated[node]

            # Resolve if we are left with a single non-resolved source node
            if len(nodes) == 1:
                return self.add_block(nodes, data)
            else:

                # Add edges for all remaining nodes to this check
                check = CheckNode(nodes, data)
                for node in nodes:
                    self.checks[node].append(check)

        # Are we done yet?
        return len(self.eliminated) >= self.num_blocks

    def eliminate(self, node, data):
        #Resolves a source node, passing the message to all associated checks


        # Cache resolved value
        self.eliminated[node] = data
        others = self.checks[node]
        del self.checks[node]

        # Pass messages to all associated checks
        for check in others:
            check.check ^= data
            check.src_nodes.remove(node)

            # Yield all nodes that can now be resolved
            if len(check.src_nodes) == 1:
                yield (next(iter(check.src_nodes)), check.check)


class LtDecoder(object):

    def __init__(self, log, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA):
        self.received_packs = 0
        self.c = c
        self.delta = delta
        self.K = 0
        self.filesize = 0
        self.blocksize = 0
        self.log = log
        self.block_graph = None
        self.prng = None
        self.initialized = False

    def is_done(self):
        return self.done

    def consume_block(self, filesize, key, lt_block, blocksize=1):
        # filesize, blocksize, blockseed, block = lt_block.split(",")
        # filesize, blocksize, blockseed, block = int(filesize), int(blocksize), int(blockseed), int(block)
        blockseed = Util.BKDRHash(key)

        # block = int(lt_block)
        # first time around, init things
        if not self.initialized:
            self.filesize = filesize
            self.blocksize = blocksize
            self.K = ceil(filesize / blocksize)
            self.block_graph = BlockGraph(self.K)
            self.prng = sampler.PRNG(params=(self.K, self.delta, self.c))
            self.initialized = True

        self.prng.set_seed(blockseed)
        # Run PRNG with given seed to figure out which blocks were XORed to make received data
        _, _, src_blocks = self.prng.get_src_blocks()# or seed=blockseed
        block,verify = self.extract(lt_block, self.prng)

        #check if the code is legal according to CRC
        if hamming.crc_check(verify):
        # If BP is done, stop
            print("Valid Package.")
            self.done = self._handle_block(src_blocks, block)
        else:
            print("Invalid Package.Skip...")
        return self.done

    def extract(self, lt_block, prng, strlen=7):
        extracted, ori_block, verify = 0, lt_block, ''
        if isinstance(lt_block, int):
            lt_block = str(lt_block)[1:]
        elif isinstance(lt_block, float):
            lt_block = str(lt_block)[1:]
            lt_block = lt_block.replace(".", "")

        s1, Set, ind = list(lt_block), set(), 0
        while ind < strlen:
            num = prng.get_next() % len(lt_block)
            if ind == 0:
                buff = num
            if num not in Set:
                Set.add(num)
                if ind < 5:
                    extracted *= 2
                    extracted += (ord(s1[num]) % 2)# * pow(2, ind)
                verify += str(ord(s1[num]) % 2)
                ind += 1

        print("Debug Extract: " + str(extracted) + " " + str(buff) + " " + str(ori_block))
        return extracted,verify

    def bytes_dump(self):
        buffer = io.BytesIO()
        self.stream_dump(buffer)
        return buffer.getvalue()

    def stream_dump(self, out_stream):

        # Iterate through blocks, stopping before padding junk
        for ix, block_bytes in enumerate(map(lambda p: int.to_bytes(p[1], self.blocksize, 'big'),
                                             sorted(self.block_graph.eliminated.items(), key=lambda p: p[0]))):
            if ix < self.K - 1 or self.filesize % self.blocksize == 0:
                out_stream.write(block_bytes)
            else:
                out_stream.write(block_bytes[:self.filesize % self.blocksize])

    def _handle_block(self, src_blocks, block):
        # What to do with new block: add check and pass messages in graph

        return self.block_graph.add_block(src_blocks, block)


class decode:
    def __init__(self,log=None):
        self.log = log

    def _read_header(self,stream):
        """Read block header from network
        """
        header_bytes = stream.read(12)
        return unpack('!III', header_bytes)

    def _read_block(self,blocksize, stream):
        """Read block data from network into integer type
        """
        blockdata = stream.read(blocksize)
        return int.from_bytes(blockdata, 'big')

    def read_blocks(self,stream):
        """Generate parsed blocks from input stream
        """
        while True:
            header = self._read_header(stream)
            block = self._read_block(header[1], stream)
            yield (header, block)

    def block_from_bytes(self,bts):
        return next(self.read_blocks(io.BytesIO(bts)))

    def decode(self, JSON, filesize, **kwargs):
        decoder = LtDecoder(self.log, **kwargs)

        for key in JSON:
            lt_block = JSON[key]

            decoder.consume_block(filesize=filesize, key=key, lt_block=lt_block, blocksize=1)
            decoder.received_packs += 1
            if decoder.is_done():
                print("Decoded Successfully...")
                break
            else:
                print("Need more Packs...Received: "+str(decoder.received_packs))

        return decoder.bytes_dump()


    def run(self,JSON, filesize, blocksize=1, seed=1, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA,log=None):
        """Reads from stream, applying the LT decoding algorithm
        to incoming encoded blocks until sufficiently many blocks
        have been received to reconstruct the entire file.



        """
        print("-----------------------------Extraction---------------------------------------")
        modified_json = {}
        modified_json, sum, valid = Util.eliminateLevels(modified_json, JSON, "")
        print(modified_json)
        print("Sum of KEYS: " + str(sum) + ". Sum of Valid: " + str(valid))

        payload = self.decode(modified_json, filesize)
        # with open('decoded.txt', 'w') as rf:
        #     rf.writelines(payload.decode('utf8'))
        res = [chr(ord('a')+i) for i in payload]
        print("     Payload: "+''.join(res))
        print('-----------------Extraction was conducted successfully...--------------------')

if __name__ == '__main__':
    pass
    # run(JSON, blocksize=1, seed=1, c=sampler.DEFAULT_C, delta=sampler.DEFAULT_DELTA)

