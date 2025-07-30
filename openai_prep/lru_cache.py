
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


# --- New, Concise Implementation as per your request ---

def default_priority_rule(item1, item2):
    """Default Rule: Returns True if item1 has HIGHER priority than item2."""
    if item1.count != item2.count:
        return item1.count > item2.count
    return item1.key > item2.key

class Item:
    """
    An item in the cache. Its comparison logic is controlled by a
    swappable class-level function `priority_rule`.
    """
    # This class-level attribute will be used for all comparisons.
    priority_rule = default_priority_rule

    def __init__(self, key, count=1):
        self.key = key
        self.count = count

    def __lt__(self, other):
        """
        Determines priority for the min-heap.
        To simulate a max-heap, an item `A` is "less than" item `B` if `A` has
        a higher priority. This ensures the highest-priority item is the
        "smallest" and thus stays at the top of the min-heap.
        """
        return self.priority_rule(self, other)

    def __repr__(self):
        return f"Item(key={self.key}, count={self.count})"

class FrequencyCacheV2:
    """
    A concise implementation using Python's `heapq` library.
    - Priority changes are handled by swapping the comparator on the Item class.
    - Updates and rule changes require an O(n) `heapify` operation.
    """
    def __init__(self):
        self.items = {}  # Maps key -> Item object for quick access
        self.heap = []   # The heap, storing Item objects

    def addKey(self, key: str):
        if key not in self.items:
            item = Item(key, 1)
            self.items[key] = item
            heapq.heappush(self.heap, item)
        else:
            item = self.items[key]
            item.count += 1
            # This is concise, but O(n). Required to fix the heap after mutation.
            heapq.heapify(self.heap)

    def getCountForKey(self, key: str) -> int:
        return self.items[key].count if key in self.items else 0

    def getMaxFrequencyKey(self) -> str:
        """Returns the highest-priority key. O(1)"""
        if not self.heap:
            return ""
        return self.heap[0].key

    def setPriorityRule(self, rule_func):
        """Swaps the priority rule and rebuilds the heap. O(n)"""
        Item.priority_rule = rule_func
        heapq.heapify(self.heap)

# --- Tests for the new implementation ---
print("--- Testing FrequencyCacheV2 ---")

# Test 1: Basic functionality with default priority
print("\n--- Test 1: Default Priority ---")
cache = FrequencyCacheV2()
cache.addKey("a")
cache.addKey("b")
# Default rule: count desc, key desc. With counts equal, 'b' > 'a'.
assert cache.getMaxFrequencyKey() == "b"
cache.addKey("a")  # a:2, b:1
assert cache.getMaxFrequencyKey() == "a"
assert cache.getCountForKey("a") == 2
print("Test 1 Passed!")

# Test 2: Changing the priority rule
print("\n--- Test 2: Dynamic Priority ---")
cache = FrequencyCacheV2()
cache.addKey("a") # a:1
cache.addKey("b") # b:1
assert cache.getMaxFrequencyKey() == "b" # Default rule

# New rule: count desc, but key ASC
def new_rule(item1, item2):
    if item1.count != item2.count:
        return item1.count > item2.count
    return item1.key < item2.key # Note: ascending key order

cache.setPriorityRule(new_rule)
# Counts are tied, 'a' < 'b', so 'a' now has higher priority.
assert cache.getMaxFrequencyKey() == "a"
cache.addKey("b") # b:2, a:1
assert cache.getMaxFrequencyKey() == "b"
print("Test 2 Passed!")

# Reset to default rule for other tests
Item.priority_rule = default_priority_rule

print("\n--- Additional Tests ---")
c = FrequencyCacheV2()
assert c.getMaxFrequencyKey() == ""
c.addKey(1)
assert c.getMaxFrequencyKey() == 1
c.addKey(2)
assert c.getMaxFrequencyKey() == 2
c.addKey(2)
assert c.getMaxFrequencyKey() == 2
c.addKey(3)
assert c.getMaxFrequencyKey() == 2
c.addKey(3)
assert c.getMaxFrequencyKey() == 3
c.addKey(3)
assert c.getMaxFrequencyKey() == 3
c.addKey(1)
c.addKey(1)
assert c.getMaxFrequencyKey() == 3
c.addKey(1)
assert c.getMaxFrequencyKey() == 1
assert c.getCountForKey(1) == 4
assert c.getCountForKey(2) == 2
assert c.getCountForKey(3) == 3
print("All tests passed!")
