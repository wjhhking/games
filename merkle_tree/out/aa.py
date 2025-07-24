import hashlib
from typing import Optional

def hash256(s: str) -> str:
    """Computes SHA-256 hash of a string."""
    return hashlib.sha256(s.encode()).hexdigest()

class TreeNode:
    """Represents a node in the Merkle Tree."""
    def __init__(self, hash_val: str, parent: Optional['TreeNode'] = None, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.hash_val = hash_val
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.hash_val[:6]}...)"

class MerkleTree:
    """A Merkle Tree implementation using explicit nodes."""
    def __init__(self, data_list: list[str]):
        self.leaves: dict[str, TreeNode] = {}
        self.root = self.build_tree(data_list)

    def build_tree(self, data_list: list[str]) -> Optional[TreeNode]:
        if not data_list:
            return None

        nodes = []
        for data in data_list:
            leaf_hash = hash256(data)
            node = TreeNode(leaf_hash)
            nodes.append(node)
            self.leaves[data] = node

        while len(nodes) > 1:
            if len(nodes) % 2 == 1:
                nodes.append(nodes[-1]) # Duplicate last node if odd

            next_level_nodes = []
            for i in range(0, len(nodes), 2):
                left_child, right_child = nodes[i], nodes[i+1]
                parent_hash = hash256(left_child.hash_val + right_child.hash_val)
                parent_node = TreeNode(parent_hash, left=left_child, right=right_child)
                left_child.parent = parent_node
                right_child.parent = parent_node
                next_level_nodes.append(parent_node)

            nodes = next_level_nodes

        return nodes[0] if nodes else None

    def get_proof(self, data: str) -> Optional[list[tuple[str, str]]]:
        if data not in self.leaves:
            return None

        node, proof = self.leaves[data], []
        while node.parent:
            parent = node.parent
            if parent.left == node:
                if parent.right:
                    proof.append((parent.right.hash_val, 'R'))
            else:
                proof.append((parent.left.hash_val, 'L'))
            node = parent
        return proof

    def update(self, old_data: str, new_data: str):
        if old_data not in self.leaves:
            raise ValueError("Data to update not found")

        leaf_node = self.leaves[old_data]
        leaf_node.hash_val = hash256(new_data)
        del self.leaves[old_data]
        self.leaves[new_data] = leaf_node

        node = leaf_node
        while node.parent:
            parent = node.parent
            right_child_hash = parent.right.hash_val if parent.right else parent.left.hash_val
            parent.hash_val = hash256(parent.left.hash_val + right_child_hash)
            node = parent
        self.root = node

    @staticmethod
    def verify_proof(proof: list[tuple[str, str]], data: str, root_hash: str) -> bool:
        current_hash = hash256(data)
        for sibling_hash, position in proof:
            if position == 'L':
                current_hash = hash256(sibling_hash + current_hash)
            else:
                current_hash = hash256(current_hash + sibling_hash)
        return current_hash == root_hash

class Server:
    """The Server manages files and the master Merkle Tree."""
    def __init__(self):
        self.files: dict[str, str] = {}
        self.file_order: list[str] = []
        self.merkle_tree: Optional[MerkleTree] = None
        self._build_tree()

    def _build_tree(self):
        """Builds/rebuilds the tree. In a real system, adding a file
        would be more efficient, but a rebuild is fine for an interview."""
        all_content = [self.files[fname] for fname in self.file_order]
        self.merkle_tree = MerkleTree(all_content)

    @property
    def root(self) -> Optional[str]:
        return self.merkle_tree.root.hash_val if self.merkle_tree and self.merkle_tree.root else None

    def upload(self, filename: str, content: str):
        """Uploads a file. Updates the tree efficiently if the file
        exists, or rebuilds the tree for a new file."""
        if filename in self.files:
            # Efficient update for existing file
            print(f"Server: Updating '{filename}'...")
            old_content = self.files[filename]
            self.files[filename] = content
            self.merkle_tree.update(old_content, content)
        else:
            # Full rebuild for new file
            print(f"Server: Adding new file '{filename}'...")
            self.files[filename] = content
            self.file_order.append(filename)
            self._build_tree()

        print(f"Server: Upload complete. New root: {self.root}")

    def check(self, filename: str) -> Optional[list[tuple[str, str]]]:
        if filename not in self.files or not self.merkle_tree:
            return None
        return self.merkle_tree.get_proof(self.files[filename])

class Client:
    """The Client uploads and verifies files."""
    def __init__(self, server: Server):
        self.server = server
        self.local_files: dict[str, str] = {}

    def add_or_update_file(self, filename: str, content: str):
        self.local_files[filename] = content
        self.server.upload(filename, content)

    def verify_file(self, filename: str) -> bool:
        if filename not in self.local_files:
            return False

        content = self.local_files[filename]
        proof = self.server.check(filename)
        server_root = self.server.root

        if proof is None or server_root is None:
            return False

        return MerkleTree.verify_proof(proof, content, server_root)

def test_final_system():
    """Comprehensive test of the client-server system with efficient updates."""
    print("--- Testing Final Client-Server System ---")
    server = Server()
    client = Client(server)

    # 1. Add initial files
    client.add_or_update_file("file1.txt", "alpha")
    client.add_or_update_file("file2.txt", "beta")
    client.add_or_update_file("file3.txt", "gamma")
    print("")

    # 2. Verify all files are valid
    assert client.verify_file("file1.txt")
    assert client.verify_file("file2.txt")
    assert client.verify_file("file3.txt")
    print("Client: Initial files verified successfully.\\n")

    # 3. Update an existing file
    client.add_or_update_file("file2.txt", "delta")
    print("")

    # 4. Verify all files again. All should be valid.
    assert client.verify_file("file1.txt")
    assert client.verify_file("file2.txt") # The updated file
    assert client.verify_file("file3.txt")
    print("Client: Files verified successfully after update.\\n")

    # 5. Simulate data corruption on the client side
    print("--- Simulating data mismatch ---")
    client.local_files["file2.txt"] = "beta" # Revert to old content locally
    is_valid = client.verify_file("file2.txt")
    print(f"Client: Verification of mismatched 'file2.txt' is {is_valid}")
    assert not is_valid
    print("Client: Mismatch correctly detected.")

if __name__ == '__main__':
    test_final_system()
