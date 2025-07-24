"""
Interview Questions:
- Implement a functional Merkle Tree from scratch.
- Verify the correctness of the tree and its proofs.
- Design a client-server sync mechanism using the Merkle Tree.
- The server has two endpoints: upload(filename, content) and check(filename).
- Follow-up: Discuss how to shard/scale a database for a rapidly growing user base.
"""

import hashlib

# --- 1. Merkle Tree Implementation ---

def sha256(data: bytes) -> str:
    """Helper function to compute SHA256 hash."""
    return hashlib.sha256(data).hexdigest()

class MerkleTree:
    """A simple Merkle Tree implementation."""
    def __init__(self, data_list: list[bytes]):
        if not data_list:
            self.root = None
            self.levels = []
            return

        # Create the first level of leaf nodes from the data
        leaves = sorted([sha256(d) for d in data_list])
        self.levels = [leaves]
        
        # Build the tree level by level
        while len(self.levels[-1]) > 1:
            self._build_next_level()

        self.root = self.levels[-1][0] if self.levels[-1] else None

    def _build_next_level(self):
        """Builds the next level of the tree from the current top level."""
        current_level = self.levels[-1]
        next_level = []
        
        # Ensure the level has an even number of nodes by duplicating the last one if needed
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])
            
        # Create parent nodes by hashing pairs of child nodes
        for i in range(0, len(current_level), 2):
            left_child, right_child = current_level[i], current_level[i+1]
            parent_hash = sha256((left_child + right_child).encode('utf-8'))
            next_level.append(parent_hash)
            
        self.levels.append(next_level)

    def get_proof(self, data: bytes) -> list[tuple[str, str]] | None:
        """
        Generates a Merkle proof for a piece of data.
        The proof is a list of (hash, position) tuples.
        """
        data_hash = sha256(data)
        
        try:
            # Find the index of the hash in the leaf level
            idx = self.levels[0].index(data_hash)
        except ValueError:
            # Data is not in the tree
            return None

        proof = []
        for level in self.levels[:-1]:
            is_right_node = idx % 2 != 0
            sibling_idx = idx - 1 if is_right_node else idx + 1
            
            # Ensure the sibling index is within bounds
            if sibling_idx < len(level):
                sibling_hash = level[sibling_idx]
                position = 'L' if is_right_node else 'R' # Position of the sibling
                proof.append((sibling_hash, position))
            
            # Move up to the parent node for the next level
            idx //= 2
            
        return proof

    @staticmethod
    def validate_proof(proof: list[tuple[str, str]], data: bytes, root: str) -> bool:
        """Validates a Merkle proof against a root hash."""
        current_hash = sha256(data)
        
        for sibling_hash, position in proof:
            if position == 'L':
                # Sibling is on the left
                combined = sibling_hash + current_hash
            else:
                # Sibling is on the right
                combined = current_hash + sibling_hash
                
            current_hash = sha256(combined.encode('utf-8'))
            
        return current_hash == root

# --- 2. Client-Server Sync Solution ---

class Server:
    """Simulates a server that stores files and maintains a Merkle Tree."""
    def __init__(self):
        self.files = {} # {filename: content_bytes}
        self.merkle_tree = MerkleTree([])

    def upload(self, filename: str, content: str):
        """Handles file uploads, updates storage, and rebuilds the Merkle Tree."""
        print(f"[Server] Uploading '{filename}'...")
        self.files[filename] = content.encode('utf-8')
        
        # In a real system, you would update the tree more efficiently,
        # but rebuilding is simple and functionally correct for this example.
        self._rebuild_tree()
        print(f"[Server] New Merkle Root: {self.merkle_tree.root[:7]}...")

    def _rebuild_tree(self):
        """Rebuilds the Merkle Tree from the current file contents."""
        all_contents = list(self.files.values())
        self.merkle_tree = MerkleTree(all_contents)

    def get_merkle_root(self) -> str:
        """Provides the current root of the Merkle Tree."""
        return self.merkle_tree.root

    def get_file_and_proof(self, filename: str) -> tuple[bytes, list] | None:
        """Provides the content and Merkle proof for a given file."""
        if filename not in self.files:
            return None
        
        content = self.files[filename]
        proof = self.merkle_tree.get_proof(content)
        return (content, proof)

class Client:
    """Simulates a client that syncs with the server."""
    def __init__(self):
        self.local_root = None

    def sync_root(self, server: Server):
        """Gets the latest Merkle root from the server."""
        print("[Client] Syncing root with server...")
        self.local_root = server.get_merkle_root()
        print(f"[Client] Synced. New local root: {self.local_root[:7]}...")

    def check_file(self, filename: str, server: Server):
        """
        Checks the integrity of a file.
        It fetches the file and its proof from the server and validates it
        against its own local Merkle root.
        """
        print(f"\n[Client] Checking integrity of '{filename}'...")
        if not self.local_root:
            print("[Client] Error: No local root. Please sync first.")
            return

        response = server.get_file_and_proof(filename)
        if not response:
            print(f"[Client] Error: File '{filename}' not found on server.")
            return

        content, proof = response
        is_valid = MerkleTree.validate_proof(proof, content, self.local_root)
        
        if is_valid:
            print(f"[Client] SUCCESS: '{filename}' is valid and matches the local root.")
        else:
            print(f"[Client] FAILURE: '{filename}' is invalid or has been changed. Local root is outdated.")

# --- 3. Demonstration ---
if __name__ == "__main__":
    # Setup
    server = Server()
    client = Client()

    # Initial state: upload two files
    server.upload("file1.txt", "Hello, this is file 1.")
    server.upload("file2.txt", "This is the second file.")
    
    # Client's first sync
    client.sync_root(server)
    
    # Client checks a file, which should be valid
    client.check_file("file1.txt", server)
    
    # A change happens on the server
    print("\n--- A file is updated on the server ---")
    server.upload("file1.txt", "The content of file 1 has been updated.")
    
    # Client checks the updated file with its OLD root, which should FAIL
    client.check_file("file1.txt", server)
    
    # Client re-syncs to get the new root
    client.sync_root(server)
    
    # Client checks the file again with the NEW root, which should now SUCCEED
    client.check_file("file1.txt", server)


# --- 4. System Design Discussion ---
"""
System Design Question: How to shard/scale a database for high user load.

This is a classic system design problem. The key is to distribute data and load across multiple servers.

1.  Sharding Strategy (How to split the data):
    -   Key-Based/Hashed Sharding: Shard based on a hash of a user ID or some other entity ID.
        -   Pros: Distributes data evenly.
        -   Cons: Can be difficult to change the number of shards. Queries across shards are complex.
    -   Range-Based Sharding: Shard based on a range of values (e.g., User IDs 1-1000 on Shard A, 1001-2000 on Shard B).
        -   Pros: Simpler to implement and easier for range queries.
        -   Cons: Can lead to "hotspots" if data is not evenly distributed (e.g., new users all go to the last shard).
    -   Directory-Based Sharding: Use a lookup service (a "locator") to find which shard holds which data.
        -   Pros: Most flexible. Easy to rebalance and add new shards.
        -   Cons: The lookup service itself can become a bottleneck or single point of failure.

2.  Scaling Strategy:
    -   Vertical Scaling (Scale-Up): Increase the resources (CPU, RAM, SSD) of a single server.
        -   Pros: Simple to implement. No code changes needed.
        -   Cons: Expensive and has a physical limit.
    -   Horizontal Scaling (Scale-Out): Add more servers to the system (sharding is a form of this).
        -   Pros: Virtually limitless scalability and better cost-efficiency.
        -   Cons: Much more complex. Requires load balancers, service discovery, and careful data management.

3.  Other Considerations:
    -   Replication: Each shard should have replicas (copies) for fault tolerance and read scaling. A primary-replica setup is common.
    -   Consistency: How to handle data consistency across shards and replicas (e.g., eventual consistency vs. strong consistency).
    -   Load Balancing: A load balancer is needed in front of the application servers to distribute incoming requests.
    -   Caching: A distributed cache (like Redis or Memcached) is crucial to reduce database load by storing frequently accessed data in memory.
"""
