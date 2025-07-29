# LRU Cache 变种 - 频次优先缓存

## 题目背景
设计一个频次优先的缓存系统，能够跟踪键的访问频次，并快速找到最高频次的键。

## 第一阶段：基础实现 (15分钟)
实现一个 `FrequencyCache` 类，支持以下操作：

```python
class FrequencyCache:
    def addKey(self, key: str) -> None:
        """添加或增加键的访问频次"""
        pass

    def getCountForKey(self, key: str) -> int:
        """获取指定键的访问次数，如果键不存在返回0"""
        pass

    def getMaxFrequencyKey(self) -> str:
        """返回频次最高的键，如果为空返回空字符串"""
        pass
```

**要求：**
- `addKey`: O(log n) 时间复杂度
- `getCountForKey`: O(1) 时间复杂度
- `getMaxFrequencyKey`: O(1) 时间复杂度

**示例：**
```python
cache = FrequencyCache()
cache.addKey("a")        # {"a": 1}
cache.addKey("b")        # {"a": 1, "b": 1}
cache.getMaxFrequencyKey()  # "b" (字典序较大)
cache.addKey("a")        # {"a": 2, "b": 1}
cache.getMaxFrequencyKey()  # "a" (频次更高)
```

## 第二阶段：优先级规则 (10分钟)
现在优先级规则需要调整：
1. 首先按频次降序排列
2. 频次相同时，按键的字典序升序排列（与第一阶段相反）

**追问：** 如果未来优先级规则可能经常变化，你会如何设计？

## 第三阶段：动态优先级 (15分钟)
系统现在需要支持动态调整优先级规则：

```python
def setPriorityRule(self, rule_func) -> None:
    """设置新的优先级比较函数"""
    pass
```

其中 `rule_func(item1, item2)` 返回 True 表示 item1 优先级更高。

**追问：**
1. 当优先级规则改变时，如何高效地重新组织数据结构？
2. 时间复杂度如何变化？

## 第四阶段：容量限制 (10分钟)
添加容量限制功能：

```python
def __init__(self, capacity: int):
    """初始化指定容量的缓存"""
    pass

def addKey(self, key: str) -> str:
    """返回被移除的键（如果有），否则返回空字符串"""
    pass
```

当容量满时，移除优先级最低的键。

## 第五阶段：性能优化 (10分钟)
**场景：** 系统需要处理高并发访问，可能有以下pattern：
- 大量重复键的访问
- 频繁的优先级查询
- 偶尔的优先级规则变更

**追问：**
1. 如何优化频繁的 heap 调整操作？
2. 能否用其他数据结构替代 heap 来提升性能？
3. 如何处理并发安全问题？

## 评分标准

### 优秀 (90-100分)
- 正确实现所有阶段功能
- 数据结构选择合理（heap + hashmap）
- 能够处理边界情况
- 对动态优先级有深入思考
- 提出合理的性能优化方案

### 良好 (70-89分)
- 基础功能实现正确
- 理解数据结构的选择原因
- 能够分析时间复杂度
- 对优先级变更有基本理解

### 一般 (50-69分)
- 基础功能大部分正确
- 数据结构使用基本合理
- 需要提示才能处理复杂场景

### 需要改进 (<50分)
- 基础功能实现有误
- 对数据结构理解不足
- 无法分析复杂度

## 常见陷阱
1. **heap 位置维护：** 忘记在 swap 时更新位置映射
2. **边界情况：** 空缓存时的 getMaxFrequencyKey
3. **优先级变更：** 没有考虑到需要重建整个 heap
4. **容量限制：** 忘记处理移除元素时的位置映射清理

## 扩展讨论
- 如果需要支持 `removeKey` 操作怎么办？
- 如果需要获取前 K 个高频键怎么办？
- 如何实现频次衰减（时间窗口内的频次）？