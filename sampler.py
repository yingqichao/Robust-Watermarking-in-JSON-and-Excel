"""Implementation of a sampler for the Robust Soliton Distribution.

This is the distribution on the `degree` of blocks encoded in the 
Luby Transform code. Blocks of data transmitted are generated by
sampling degree `d` from the Robust Soliton Distrubution, then
sampling `d` blocks uniformly from the sequence of blocks in the
file to be transmitted. These are XOR'ed together, and the result
is transmitted. 

Critically, the state of the PRNG when the degree of a block was 
sampled is transmitted with the block as metadata, so the 
receiver can reconstruct the sampling of source blocks given the
same PRNG parameters below.
"""
from math import log, floor, sqrt

DEFAULT_C = 0.1
DEFAULT_DELTA = 0.5

# Parameters for Pseudorandom Number Generator
PRNG_A = 16807
PRNG_M = (1 << 31) - 1
PRNG_MAX_RAND = PRNG_M - 1

def gen_tau(S, K, delta):
    """The Robust part of the RSD, we precompute an
    array for speed
    """
    pivot = floor(K/S)
    return [S/K * 1/d for d in range(1, pivot)] \
            + [S/K * log(S/delta)] \
            + [0 for d in range(pivot, K)] 

def gen_rho(K):
    """The Ideal Soliton Distribution, we precompute
    an array for speed
    """
    return [1/K] + [1/(d*(d-1)) for d in range(2, K+1)]

def gen_mu(K, delta, c):
    """The Robust Soliton Distribution on the degree of 
    transmitted blocks
    """

    S = c * log(K/delta) * sqrt(K) 
    tau = gen_tau(S, K, delta)
    rho = gen_rho(K)
    normalizer = sum(rho) + sum(tau)
    return [(rho[d] + tau[d])/normalizer for d in range(K)]

def gen_rsd_cdf(K, delta, c):
    """The CDF of the RSD on block degree, precomputed for
    sampling speed"""

    mu = gen_mu(K, delta, c)
    return [sum(mu[:d+1]) for d in range(K)]


class PRNG(object):
    """A Pseudorandom Number Generator that yields samples
    from the set of source blocks using the RSD degree
    distribution described above.
    """

    def __init__(self, params):
        """Provide RSD parameters on construction
        """

        self.state = None  # Seed is set by interfacing code using set_seed
        K, delta, c = params
        self.K = K
        self.cdf = gen_rsd_cdf(K, delta, c)

    def get_next(self):
        """Executes the next iteration of the PRNG
        evolution process, and returns the result
        """

        self.state = PRNG_A * self.state % PRNG_M
        return self.state

    def _sample_d(self):
        """Samples degree given the precomputed
        distributions above and the linear PRNG output
        """

        p = self.get_next() / PRNG_MAX_RAND
        for ix, v in enumerate(self.cdf):
            if v > p:
                return ix + 1
        return ix + 1

    def set_seed(self, seed):
        """Reset the state of the PRNG to the 
        given seed
        """

        self.state = seed

    
    def get_src_blocks(self, seed=None):
        """Returns the indices of a set of `d` source blocks
        sampled from indices i = 1, ..., K-1 uniformly, where
        `d` is sampled from the RSD described above.
        """

        if seed:
            self.state = seed

        blockseed = self.state
        d = self._sample_d() #Use Pseudo Random 1st
        have = 0
        nums = set()
        while have < d:
            num = self.get_next() % self.K #Use Pseudo Random 2nd
            if num not in nums:
                nums.add(num)
                have += 1
        return blockseed, d, nums

