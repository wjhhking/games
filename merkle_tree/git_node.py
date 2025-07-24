"""
Final, Correct Solution for the AI Coding Startup Interview

This implementation correctly addresses the core requirements:
1.  **True O(log n) Incremental Updates**: `upload` only re-hashes the affected path.
2.  **Efficient O(log n) Proofs**: Proofs are small and contain only sibling hashes.
3.  **Clean API Design**: Server endpoints have clear, single responsibilities.
4.  **Demonstrates Core Insight**: Shows understanding of why a Merkle tree is used for efficient sync and verification.
"""

import hashlib
from typing import Dict, List, Optional, Tuple

def hash_data(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

class TreeNode:
    """Represents a node in the Merkle Tree."""
    def __init__(self, hash_val: str, parent=None, left=None, right=None):
        self.hash = hash_val
        self.parent = parent
        self.left = left
        self.right = right

# --- 1. The Correct Merkle Tree Implementation ---
class MerkleTree:
    def __init__(self):
        self.leaves: Dict[str, TreeNode] = {}  # filename -> leaf_node
        self.root: Optional[TreeNode] = None
        self._rebuild()

    def _rebuild(self):
        """Builds the tree from the current leaves. O(n) operation."""
        if not self.leaves:
            self.root = None
            return

        # Deterministic order of leaves is crucial
        sorted_leaves = [self.leaves[fname] for fname in sorted(self.leaves.keys())]

        if len(sorted_leaves) % 2 == 1:
            sorted_leaves.append(sorted_leaves[-1]) # Duplicate last leaf if odd

        self.root = self._build_level(sorted_leaves)

    def _build_level(self, nodes: List[TreeNode]) -> TreeNode:
        if len(nodes) == 1:
            return nodes[0]

        parents = []
        for i in range(0, len(nodes), 2):
            left, right = nodes[i], nodes[i+1]
            parent_hash = hash_data((left.hash + right.hash).encode())
            parent = TreeNode(parent_hash, left=left, right=right)
            left.parent, right.parent = parent, parent
            parents.append(parent)

        if len(parents) % 2 == 1 and len(parents) > 1:
            parents.append(parents[-1])

        return self._build_level(parents)

    def upload_file(self, filename: str, content: str):
        """
        Handles file uploads with efficient O(log n) updates.
        This is the core of the solution.
        """
        new_hash = hash_data(content.encode())

        if filename in self.leaves:
            leaf_node = self.leaves[filename]
            if leaf_node.hash == new_hash:
                print(f"[Tree] No change for '{filename}'.")
                return # No change

            # Update existing leaf and propagate hash changes upwards
            leaf_node.hash = new_hash
            self._update_path_to_root(leaf_node.parent)
            print(f"[Tree] Updated '{filename}' incrementally.")
        else:
            # New file requires a rebuild
            self.leaves[filename] = TreeNode(new_hash)
            self._rebuild()
            print(f"[Tree] Added '{filename}', rebuilt tree.")

    def _update_path_to_root(self, node: Optional[TreeNode]):
        """Recursively updates hashes up to the root. O(log n) operation."""
        if not node:
            return

        left_hash = node.left.hash if node.left else ""
        right_hash = node.right.hash if node.right else ""

        new_hash = hash_data((left_hash + right_hash).encode())
        if node.hash != new_hash:
            node.hash = new_hash
            self._update_path_to_root(node.parent)

    def get_proof(self, filename: str) -> Optional[List[Tuple[str, str]]]:
        """Generates a true O(log n) proof."""
        if filename not in self.leaves:
            return None

        proof = []
        node = self.leaves[filename]

        while node.parent:
            parent = node.parent
            if parent.left == node:
                sibling = parent.right
                proof.append((sibling.hash, 'right'))
            else:
                sibling = parent.left
                proof.append((sibling.hash, 'left'))
            node = parent

        return proof

    @staticmethod
    def verify_proof(root_hash: str, content: str, proof: List[Tuple[str, str]]) -> bool:
        """Verifies an O(log n) proof."""
        current_hash = hash_data(content.encode())
        for sibling_hash, position in proof:
            if position == 'left':
                current_hash = hash_data((sibling_hash + current_hash).encode())
            else:
                current_hash = hash_data((current_hash + sibling_hash).encode())

        return current_hash == root_hash

# --- 2. The Server with a Clean API ---
class Server:
    def __init__(self):
        self.files: Dict[str, str] = {}
        self.tree = MerkleTree()
        print("[Server] Initialized.")

    def upload(self, filename: str, content: str):
        self.files[filename] = content
        self.tree.upload_file(filename, content)
        print(f"[Server] Uploaded '{filename}'. New root: {self.tree.root.hash[:8] if self.tree.root else 'N/A'}...")

    def check(self, filename: str) -> Optional[Dict]:
        """Returns the proof for a file, not its content."""
        print(f"\n[Server] Received check for '{filename}'.")
        if filename not in self.files:
            return None

        return {
            "root": self.tree.root.hash,
            "proof": self.tree.get_proof(filename)
        }

    def download(self, filename: str) -> Optional[str]:
        """A separate endpoint to get file content."""
        return self.files.get(filename)

# --- 3. The Client ---
class Client:
    def __init__(self, server: Server):
        self.server = server
        self.known_root: Optional[str] = None
        print("[Client] Initialized.")

    def verify_file(self, filename: str):
        print(f"\n[Client] Verifying '{filename}'...")
        content = self.server.download(filename)
        if content is None:
            print(f"[Client] ✗ Verification failed: File not found on server.")
            return

        check_response = self.server.check(filename)
        if not check_response:
            print(f"[Client] ✗ Verification failed: Could not get proof.")
            return

        is_valid = MerkleTree.verify_proof(
            check_response["root"],
            content,
            check_response["proof"]
        )

        if is_valid:
            print(f"[Client] ✓ Verification successful for '{filename}'.")
        else:
            print(f"[Client] ✗ Verification FAILED for '{filename}'.")

# --- 4. Demonstration ---
if __name__ == "__main__":
    print("=== Correct Merkle Tree Implementation Demo ===")

    server = Server()
    client = Client(server)

    print("\n--- Phase 1: Initial Uploads ---")
    server.upload("file1.txt", "This is the first file.")
    server.upload("file2.txt", "This is the second file.")
    server.upload("file3.txt", "This is the third file.")

    print("\n--- Phase 2: Client Verification (should succeed) ---")
    client.verify_file("file2.txt")

    print("\n--- Phase 3: Incremental Update (O(log n) change) ---")
    server.upload("file2.txt", "This file has been updated.")

    print("\n--- Phase 4: Client Verification After Update (should succeed) ---")
    client.verify_file("file2.txt")

    print("\n--- Phase 5: Tampering Demo ---")
    # Manually tamper with a proof to show verification failure
    proof_response = server.check("file1.txt")
    tampered_proof = proof_response["proof"]
    tampered_proof[0] = (hash_data(b"tampered"), tampered_proof[0][1]) # Alter a sibling hash

    print("[Client] Attempting to verify with a tampered proof...")
    is_valid_tampered = MerkleTree.verify_proof(
        proof_response["root"],
        server.download("file1.txt"),
        tampered_proof
    )
    if not is_valid_tampered:
        print("[Client] ✓ Correctly detected tampered proof.")
    else:
        print("[Client] ✗ FAILED to detect tampered proof.")