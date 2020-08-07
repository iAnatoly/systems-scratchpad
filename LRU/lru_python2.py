from collections import OrderedDict

class LRUCache:

    # @param capacity, an integer
    def __init__(self, capacity):
        self.capacity = capacity
        self.storage = OrderedDict()

    # @return an integer
    def get(self, key):
        if key not in self.storage:
            return -1
        value = self.storage[key]
        # it would be easy in python 3.2+ :
        # self.storage.move_to_end(key)
        # but no, we are stuck with dead language instead
        del self.storage[key]
        self.storage[key] = value
        return value


    # @param key, an integer
    # @param value, an integer
    # @return nothing
    def set(self, key, value):
        ##
        # damn you python2, this is the only way to force the update
        if key in self.storage:
            del self.storage[key]
            
        self.storage[key] = value
            
        if len(self.storage) > self.capacity:
            oldest = next(iter(self.storage))
            del self.storage[oldest]
