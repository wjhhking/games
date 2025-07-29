# Interview Question: Implementing an Advanced `cd` (Change Directory) Command

This question assesses your ability to manipulate strings, handle edge cases, and work with complex data structures to simulate the behavior of the `cd` command in a Unix-like shell, including support for symbolic links.

## Part 1: Basic Path Simplification

### Objective

Implement a function `cd(current_dir, new_dir)` that simulates changing the current working directory. The function should take the current directory path and a new path (which can be absolute or relative) and return the resulting absolute path.

### Requirements

- An absolute path starts with `/`.
- `.` refers to the current directory.
- `..` refers to the parent directory. Moving up from the root directory (`/`) should result in the root directory itself.
- Multiple slashes should be treated as a single slash (e.g., `//` is equivalent to `/`).

### Function Signature

```python
def cd(current_dir: str, new_dir: str) -> str:
```

### Examples

- `cd("/foo/bar", "baz")` → `"/foo/bar/baz"`
- `cd("/foo/bar", "../baz")` → `"/foo/baz"`
- `cd("/home", "/user/profile")` → `"/user/profile"` (since `new_dir` is an absolute path)
- `cd("/", "foo/bar/../../baz")` → `"/baz"`
- `cd("/", "..")` → `"/"`

## Part 2: Support for Home Directory (`~`)

### Objective

Extend your `cd` function to support the `~` character, which represents the user's home directory. For the purpose of this problem, assume the home directory is always `/home/user`.

### Requirements

- If `~` appears at the beginning of `new_dir`, it should be expanded to `/home/user`.
- If `~` appears elsewhere in the path, it should be treated as a regular directory name.

### Function Signature (no change)

```python
def cd(current_dir: str, new_dir: str) -> str:
```

### Examples

- `cd("/foo/bar", "~/documents")` → `"/home/user/documents"`
- `cd("/foo", "bar/~/baz")` → `"/foo/bar/~/baz"`
- `cd("/home/user/downloads", "~")` → `"/home/user"`

## Part 3: Symbolic Links (Symlinks)

### Objective

Further enhance the `cd` function to handle symbolic links. You will be given a dictionary (or map) where keys are source paths (symlinks) and values are their target paths. After calculating a new path, you must check if it (or any of its parent paths) is a symlink and resolve it.

### Requirements

- **Longest Prefix Match**: If multiple symlinks from the dictionary are a prefix of your calculated path, you must use the longest (most specific) one.
- **Recursive Resolution**: The target of a symlink might itself be another symlink. You should continue resolving until the path is no longer a symlink.
- **Path Combination**: After resolving a symlink, any remaining part of the original path should be appended to the resolved symlink target.

### Function Signature

```python
def cd_with_symlinks(current_dir: str, new_dir: str, symlinks: dict[str, str]) -> str:
```

### Examples

- **Simple Symlink**
  - **Input**: `cd_with_symlinks("/foo", "bar", {"/foo/bar": "/abc"})`
  - **Resolution**: Initial Path: `/foo/bar` -> Resolves to `/abc`
  - **Result**: `"/abc"`

- **Longest Prefix Match**
  - **Input**: `cd_with_symlinks("/foo", "bar/baz", {"/foo": "/a", "/foo/bar": "/b"})`
  - **Resolution**: Initial Path: `/foo/bar/baz` -> Longest match is `/foo/bar`, which maps to `/b`.
  - **Result**: `"/b/baz"`

- **Recursive Symlink**
  - **Input**: `cd_with_symlinks("/a", "b", {"/a/b": "/c", "/c": "/d/e"})`
  - **Resolution**: Initial Path: `/a/b` -> Resolves to `/c` -> Resolves to `/d/e`
  - **Result**: `"/d/e"`

## Part 4: Cycle Detection in Symbolic Links

### Objective

The final challenge is to detect and handle cyclical references within the symbolic links. If resolving a path leads into a cycle, your function should throw an exception.

### Requirements

- If a cycle is detected during symlink resolution, raise a `ValueError` with a descriptive message.
- A cycle occurs if you encounter the same symlink source path more than once while resolving a single `cd` command.

### Function Signature (no change)

```python
def cd_with_symlinks(current_dir: str, new_dir: str, symlinks: dict[str, str]) -> str:
```

### Examples

- **Direct Cycle**
  - **Input**: `cd_with_symlinks("/", "a", {"/a": "/b", "/b": "/a"})`
  - **Resolution**: Path `/a` -> Resolves to `/b` -> Resolves to `/a`... (Cycle detected)
  - **Result**: `ValueError("Cyclical symbolic link detected.")`

- **Indirect Cycle**
  - **Input**: `cd_with_symlinks("/", "start", {"/start": "/link1", "/link1": "/link2", "/link2": "/link1"})`
  - **Resolution**: Path `/start` -> `/link1` -> `/link2` -> `/link1`... (Cycle detected)
  - **Result**: `ValueError("Cyclical symbolic link detected.")`

## Evaluation Criteria

- **Correctness**: Does the code produce the correct output for all test cases, including edge cases?
- **Code Quality**: Is the code clean, well-structured, and easy to understand?
- **Algorithm Design**: Is the approach for path normalization, symlink resolution, and cycle detection efficient?
- **Problem Solving**: Can you break down the complex problem into smaller, manageable parts and build upon your solution for each follow-up?