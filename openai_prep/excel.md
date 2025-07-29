# Spreadsheet API Design Interview Problem

## Problem Statement

Design and implement a simplified spreadsheet system that supports cells with either numeric values or formulas that reference other cells.

### Core Requirements

You need to implement a `Spreadsheet` class with the following interface:

```python
class Spreadsheet:
    def get_cell_value(self, key: str) -> int:
        """Return the current value of the cell"""
        pass

    def set_cell(self, key: str, value=None, formula=None):
        """Set a cell to either a numeric value or a formula"""
        pass
```

### Cell Types
- **Value Cell**: Contains a numeric value (e.g., `set_cell("A1", value=10)`)
- **Formula Cell**: Contains a formula that adds two other cells (e.g., `set_cell("C1", formula=("A1", "B1"))`)

### Basic Example
```python
spreadsheet = Spreadsheet()

# Set value cells
spreadsheet.set_cell("A1", value=6)
spreadsheet.set_cell("B1", value=7)

# Set formula cell (A1 + B1)
spreadsheet.set_cell("C1", formula=("A1", "B1"))

print(spreadsheet.get_cell_value("C1"))  # Should output: 13

# Update a dependency
spreadsheet.set_cell("A1", value=5)
print(spreadsheet.get_cell_value("C1"))  # Should output: 12
```

## Part 1: Basic Implementation (15-20 minutes)

Implement the basic functionality using a simple recursive approach. Don't worry about efficiency yet.

**Test Cases:**
```python
# Basic functionality
spreadsheet = Spreadsheet()
spreadsheet.set_cell("A1", value=6)
spreadsheet.set_cell("B1", value=7)
spreadsheet.set_cell("C1", formula=("A1", "B1"))
assert spreadsheet.get_cell_value("C1") == 13

# Dynamic updates
spreadsheet.set_cell("A1", value=5)
assert spreadsheet.get_cell_value("C1") == 12

# Chained formulas
spreadsheet.set_cell("D1", value=10)
spreadsheet.set_cell("E1", formula=("C1", "D1"))  # (A1 + B1) + D1
assert spreadsheet.get_cell_value("E1") == 22
```

## Part 2: Optimization (15-20 minutes)

**Follow-up Question**: "The current implementation recalculates values every time `get_cell_value` is called. How would you optimize this for better read performance when there are many repeated reads?"

### Requirements:
- Add caching to avoid redundant calculations
- Properly invalidate cache when dependencies change
- Handle the case where a cell changes from a value to a formula or vice versa

**Additional Test Cases:**
```python
# Test cache invalidation
spreadsheet.set_cell("F1", value=20)
spreadsheet.set_cell("G1", formula=("F1", "A1"))
old_value = spreadsheet.get_cell_value("G1")

# Change F1 from value to formula
spreadsheet.set_cell("F1", formula=("A1", "B1"))
new_value = spreadsheet.get_cell_value("G1")
assert new_value != old_value
```

## Part 3: Cycle Detection (10-15 minutes)

**Follow-up Question**: "What happens if there's a circular dependency? How would you detect and handle this?"

### Requirements:
- Detect circular dependencies during `set_cell` operations
- Raise an appropriate exception when a cycle is detected
- Ensure the spreadsheet remains in a valid state

**Test Cases:**
```python
# Test cycle detection
spreadsheet = Spreadsheet()
spreadsheet.set_cell("X1", value=1)
spreadsheet.set_cell("Y1", value=2)
spreadsheet.set_cell("Z1", formula=("X1", "Y1"))

# This should raise an exception
try:
    spreadsheet.set_cell("X1", formula=("Z1", "Y1"))  # Creates X1 -> Z1 -> X1 cycle
    assert False, "Should have detected cycle"
except ValueError as e:
    assert "cycle" in str(e).lower() or "circular" in str(e).lower()
```

## Bonus Questions (Time Permitting)

### Concurrency
"How would you handle concurrent access to the spreadsheet? What if multiple threads are reading and writing simultaneously?"

### Memory Optimization
"If this spreadsheet could have millions of cells, how would you optimize memory usage?"

### Extended Formulas
"How would you extend this to support more complex formulas like SUM(A1:A10) or multiplication?"

## Evaluation Criteria

### Must Have:
- ✅ Correct basic functionality with recursive evaluation
- ✅ Proper handling of dependency updates
- ✅ Cache implementation that improves read performance
- ✅ Cache invalidation when dependencies change
- ✅ Cycle detection with appropriate error handling

### Nice to Have:
- Clean, readable code structure
- Efficient algorithms (O(1) reads after caching, efficient invalidation)
- Thoughtful discussion of trade-offs
- Good error handling and edge case consideration
- Clear explanation of approach and optimizations

## Implementation Notes

**Common Pitfalls:**
- Forgetting to handle the case where a cell changes type (value ↔ formula)
- Inefficient cache invalidation (invalidating too many or too few cells)
- Not properly detecting all types of cycles
- Memory leaks from not cleaning up old dependencies

**Key Insights:**
- This is fundamentally a directed graph problem
- Topological relationships matter for both evaluation and invalidation
- Cache invalidation should propagate through the dependency graph
- Cycle detection can be done during dependency graph construction