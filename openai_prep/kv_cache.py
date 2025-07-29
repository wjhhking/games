import bisect
from collections import defaultdict
import threading
import time

# ======================================================================================
# Section 1: Basic Single-Threaded Solution
# ======================================================================================

class TimeMap:
    """
    A time-based key-value store. This implementation is for a single-threaded
    environment. It uses a dictionary to store keys and a sorted list of
    (timestamp, value) pairs for each key.
    """
    def __init__(self):
        """
        Initializes the data structure.
        """
        self.data = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        """
        Stores a value for a key at a specific timestamp.
        The list of values for each key is kept sorted by timestamp,
        allowing for efficient retrieval.
        """
        # Since timestamps are expected to be always increasing, we can just append.
        # If timestamps can be out of order, we would use:
        # bisect.insort(self.data[key], (timestamp, value))
        self.data[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        """
        Retrieves the value for a key at a specific timestamp.
        It uses binary search to find the value with the largest timestamp
        less than or equal to the given timestamp.
        """
        if key not in self.data:
            return ""

        values = self.data[key]

        # Binary search to find the insertion point for the given timestamp.
        # `bisect_right` finds an insertion point which comes after (to the right of)
        # any existing entries of `timestamp`.
        # We create a tuple (timestamp, "{") where "{" is a character that is
        # larger than any character in a typical string value, ensuring that
        # if a tuple with the exact timestamp exists, our needle is considered larger.
        # This gives us the index of the first element strictly greater than the target timestamp.
        i = bisect.bisect_right(values, (timestamp, "{"))

        if i == 0:
            return ""

        # The desired value is at the index just before the insertion point.
        return values[i - 1][1]


# ======================================================================================
# Section 2: Thread-Safe Solution for Concurrency
# ======================================================================================

class ReadWriteLockOld:
    """
    A lock object that allows many simultaneous readers, but only one writer.
    A writer blocks all readers. A reader blocks a writer.
    """
    def __init__(self):
        self.read_ready = threading.Condition(threading.Lock())
        self.readers = 0

    def acquire_read(self):
        with self.read_ready:
            self.readers += 1

    def release_read(self):
        with self.read_ready:
            self.readers -= 1
            if self.readers == 0:
                self.read_ready.notify_all()

    def acquire_write(self):
        self.read_ready.acquire()
        while self.readers > 0:
            # Wait for all readers to finish
            self.read_ready.wait()

    def release_write(self):
        self.read_ready.release()


class ReadWriteLock:
    def __init__(self):
        self._lock = threading.RLock()
        self._readers = 0
        self._writers = 0
        self._condition = threading.Condition(self._lock)

    def acquire_read(self):
        with self._lock:
            while self._writers > 0:
                self._condition.wait()
            self._readers += 1

    def release_read(self):
        with self._lock:
            self._readers -= 1
            if self._readers == 0:
                self._condition.notify_all()

    def acquire_write(self):
        with self._lock:
            while self._readers > 0 or self._writers > 0:
                self._condition.wait()
            self._writers = 1

    def release_write(self):
        with self._lock:
            self._writers = 0
            self._condition.notify_all()

rwlock = ReadWriteLock()
data = ()

def reader(name):
    rwlock.acquire_read()
    try:
        print('read data')
    finally:
        rwlock.release_read()

def writer(value):
    rwlock.acquire_write()
    try:
        data.append(value)
    finally:
        rwlock.release_write()


class ShardedTimeMap:
    """
    A thread-safe, sharded implementation of the TimeMap.
    It distributes keys across a fixed number of shards, each with its own
    ReadWriteLock, to allow for high concurrency.
    """
    class _Shard:
        def __init__(self):
            self.data = defaultdict(list)
            self.lock = ReadWriteLock()

        def set(self, key: str, value: str, timestamp: int):
            self.lock.acquire_write()
            try:
                # bisect.insort is needed here if timestamps are not guaranteed to be sequential per key
                self.data[key].append((timestamp, value))
            finally:
                self.lock.release_write()

        def get(self, key: str, timestamp: int) -> str:
            self.lock.acquire_read()
            try:
                if key not in self.data:
                    return ""

                values = self.data[key]
                i = bisect.bisect_right(values, (timestamp, "{"))
                if i == 0:
                    return ""
                return values[i - 1][1]
            finally:
                self.lock.release_read()

    def __init__(self, num_shards: int = 16):
        """
        Initializes the sharded map.

        Args:
            num_shards: The number of shards to partition the key space into.
                        A higher number can increase concurrency but also memory overhead.
                        Should be a power of 2 for efficient hashing.
        """
        self.shards = [self._Shard() for _ in range(num_shards)]
        self.num_shards = num_shards

    def _get_shard(self, key: str) -> '_Shard':
        """
        Determines which shard a key belongs to using its hash.
        """
        return self.shards[hash(key) % self.num_shards]

    def set(self, key: str, value: str, timestamp: int) -> None:
        self._get_shard(key).set(key, value, timestamp)

    def get(self, key: str, timestamp: int) -> str:
        return self._get_shard(key).get(key, timestamp)