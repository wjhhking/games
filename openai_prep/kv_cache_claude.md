# TimeMap 完整面试题与解答

## 主题：Time-Based Key-Value Store (LeetCode 981)

### 基础题目
实现一个基于时间的键值存储系统 TimeMap，支持：
- `set(key, value, timestamp)`: 存储键值对和时间戳
- `get(key, timestamp)`: 返回指定时间戳或之前最新的值

**基础实现：**
```python
import bisect

class TimeMap:
    def __init__(self):
        self.data = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.data:
            self.data[key] = []
        self.data[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.data:
            return ""

        timestamps = [item[0] for item in self.data[key]]
        idx = bisect.bisect_right(timestamps, timestamp)

        return "" if idx == 0 else self.data[key][idx - 1][1]
```

---

## Follow-up 1: 多线程并发安全

**问题：** 如何处理多线程并发访问？多个线程同时调用 `set` 和 `get` 会有什么问题？

### 问题分析：

**并发访问的风险：**
1. **数据竞争**：多个线程同时修改 `self.data[key]` 列表，可能导致数据丢失或列表损坏
2. **读写不一致**：线程A在读取时，线程B正在写入，可能读到不完整的数据
3. **内存可见性**：由于CPU缓存，一个线程的写入可能对其他线程不立即可见

**具体场景：**
```python
# 危险场景1：同时 set 同一个 key
Thread1: self.data[key].append((1, "value1"))  # 正在执行
Thread2: self.data[key].append((2, "value2"))  # 同时执行 -> 列表可能损坏

# 危险场景2：读写并发
Thread1: bisect.bisect_right(timestamps, target)  # 正在二分查找
Thread2: self.data[key].append((3, "value3"))     # 同时修改列表 -> 查找结果错误
```

### 解决方案对比：

#### 方案1：全局读写锁 (简单场景)
```python
import threading
from collections import defaultdict

class ThreadSafeTimeMap:
    def __init__(self):
        self.data = {}
        self.lock = threading.RLock()

    def set(self, key: str, value: str, timestamp: int) -> None:
        with self.lock:
            if key not in self.data:
                self.data[key] = []
            self.data[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        with self.lock:
            # ... 查找逻辑
```

#### 方案2：Per-Key 读写锁 (推荐)
```python
class ReadWriteLock:
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
            self.read_ready.wait()

    def release_write(self):
        self.read_ready.release()

class TimeMapPerKey:
    def __init__(self):
        self.data = {}
        self.locks = defaultdict(ReadWriteLock)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.locks[key].acquire_write()
        try:
            if key not in self.data:
                self.data[key] = []
            self.data[key].append((timestamp, value))
        finally:
            self.locks[key].release_write()

    def get(self, key: str, timestamp: int) -> str:
        self.locks[key].acquire_read()
        try:
            # ... 查找逻辑
        finally:
            self.locks[key].release_read()
```

#### 方案3：分片锁 (高并发场景)
```python
class TimeMapSharded:
    def __init__(self, num_shards=16):
        self.num_shards = num_shards
        self.shards = [TimeMapShard() for _ in range(num_shards)]

    def get_shard(self, key):
        return self.shards[hash(key) % self.num_shards]

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.get_shard(key).set(key, value, timestamp)

    def get(self, key: str, timestamp: int) -> str:
        return self.get_shard(key).get(key, timestamp)
```

---

## Follow-up 2: 内存溢出 (OOM) 处理

**问题：** 如果数据量太大导致内存不足怎么办？

### 问题分析：

**内存溢出的原因：**
1. **数据量增长**：每个 key 的历史版本不断积累，永不删除
2. **热点 key**：某些 key 被频繁更新，产生大量时间戳版本
3. **长尾数据**：很多旧的时间戳数据很少被访问，但仍占用内存

**内存使用估算：**
```
假设：
- 1000万个 key
- 每个 key 平均 100 个版本
- 每个版本 100 字节 (timestamp + value)
总内存 ≈ 10M × 100 × 100B = 100GB
```

### 解决方案：

#### 1. LRU 淘汰策略
```python
from collections import OrderedDict

class TimeMapWithLRU:
    def __init__(self, max_keys=1000):
        self.data = {}
        self.access_order = OrderedDict()
        self.max_keys = max_keys

    def _evict_if_needed(self):
        while len(self.access_order) > self.max_keys:
            oldest_key = next(iter(self.access_order))
            del self.data[oldest_key]
            del self.access_order[oldest_key]

    def get(self, key: str, timestamp: int) -> str:
        if key in self.access_order:
            self.access_order.move_to_end(key)  # 更新访问顺序
        # ... 查找逻辑
```

#### 2. 时间窗口淘汰
```python
import time

class TimeMapWithTTL:
    def __init__(self, ttl_seconds=3600):
        self.data = {}
        self.ttl = ttl_seconds

    def _cleanup_expired(self, key):
        if key not in self.data:
            return

        current_time = time.time()
        # 移除过期的时间戳
        self.data[key] = [
            (ts, val) for ts, val in self.data[key]
            if current_time - ts <= self.ttl
        ]

        if not self.data[key]:
            del self.data[key]
```

#### 3. 磁盘持久化
```python
import pickle
import os

class TimeMapWithDisk:
    def __init__(self, memory_limit=1000):
        self.memory_data = {}
        self.disk_keys = set()
        self.memory_limit = memory_limit

    def _flush_to_disk(self, key):
        if key in self.memory_data:
            with open(f"data_{key}.pkl", "wb") as f:
                pickle.dump(self.memory_data[key], f)
            del self.memory_data[key]
            self.disk_keys.add(key)

    def _load_from_disk(self, key):
        if key in self.disk_keys:
            with open(f"data_{key}.pkl", "rb") as f:
                self.memory_data[key] = pickle.load(f)
            self.disk_keys.remove(key)
```

---

## Follow-up 3: 未来时间戳处理

**问题：** 如果 `get(key, future_timestamp)` 传入未来时间戳怎么处理？

### 问题分析：

**核心挑战：** 传统的 get 操作是查找"小于等于给定时间戳的最新值"，但如果时间戳是未来的，我们需要等待可能的新数据。

**业务场景：**
```
当前时间: 10
调用: get("key", 20)  # 查询未来时间点的值
时间 15: set("key", "value_15")  # 有新数据写入
问题: get("key", 20) 应该返回什么？
- 选项1: 立即返回当前最新值
- 选项2: 等待到时间20，返回那时的最新值 (即 "value_15")
```

**技术难点：**
1. **阻塞风险**：如果等待时间过长(如1000年后)，线程会被长期阻塞
2. **死锁风险**：在有锁的环境下，长时间等待容易导致死锁
3. **资源浪费**：大量线程等待未来时间，消耗系统资源

### 解决方案：

#### 1. 同步等待 (简单但有风险)
```python
import time

def get(self, key: str, timestamp: int) -> str:
    current = time.time()
    if timestamp > current:
        time.sleep(timestamp - current)  # 等待到指定时间

    # 正常查找逻辑
```

#### 2. 异步回调 (推荐)
```python
import threading
from typing import Callable

class AsyncTimeMap:
    def __init__(self):
        self.data = {}
        self.pending_queries = []

    def get_async(self, key: str, timestamp: int, callback: Callable):
        current_time = time.time()

        if timestamp <= current_time:
            # 立即返回
            result = self._get_immediate(key, timestamp)
            callback(result)
        else:
            # 加入待处理队列
            self.pending_queries.append({
                'key': key,
                'timestamp': timestamp,
                'callback': callback,
                'scheduled_time': timestamp
            })

    def _process_pending_queries(self):
        current_time = time.time()
        ready_queries = [q for q in self.pending_queries if q['scheduled_time'] <= current_time]

        for query in ready_queries:
            result = self._get_immediate(query['key'], query['timestamp'])
            query['callback'](result)
            self.pending_queries.remove(query)
```

---

## 系统设计扩展

### 分布式 TimeMap
- **分片策略**: 按 key 哈希分片
- **一致性**: 使用分布式锁或 Raft 协议
- **复制**: 主从复制保证高可用

### 性能优化
- **索引**: 为热点 key 建立 B+ 树索引
- **缓存**: Redis 缓存热点数据
- **压缩**: 对历史数据进行压缩存储

## 测试用例

```python
def test_basic_functionality():
    tm = TimeMap()
    tm.set("key1", "value1", 1)
    tm.set("key1", "value2", 3)

    assert tm.get("key1", 2) == "value1"
    assert tm.get("key1", 3) == "value2"
    assert tm.get("key1", 4) == "value2"
    assert tm.get("nonexistent", 1) == ""

def test_concurrent_access():
    tm = ThreadSafeTimeMap()

    def writer():
        for i in range(100):
            tm.set("key", f"value{i}", i)

    def reader():
        for i in range(100):
            result = tm.get("key", i)
            # 验证结果合理性

    threads = [threading.Thread(target=writer) for _ in range(5)]
    threads.extend([threading.Thread(target=reader) for _ in range(10)])

    for t in threads:
        t.start()
    for t in threads:
        t.join()
```

## 面试要点总结

1. **基础实现**: 使用 bisect 优化查找
2. **并发处理**: 根据场景选择合适的锁策略
3. **内存管理**: LRU、TTL、磁盘持久化
4. **未来时间戳**: 异步处理比同步等待更优
5. **系统设计**: 分片、复制、缓存等扩展方案

**时间复杂度分析:**
- set: O(1) amortized (假设 timestamp 递增)
- get: O(log n) where n is the number of timestamps for the key