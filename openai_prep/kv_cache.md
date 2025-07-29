# Time-Based Key-Value Store

Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

## Problem Statement

Implement the `TimeMap` class:

-   `TimeMap()` Initializes the object.
-   `set(key: str, value: str, timestamp: int)` Stores the key `key` with the value `value` at the given time `timestamp`.
-   `get(key: str, timestamp: int) -> str` Returns a value.
    -   If there are multiple values for a key, it should return the value associated with the largest `timestamp` that is less than or equal to the given `timestamp`.
    -   If there are no values for the key, or if all timestamps for the key are greater than the given `timestamp`, it should return `""`.

### Example

```
timeMap = TimeMap()
timeMap.set("foo", "bar", 1)
timeMap.get("foo", 1) # returns "bar"
timeMap.get("foo", 3) # returns "bar"
timeMap.set("foo", "bar2", 4)
timeMap.get("foo", 4) # returns "bar2"
timeMap.get("foo", 5) # returns "bar2"
```

This problem is a variation of LeetCode 981: Time Based Key-Value Store. The following sections also discuss common follow-up questions related to concurrency, out-of-memory issues, and handling future timestamps, based on collected interview experiences.

---

## Follow-up Questions

### 1. Concurrency and Thread-Safety

**Question:** How would you make this data structure thread-safe? What if multiple threads are calling `set` and `get` concurrently?

**Discussion:**
Without synchronization, concurrent access can lead to race conditions, where the data structure becomes corrupted or `get` operations return incorrect results.

-   **Approach 1: Single Global Lock (Coarse-Grained)**
    The simplest solution is to wrap every `set` and `get` call in a single global lock (e.g., `threading.Lock`). This is easy to implement but creates a major performance bottleneck, as only one thread can access the map at a time, regardless of the key.

-   **Approach 2: Read-Write Lock**
    If read operations (`get`) are much more frequent than write operations (`set`), a `ReadWriteLock` can improve performance. It allows multiple readers to access the data concurrently, but a writer must obtain an exclusive lock.

-   **Approach 3: Sharding with Fine-Grained Locks (Recommended)**
    To maximize concurrency, we can partition the key space into a fixed number of "shards". Each shard has its own lock, protecting only the subset of keys that map to it. Operations on keys in different shards can run in parallel. This is similar to how Java's `ConcurrentHashMap` works.

-   **Alternative: Per-Key Locks.** An even more granular approach is to have one lock per key. While this provides the absolute best concurrency (operations on different keys never block each other), it comes at a significant cost. It requires storing a lock object for every unique key, which can lead to massive memory overhead in a system with millions of keys. Sharding offers a practical compromise, providing excellent concurrency while keeping the number of lock objects fixed and manageable.

### 2. Out-of-Memory (OOM) Issues

**Question:** What if the dataset becomes too large to fit in memory?

**Discussion:**
This is a system design question. The key idea is to move from a purely in-memory store to a tiered storage system.

-   **Tiered Storage:** Keep a cache of the most relevant data in memory (RAM) and spill the rest to a persistent, slower storage like an SSD or HDD.

-   **Eviction Policy:** An eviction policy is needed to decide what to move from memory to disk. Common choices include:
    -   **LRU (Least Recently Used):** Evict the key-value pairs that haven't been accessed for the longest time.
    -   **LFU (Least Frequently Used):** Evict data that is accessed least often.
    -   **Time-based Eviction:** Evict old versions of values (e.g., older than 30 days).

-   **On-Disk Storage Format:**
    -   **Append-Only Log:** Simple, fast for writes, but slow for reads.
    -   **SSTables (Sorted String Tables):** Used by systems like Bigtable and RocksDB. Data is stored in sorted, immutable files, allowing for efficient lookups.

### 3. Handling Future Timestamps

**Question:** How should `get(key, timestamp)` behave if the timestamp is in the future? For example, at T=10, a client calls `get("foo", 20)`. Then at T=15, another client calls `set("foo", "bar", 15)`. The first `get` call should now return "bar".

**Discussion:**
This transforms `get` from a simple lookup into a potentially blocking or asynchronous operation.

-   **Approach 1: Define as Invalid (Simple & Practical)**
    Return the latest value available *now*. This is the most common and predictable behavior.

-   **Approach 2: Busy-Wait or Sleep (Inefficient)**
    `time.sleep(future_timestamp - time.time())`. This is highly inefficient as it ties up a worker thread.

-   **Approach 3: Wait with Condition Variables (Recommended for this scenario)**
    Use `threading.Condition` variables. `get` waits on a condition specific to the key, and `set` notifies waiters. This avoids burning CPU cycles.

-   **Approach 4: Asynchronous Callbacks or Futures (Complex)**
    `get` could immediately return a "future" or "promise" object. The client can check this object later for the result. This increases complexity.
