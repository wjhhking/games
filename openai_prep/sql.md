# In-Memory Database 设计面试题

## 题目描述
设计并实现一个简单的内存数据库，支持基本的SQL操作。你需要逐步实现以下功能，每个阶段都需要通过测试用例。

## 基本要求
- **不需要**解析SQL语句，自定义API接口即可
- 所有数据类型都当作**字符串**处理
- 与面试官确认接口设计后立即开始实现
- 每个功能点完成后需要能够编译运行

## 功能实现阶段

### 阶段1：基础功能
- 插入数据行（第一次插入时自动创建表和列）
- 基本查询（返回所有行的指定列）

### 阶段2：WHERE条件查询
- 单列WHERE条件查询（支持 =, >, < 操作符）
- 多列WHERE条件查询（AND关系）

### 阶段3：复杂条件
- 混合使用等值和比较操作
- 多个条件的组合查询

### 阶段4：排序功能
- 单列ORDER BY
- 多列ORDER BY
- 支持升序和降序

### 阶段5：高级功能（时间允许的话）
- 倒排索引实现

## 示例API设计

```python
# 方案1：分离式API
class InMemoryDB:
    def insert(self, table_name: str, row: dict):
        pass

    def query(self, table_name: str, select_columns: list):
        pass

    def query_with_where(self, table_name: str, select_columns: list, conditions: list):
        # conditions: [["column", "operator", "value"], ...]
        pass

    def query_with_order_by(self, table_name: str, select_columns: list,
                           order_by_columns: list, reverse: bool = False):
        pass

# 方案2：统一式API
class InMemoryDB:
    def insert(self, table_name: str, row: dict):
        pass

    def query(self, table_name: str, select_columns: list,
              conditions: list = None, order_by: list = None, reverse: bool = False):
        # conditions: [["column", "operator", "value"], ...]
        # order_by: ["column1", "column2", ...]
        pass
```

## 测试用例示例

```python
# 直接插入数据，表和列会自动创建
db.insert("users", {"id": "1", "name": "Ada", "birthday": "1815-12-10"})
db.insert("users", {"id": "2", "name": "Charles", "birthday": "1791-12-26"})
db.insert("users", {"id": "3", "name": "Ben", "birthday": "1715-12-11"})

# 基础查询
assert db.query("users", ["name"]) == [
    {"name": "Ada"},
    {"name": "Charles"},
    {"name": "Ben"}
]

# WHERE条件查询（支持 =, >, < 操作符）
assert db.query("users", ["name"], [["birthday", ">", "1800-01-01"]]) == [
    {"name": "Ada"}
]

assert db.query("users", ["name"], [["birthday", "<", "1800-01-01"]]) == [
    {"name": "Charles"}, {"name": "Ben"}
]

# ORDER BY查询
assert db.query("users", ["name"], [["birthday", "<", "1800-01-01"]], "birthday") == [
    {"name": "Ben"},
    {"name": "Charles"}
]
```

## 实现提示

### 数据结构建议
- 使用Map存储表（表名 -> 表对象）
- 每个表用List存储行数据
- 用Map记录列名到索引的映射

### 性能考虑
- WHERE条件：直接表扫描（O(n)），无需构建索引
- ORDER BY：使用Python内置排序（O(n log n)）
- 时间复杂度不是重点，重点是功能完整性和代码正确性

### 常见注意点
- 第一次插入时动态创建列映射
- 字符串比较逻辑的正确实现
- 多列排序时排序键的构造
- 处理不存在的表名或列名
- 边界条件（空表、空条件等）

## 评分标准
1. **功能完整性**（40%）：能否实现所有要求的功能
2. **代码质量**（30%）：代码结构清晰，命名规范
3. **测试通过**（20%）：所有测试用例能够通过
4. **沟通能力**（10%）：与面试官的交流和假设确认

## 时间分配建议
- 阶段1-2：15-20分钟
- 阶段3：10分钟
- 阶段4：10-15分钟
- 阶段5：5-10分钟（可选）

## 注意事项
- 优先完成基础功能，再考虑优化
- 及时与面试官确认需求理解
- 代码要能编译运行，功能正确性很重要
- 如果时间不够，说明实现思路即可