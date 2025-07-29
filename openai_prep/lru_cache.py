
import heapq


class FrequencyCache:

    def __init(self):
        self.count = {} # key -> count
        self.heap = [] # max_heap (-count， key)

    def addKey(self, key: str):
        self.count[key] = self.count.get(key,0)
        heapq.heappush(self.heap, (-self.count))

    def getCountForKey(self, key):
        return self.count.get(key, 0)

    def getMaxFrequencyKey(self) -> str:
        return self.heap[0][1]