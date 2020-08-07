# based on https://techspot.zzzeek.org/2012/07/07/the-absolutely-simplest-consistent-hashing-example/
# ported to python3
import bisect
import hashlib 

class ConsistentHashRing:
    def __init__(self, replicas:int =100):
        self.replicas = replicas
        self._keys = []
        self._nodes = {}

    def _hash(self, key:str)->int:
        return int(hashlib.md5(key.encode("utf8")).hexdigest(), 16)

    def _repl_iterator(self, nodename):
        return (self._hash("%s:%s" % (nodename, i))
                for i in range(self.replicas))

    def __setitem__(self, nodename, node):
        for hash_ in self._repl_iterator(nodename):
            if hash_ in self._nodes:
                raise ValueError("Node name %r is "
                            "already present" % nodename)
            self._nodes[hash_] = node
            bisect.insort(self._keys, hash_)

    def __delitem__(self, nodename):
        for hash_ in self._repl_iterator(nodename):
            # will raise KeyError for nonexistent node name
            del self._nodes[hash_]
            index = bisect.bisect_left(self._keys, hash_)
            del self._keys[index]

    def __getitem__(self, key):
        """Return a node, given a key.

        The node replica with a hash value nearest
        but not less than that of the given
        name is returned.   If the hash of the
        given name is greater than the greatest
        hash, returns the lowest hashed node.

        """
        hash_ = self._hash(key)
        start = bisect.bisect(self._keys, hash_)
        if start == len(self._keys):
            start = 0
        return self._nodes[self._keys[start]]
