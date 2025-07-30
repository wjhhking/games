import sys

"""
This file provides a solution to the Frequency Cache problem described in lru_cache.md.
The implementation handles all phases of the problem, including:
1. Basic frequency counting with a heap.
2. Handling complex priority rules (frequency, lexicographical order).
3. Support for dynamic, user-defined priority rules.
4. Capacity limits and eviction of the lowest-priority item.
"""

# Default priority rule: Higher frequency is higher priority.
# For ties in frequency, larger key (lexicographically) is higher priority.
def default_priority_rule(item1, item2):
    """
    Returns True if item1 has higher priority than item2.
    """
    if item1.count != item2.count:
        return item1.count > item2.count
    return item1.key > item2.key

class Item:
    """A simple data class to hold the key and its count."""
    def __init__(self, key, count=0):
        self.key = key
        self.count = count

    def __repr__(self):
        return f"Item(key={self.key}, count={self.count})"

class PriorityHeap:
    """
    A custom heap implementation that supports O(log n) updates and removals.
    It uses a dictionary to keep track of the position of each key in the heap,
    which is crucial for efficient updates.
    """
    def __init__(self, priority_rule):
        self.heap = []
        self.positions = {}
        self.priority_rule = priority_rule

    def _swap(self, i, j):
        """Swaps two elements in the heap and updates their positions."""
        item1_key = self.heap[i].key
        item2_key = self.heap[j].key

        self.positions[item1_key], self.positions[item2_key] = j, i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _sift_up(self, i):
        """Moves an element up the heap to its correct position."""
        parent_idx = (i - 1) // 2
        while i > 0 and self.priority_rule(self.heap[i], self.heap[parent_idx]):
            self._swap(i, parent_idx)
            i = parent_idx
            parent_idx = (i - 1) // 2

    def _sift_down(self, i):
        """Moves an element down the heap to its correct position."""
        max_index = i
        left_child_idx = 2 * i + 1
        right_child_idx = 2 * i + 2

        if left_child_idx < len(self.heap) and self.priority_rule(self.heap[left_child_idx], self.heap[max_index]):
            max_index = left_child_idx

        if right_child_idx < len(self.heap) and self.priority_rule(self.heap[right_child_idx], self.heap[max_index]):
            max_index = right_child_idx

        if i != max_index:
            self._swap(i, max_index)
            self._sift_down(max_index)

    def push(self, item):
        """Adds a new item to the heap."""
        self.heap.append(item)
        self.positions[item.key] = len(self.heap) - 1
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        """Removes and returns the highest-priority item from the heap."""
        if not self.heap:
            return None

        root_item = self.heap[0]
        if len(self.heap) > 1:
            last_item = self.heap.pop()
            del self.positions[root_item.key]
            self.heap[0] = last_item
            self.positions[last_item.key] = 0
            self._sift_down(0)
        else:
            self.heap.pop()
            del self.positions[root_item.key]

        return root_item

    def update(self, key):
        """
        To be called when an item's priority might have changed.
        It finds the item and re-heapifies it.
        """
        if key not in self.positions:
            return
        idx = self.positions[key]
        # An item's priority only increases in this problem, so we only need to sift up.
        self._sift_up(idx)

    def remove(self, key):
        """Removes an item from the heap by its key in O(log n)."""
        if key not in self.positions:
            return None

        idx_to_remove = self.positions[key]

        self._swap(idx_to_remove, len(self.heap) - 1)

        item_removed = self.heap.pop()
        del self.positions[key]

        # If the removed item was not the last one, we need to fix the heap
        if idx_to_remove < len(self.heap):
            # We don't know if the swapped element should go up or down, so try both.
            self._sift_up(idx_to_remove)
            self._sift_down(idx_to_remove)

        return item_removed

    def peek(self):
        """Returns the highest-priority item without removing it."""
        return self.heap[0] if self.heap else None

    def find_lowest_priority_item(self):
        """
        Finds the item with the lowest priority.
        This is an O(n) operation. For a more performant solution
        for frequent evictions, a second min-heap would be required.
        """
        if not self.heap:
            return None

        # The lowest priority items in a max-heap are always at the leaf nodes.
        # We only need to check the second half of the array.
        start_index = len(self.heap) // 2
        if start_index == 0 and len(self.heap) > 0:
             return self.heap[0]
        if start_index >= len(self.heap):
             return None

        lowest_item = self.heap[start_index]
        for i in range(start_index + 1, len(self.heap)):
            if self.priority_rule(lowest_item, self.heap[i]):
                lowest_item = self.heap[i]
        return lowest_item

    def set_priority_rule(self, new_rule):
        """Updates the priority rule and rebuilds the entire heap in O(n)."""
        self.priority_rule = new_rule
        # Rebuild the heap from the bottom up.
        for i in range((len(self.heap) // 2) - 1, -1, -1):
            self._sift_down(i)

    def __len__(self):
        return len(self.heap)

class FrequencyCache:
    """
    A frequency-based cache that supports dynamic priority rules and a capacity limit.
    """
    def __init__(self, capacity=sys.maxsize):
        self.capacity = capacity
        self.items = {}  # key -> Item(key, count)
        # The default rule is used for initialization.
        self.priority_rule = default_priority_rule
        self.heap = PriorityHeap(self.priority_rule)

    def addKey(self, key: str) -> str:
        """
        Adds a key to the cache or increments its frequency.
        If the cache is full, it evicts the lowest-priority item.
        Returns the key of the evicted item, or an empty string if no item was evicted.
        """
        evicted_key = ""
        if key not in self.items:
            if len(self.heap) >= self.capacity:
                item_to_evict = self.heap.find_lowest_priority_item()
                if item_to_evict:
                    self.heap.remove(item_to_evict.key)
                    del self.items[item_to_evict.key]
                    evicted_key = item_to_evict.key

            new_item = Item(key, 1)
            self.items[key] = new_item
            self.heap.push(new_item)
        else:
            item = self.items[key]
            item.count += 1
            self.heap.update(key)

        return evicted_key

    def getCountForKey(self, key: str) -> int:
        """Returns the frequency count for a given key."""
        return self.items[key].count if key in self.items else 0

    def getMaxFrequencyKey(self) -> str:
        """Returns the key with the highest priority."""
        item = self.heap.peek()
        return item.key if item else ""

    def setPriorityRule(self, rule_func):
        """
        Sets a new priority rule for the cache and rebuilds the heap.
        The rule_func(item1, item2) should return True if item1 has higher priority.
        """
        self.priority_rule = rule_func
        self.heap.set_priority_rule(self.priority_rule)

# --- Example Usage and Tests ---

# Phase 1: Basic functionality
print("--- Phase 1: Basic ---")
cache = FrequencyCache()
cache.addKey("a")
cache.addKey("b")
# Tie in count, "b" > "a" lexicographically
assert cache.getMaxFrequencyKey() == "b"
cache.addKey("a")  # a count becomes 2
assert cache.getMaxFrequencyKey() == "a"
assert cache.getCountForKey("a") == 2
assert cache.getCountForKey("b") == 1
assert cache.getCountForKey("c") == 0
print("Phase 1 Passed!")

# Phase 2 & 3: Dynamic priority rule
print("\n--- Phase 2 & 3: Dynamic Priority ---")
cache = FrequencyCache()
cache.addKey("a")
cache.addKey("b")
# Default rule: b > a
assert cache.getMaxFrequencyKey() == "b"

# New rule: frequency desc, then key asc
def new_rule(item1, item2):
    if item1.count != item2.count:
        return item1.count > item2.count
    return item1.key < item2.key # Note the '<'

cache.setPriorityRule(new_rule)
# Tie in count, 'a' < 'b' so 'a' has higher priority now
assert cache.getMaxFrequencyKey() == "a"
cache.addKey("b") # b count becomes 2
assert cache.getMaxFrequencyKey() == "b"
print("Phase 2 & 3 Passed!")

# Phase 4: Capacity limit
print("\n--- Phase 4: Capacity Limit ---")
# Use the new rule (key asc for ties)
cache = FrequencyCache(capacity=2)
cache.setPriorityRule(new_rule)
cache.addKey("a") # a:1
cache.addKey("b") # b:1, a:1 -> max is 'a' due to rule
assert cache.getMaxFrequencyKey() == "a"
# Add 'c', capacity is full.
# Eviction check: 'a' and 'b' have count 1. 'b' has lower priority (b > a).
# So 'b' should be evicted.
evicted = cache.addKey("c") # c:1. Evicts 'b'.
assert evicted == "b"
assert cache.getCountForKey("b") == 0
assert "b" not in cache.items
# State: {a:1, c:1}. Max is 'a' (a < c).
assert cache.getMaxFrequencyKey() == "a"
cache.addKey("c") # State: {a:1, c:2}. Max is 'c'.
assert cache.getMaxFrequencyKey() == "c"
print("Phase 4 Passed!")

print("\n--- Additional Tests ---")
c = FrequencyCache()
assert c.getMaxFrequencyKey() == ""
c.addKey(1)
assert c.getMaxFrequencyKey() == 1
c.addKey(2)
# Default rule: 2 > 1
assert c.getMaxFrequencyKey() == 2
c.addKey(2)
assert c.getMaxFrequencyKey() == 2
c.addKey(3)
# State {1:1, 2:2, 3:1}. Max is 2.
assert c.getMaxFrequencyKey() == 2
c.addKey(3)
# State {1:1, 2:2, 3:2}. Max is 3 (3 > 2)
assert c.getMaxFrequencyKey() == 3
c.addKey(3)
# State {1:1, 2:2, 3:3}. Max is 3.
assert c.getMaxFrequencyKey() == 3
c.addKey(1)
c.addKey(1)
# State {1:3, 2:2, 3:3}. Max is 3 (tie, 3 > 1)
assert c.getMaxFrequencyKey() == 3
c.addKey(1)
# State {1:4, 2:2, 3:3}. Max is 1.
assert c.getMaxFrequencyKey() == 1
assert c.getCountForKey(1) == 4
assert c.getCountForKey(2) == 2
assert c.getCountForKey(3) == 3
print("Additional Tests Passed!")
