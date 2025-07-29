# Resumable Iterator Problem

This problem is divided into four parts. You will be building a series of "resumable"
iterators, which can be saved at a certain point and restored to that same point later.

---

### Part 1: The Interface

First, define an abstract base class for a resumable iterator. It should have the
following interface. Note the absence of a `hasNext()` method; you should rely on
Python's standard iteration protocol (`__next__` raising `StopIteration`).

```python
import abc

class ResumableIterator(abc.ABC):
    @abc.abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __next__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_state(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_state(self, state):
        raise NotImplementedError
```

---

### Part 2: List Iterator and Test-Driven Development

**Task 1: Implement a List Iterator**

Implement a concrete class `ListIterator` that conforms to the `ResumableIterator`
interface. This iterator will walk through a standard Python list. The state you
save and restore can be a simple index.

**Task 2: Implement a Generic Test Function**

A key part of this problem is testing. Write a generic test function
`test_iterator(...)` that rigorously validates the `get_state` and `set_state`
functionality.

This function should:
1. Create an instance of the iterator.
2. Iterate through it completely, from start to finish.
3. At *every* step of the iteration (including before the first `next()` call),
   call `get_state()` and store the returned state object.
4. After the iterator is exhausted, loop through the list of saved states.
5. For each saved state:
   a. Create a *new* instance of the iterator.
   b. Use `set_state()` to restore it to that saved state.
   c. Iterate from the restored point to the end.
   d. Assert that the elements produced by the iterator match the expected
      sequence from that point forward.

**Task 3: Run the Test**

Use your `test_iterator` function to validate your `ListIterator` implementation.

---

### Part 3: Multiple File Iterator

Now, implement `MultipleResumableFileIterator`. This iterator takes a list of JSON file paths and iterates over all their elements sequentially, as if they were a single stream of data.

**Requirements:**
- It must conform to the `ResumableIterator` interface.
- Use existing `ResumableFileIterator` instances to read each JSON file.
- Handle empty files gracefully (skip them and continue to the next file).
- Handle the case where all files are empty or the file list is empty.
- The state object must track both which file you are currently reading and the state within that file.

**Implementation Strategy:**
This problem combines the concepts from LeetCode 251 (2D Vector) with resumable iterators:
- Maintain a list of `ResumableFileIterator` objects, one for each file.
- Track the current file index and the state of the current file iterator.
- When a file iterator is exhausted, move to the next non-empty file.
- For `get_state()`: return a tuple containing (current_file_index, current_file_iterator_state).
- For `set_state()`: restore both the file index and set the appropriate file iterator's state.

**Example:**
```python
# Files: file1.json: [1, 2], file2.json: [], file3.json: [3, 4]
# Iterator should produce: 1, 2, 3, 4 (skipping the empty file2.json)

file_paths = ["file1.json", "file2.json", "file3.json"]
iterator = MultipleResumableFileIterator(file_paths)
```

**Testing:**
Use your `test_iterator` function to validate your `MultipleResumableFileIterator` implementation, ensuring it correctly handles:
- Normal files with data
- Empty files
- Mixed scenarios with some empty and some non-empty files
- Edge case where all files are empty

---

这样的描述更准确地反映了实际的技术挑战：处理文件I/O、状态管理的复杂性、以及空文件处理的边界情况。

---

### Part 4: Asynchronous Iterators (Follow-up)

As a follow-up, convert your implementations to be asynchronous.

1.  Define an `AsyncResumableIterator` interface with `__aiter__` and `__anext__`.
2.  Implement `AsyncListIterator` and `AsyncMultipleListIterator`.
3.  Write an `async_test_iterator` to validate the asynchronous versions. This will
    be an `async def` function and will use `async for` and `await`.

The goal is to understand how these concepts translate to an asynchronous context,
which is common for I/O-bound operations like reading multiple files from a
network or disk.
