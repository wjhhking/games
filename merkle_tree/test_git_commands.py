#!/usr/bin/env python3

import git_merkle_tree_03

def test_git_commands():
    print("--- Testing git add/commit/log ---")
    
    # First commit
    git_merkle_tree_03.git_add("file1.txt", "Initial content for file 1")
    git_merkle_tree_03.git_add("file2.txt", "Initial content for file 2")
    first_commit_hash = git_merkle_tree_03.git_commit("Initial commit with two files")
    
    print(f"\nHEAD is now: {git_merkle_tree_03.HEAD}")
    assert git_merkle_tree_03.HEAD == first_commit_hash
    
    # Second commit
    git_merkle_tree_03.git_add("file1.txt", "Updated content for file 1")
    git_merkle_tree_03.git_add("file3.txt", "A new file for the second commit")
    second_commit_hash = git_merkle_tree_03.git_commit("Update file1 and add file3")
    
    print(f"\nHEAD is now: {git_merkle_tree_03.HEAD}")
    assert git_merkle_tree_03.HEAD == second_commit_hash
    
    # Third commit
    git_merkle_tree_03.git_add("file2.txt", "Updated content for file 2")
    third_commit_hash = git_merkle_tree_03.git_commit("A final update to file2")
    
    print(f"\nHEAD is now: {git_merkle_tree_03.HEAD}")
    assert git_merkle_tree_03.HEAD == third_commit_hash
    
    print("\n--- Testing git log ---")
    git_merkle_tree_03.git_log()
    
    print("\n--- Testing diff between first and third commit ---")
    git_merkle_tree_03.diff(first_commit_hash, third_commit_hash)

if __name__ == "__main__":
    test_git_commands() 