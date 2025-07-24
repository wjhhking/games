import hashlib
import json
import time
from typing import Optional, Union

# --- Git's Internal State Simulation ---
GIT_DB: dict[str, Union['Blob', 'Tree', 'Commit']] = {}
HEAD: Optional[str] = None
staging_area: dict[str, str] = {} # Maps filename to blob hash (the "index")

def sha1(text: str) -> str:
    """The one and only hash function for our system."""
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

class Blob:
    """A blob's hash is the hash of its type and content."""
    def __init__(self, file_content: str):
        self.content = file_content
        # Hash a tuple of (type, data) to prevent hash collisions between object types.
        self.hash = sha1(json.dumps(('blob', self.content)))
        GIT_DB[self.hash] = self

    def __repr__(self):
        return f"Blob(hash='{self.hash[:7]}...')"

class Tree:
    """A tree's hash is the hash of its type and entries."""
    def __init__(self):
        # Simplified: entries just map a name to a hash.
        self.entries: dict[str, str] = {}
        self.hash: Optional[str] = None

    def add_entry(self, name: str, obj_hash: str):
        self.entries[name] = obj_hash

    def bake(self) -> str:
        """Computes the hash for the tree and finalizes it."""
        # We must serialize the tuple to a stable string before hashing.
        # json.dumps is the simplest way to do this.
        self.hash = sha1(json.dumps(('tree', self.entries), sort_keys=True))
        GIT_DB[self.hash] = self
        return self.hash

    def __repr__(self):
        return f"Tree(hash='{self.hash[:7] if self.hash else 'unbaked'}...', entries={len(self.entries)})"

class Commit:
    """A commit's hash is the hash of its type, pointers, and metadata JSON."""
    def __init__(self, tree_hash: str, parent_hash: Optional[str], metadata: dict):
        self.tree_hash = tree_hash
        self.parent_hash = parent_hash
        self.metadata = metadata

        # Hash a tuple of the commit's essential data.
        # sort_keys=True is crucial for the metadata dictionary to ensure determinism.
        data_tuple = ('commit', self.tree_hash, self.parent_hash, self.metadata)
        self.hash = sha1(json.dumps(data_tuple, sort_keys=True))
        GIT_DB[self.hash] = self

    def __repr__(self):
        message = self.metadata.get('message', '').strip()
        return f"Commit(hash='{self.hash[:7]}...', msg='{message}')"

# --- Porcelain Commands (User-Facing API) ---

def git_add(filename: str, content: str):
    """Creates a blob and adds it to the staging area (the 'index')."""
    blob = Blob(content)
    staging_area[filename] = blob.hash
    print(f"Staged '{filename}' for commit.")

def git_commit(metadata: dict):
    """Creates a tree from the staging area and the parent commit, then commits it."""
    global HEAD
    if not staging_area:
        print("Nothing to commit, staging area is empty.")
        return None

    # Start with the parent tree's content, if it exists.
    current_tree_entries = {}
    if HEAD:
        parent_commit = GIT_DB.get(HEAD)
        if isinstance(parent_commit, Commit):
            parent_tree = GIT_DB.get(parent_commit.tree_hash)
            if isinstance(parent_tree, Tree):
                current_tree_entries = parent_tree.entries.copy() # Important to copy!

    # Apply staged changes to the inherited entries.
    current_tree_entries.update(staging_area)

    # Bake the new tree from the combined entries.
    tree = Tree()
    tree.entries = current_tree_entries
    tree_hash = tree.bake()

    commit = Commit(tree_hash, HEAD, metadata)
    HEAD = commit.hash
    staging_area.clear() # Clear the index after commit

    print(f"Committed on top of {commit.parent_hash[:7] if commit.parent_hash else 'None'}. New HEAD is {HEAD[:7]}...")
    return HEAD

def git_log(commit_hash: Optional[str]):
    """Traverses and prints the commit history."""
    print("--- Git Log ---")
    current_hash = commit_hash
    while current_hash:
        commit = GIT_DB.get(current_hash)
        if not isinstance(commit, Commit):
            break

        print(f"Commit: {commit.hash}")
        print(f"    {commit.metadata.get('message', 'No commit message')}")
        print("-" * 20)
        current_hash = commit.parent_hash

def git_diff(hash_a: str, hash_b: str):
    """Compares the trees of two commits and prints the differences."""
    commit_a = GIT_DB.get(hash_a)
    commit_b = GIT_DB.get(hash_b)

    tree_a = GIT_DB.get(commit_a.tree_hash) if isinstance(commit_a, Commit) else None
    tree_b = GIT_DB.get(commit_b.tree_hash) if isinstance(commit_b, Commit) else None

    if not isinstance(tree_a, Tree) or not isinstance(tree_b, Tree):
        print("Error: Could not find trees for one or both commits.")
        return

    print(f"--- Diff between {hash_a[:7]}... and {hash_b[:7]}... ---")
    entries_a = tree_a.entries
    entries_b = tree_b.entries
    all_files = set(entries_a.keys()) | set(entries_b.keys())

    for filename in sorted(all_files):
        blob_hash_a, blob_hash_b = entries_a.get(filename), entries_b.get(filename)
        if blob_hash_a and not blob_hash_b:
            print(f"REMOVED:  {filename}")
        elif not blob_hash_a and blob_hash_b:
            print(f"ADDED:    {filename}")
        elif blob_hash_a != blob_hash_b:
            print(f"MODIFIED: {filename}")

def main():
    """A demo simulating a git workflow with add, commit, log, and diff."""
    global HEAD

    # --- First Commit ---
    print("--- Staging and making initial commit ---")
    git_add("main.py", "print('hello world')")
    git_add("README.md", "Welcome to my project!")

    metadata_v1 = {"message": "Initial commit", "timestamp": int(time.time())}
    commit1_hash = git_commit(metadata_v1)
    print("")
    time.sleep(1)

    # --- Second Commit ---
    print("--- Staging and making a second commit ---")
    git_add("main.py", "print('hello world, updated!')") # Modify a file
    git_add("extra.txt", "An extra file.") # Add a new file
    # Note: README.md is not re-added, and the new commit will now correctly carry it forward.

    metadata_v2 = {
        "message": "Update main.py and add extra.txt",
        "author": "User <user@example.com>",
        "timestamp": int(time.time())
    }
    commit2_hash = git_commit(metadata_v2)
    print("")

    # --- Log and Diff ---
    git_log(HEAD)
    print("")
    git_diff(commit1_hash, commit2_hash)

if __name__ == "__main__":
    main()