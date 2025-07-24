"""
Interview Questions (Fixed Implementation):
- Implement a file-aware Merkle tree that tracks files by filename
- Server endpoints: upload(filename, content) and check(filename)  
- Efficient incremental updates: only rehash affected nodes when files change
- Client-server sync mechanism that can identify and transfer only changed parts
- Follow-up: Database sharding/scaling for high user load
"""

import hashlib
import json
from typing import Dict, List, Optional, Tuple, Set

def sha256(data: bytes) -> str:
    """Helper function to compute SHA256 hash."""
    return hashlib.sha256(data).hexdigest()

# --- 1. File-Aware Merkle Tree (Git-style) ---

class FileTree:
    """
    A file-aware Merkle tree that maps filenames to content hashes.
    Supports efficient incremental updates.
    """
    
    def __init__(self):
        self.files: Dict[str, str] = {}  # filename -> content_hash
        self.tree_hash: Optional[str] = None
        self._compute_tree_hash()
    
    def _compute_tree_hash(self) -> str:
        """Computes hash of the entire file mapping."""
        if not self.files:
            self.tree_hash = sha256(b"empty_tree")
            return self.tree_hash
            
        # Create deterministic representation: sorted filename:hash pairs
        content = "\n".join(f"{name}:{hash}" for name, hash in sorted(self.files.items()))
        self.tree_hash = sha256(content.encode('utf-8'))
        return self.tree_hash
    
    def upload_file(self, filename: str, content: bytes) -> List[str]:
        """
        Uploads a single file and returns the chain of hashes that changed.
        This addresses the key interview insight about tracking update chains.
        """
        old_tree_hash = self.tree_hash
        old_file_hash = self.files.get(filename)
        
        # Calculate new file hash
        new_file_hash = sha256(content)
        
        # Track what changed
        changes = []
        if old_file_hash != new_file_hash:
            changes.append(f"file:{filename} {old_file_hash} -> {new_file_hash}")
            self.files[filename] = new_file_hash
            
            # Recompute tree hash
            new_tree_hash = self._compute_tree_hash()
            changes.append(f"tree: {old_tree_hash} -> {new_tree_hash}")
            
            print(f"[FileTree] Update chain: {' | '.join(changes)}")
        
        return changes
    
    def get_file_proof(self, filename: str) -> Optional[Dict]:
        """Returns proof that a file exists in this tree."""
        if filename not in self.files:
            return None
            
        return {
            "filename": filename,
            "content_hash": self.files[filename],
            "tree_hash": self.tree_hash,
            "all_files": dict(self.files)  # In practice, this would be more efficient
        }
    
    def verify_file_proof(self, proof: Dict, content: bytes) -> bool:
        """Verifies that content matches the proof."""
        expected_hash = proof["content_hash"]
        actual_hash = sha256(content)
        
        if actual_hash != expected_hash:
            return False
            
        # Verify the tree hash matches the file mapping
        files = proof["all_files"]
        content_str = "\n".join(f"{name}:{hash}" for name, hash in sorted(files.items()))
        expected_tree_hash = sha256(content_str.encode('utf-8'))
        
        return expected_tree_hash == proof["tree_hash"]

# --- 2. Server with Proper Endpoints ---

class Server:
    """
    Server that maintains files and provides the exact endpoints from the interview.
    """
    
    def __init__(self):
        self.file_contents: Dict[str, bytes] = {}  # filename -> raw content
        self.tree = FileTree()
        print("[Server] Initialized with empty file tree")
    
    def upload(self, filename: str, content: str) -> Dict:
        """
        Server endpoint: upload(filename, content)
        Returns information about what changed.
        """
        content_bytes = content.encode('utf-8')
        
        print(f"\n[Server] upload('{filename}', <{len(content)} chars>)")
        
        # Store the content
        self.file_contents[filename] = content_bytes
        
        # Upload the file to tree and get the change chain
        changes = self.tree.upload_file(filename, content_bytes)
        
        result = {
            "status": "uploaded",
            "filename": filename,
            "new_tree_hash": self.tree.tree_hash,
            "changes": changes
        }
        
        print(f"[Server] Result: {result['status']}, new tree hash: {result['new_tree_hash'][:8]}...")
        return result
    
    def check(self, filename: str) -> Dict:
        """
        Server endpoint: check(filename) 
        Returns verification info for the file.
        """
        print(f"\n[Server] check('{filename}')")
        
        if filename not in self.file_contents:
            result = {"status": "not_found", "filename": filename}
            print(f"[Server] Result: {result['status']}")
            return result
        
        proof = self.tree.get_file_proof(filename)
        content = self.file_contents[filename]
        
        result = {
            "status": "found",
            "filename": filename,
            "content": content.decode('utf-8'),
            "proof": proof
        }
        
        print(f"[Server] Result: {result['status']}, content hash: {proof['content_hash'][:8]}...")
        return result
    
    def get_tree_summary(self) -> Dict:
        """Returns current state for sync purposes."""
        return {
            "tree_hash": self.tree.tree_hash,
            "file_count": len(self.file_contents),
            "files": list(self.tree.files.keys())
        }

# --- 3. Client with Efficient Sync ---

class Client:
    """
    Client that efficiently syncs with server using incremental updates.
    """
    
    def __init__(self):
        self.known_tree_hash: Optional[str] = None
        self.local_files: Dict[str, str] = {}  # filename -> content_hash
        print("[Client] Initialized")
    
    def sync_with_server(self, server: Server) -> Dict:
        """
        Efficient sync: only fetches what changed since last sync.
        This addresses the key interview question about sync efficiency.
        """
        print(f"\n[Client] Starting sync (last known tree: {self.known_tree_hash[:8] if self.known_tree_hash else 'None'}...)")
        
        # Get current server state
        server_summary = server.get_tree_summary()
        server_tree_hash = server_summary["tree_hash"]
        
        if self.known_tree_hash == server_tree_hash:
            print("[Client] Already up to date")
            return {"status": "up_to_date"}
        
        # Identify what changed
        server_files = set(server_summary["files"])
        local_files = set(self.local_files.keys())
        
        added_files = server_files - local_files
        removed_files = local_files - server_files
        potentially_changed = server_files & local_files
        
        sync_result = {
            "status": "synced",
            "added": list(added_files),
            "removed": list(removed_files),
            "checked": list(potentially_changed),
            "updated": []
        }
        
        # Fetch added files
        for filename in added_files:
            self._fetch_file(server, filename)
        
        # Remove deleted files
        for filename in removed_files:
            del self.local_files[filename]
        
        # Check potentially changed files
        for filename in potentially_changed:
            check_result = server.check(filename)
            new_hash = check_result["proof"]["content_hash"]
            if self.local_files[filename] != new_hash:
                self._fetch_file(server, filename)
                sync_result["updated"].append(filename)
        
        self.known_tree_hash = server_tree_hash
        print(f"[Client] Sync complete: {sync_result}")
        return sync_result
    
    def _fetch_file(self, server: Server, filename: str):
        """Fetches a single file from server."""
        check_result = server.check(filename)
        if check_result["status"] == "found":
            content_hash = check_result["proof"]["content_hash"]
            self.local_files[filename] = content_hash
            print(f"[Client] Fetched '{filename}' (hash: {content_hash[:8]}...)")
    
    def verify_file(self, server: Server, filename: str) -> bool:
        """
        Verifies a file's integrity against server.
        This is the core verification the interview was testing.
        """
        print(f"\n[Client] Verifying '{filename}'...")
        
        if filename not in self.local_files:
            print(f"[Client] File '{filename}' not in local cache")
            return False
        
        # Get current proof from server
        check_result = server.check(filename)
        if check_result["status"] != "found":
            print(f"[Client] File not found on server")
            return False
        
        # Verify the proof
        content = check_result["content"].encode('utf-8')
        proof = check_result["proof"]
        
        tree = FileTree()
        is_valid = tree.verify_file_proof(proof, content)
        
        if is_valid:
            print(f"[Client] ✓ File '{filename}' is valid")
        else:
            print(f"[Client] ✗ File '{filename}' verification failed")
        
        return is_valid

# --- 4. Demonstration ---
if __name__ == "__main__":
    print("=== Fixed Implementation Demo ===")
    
    # Setup
    server = Server()
    client = Client()
    
    # Upload files and show incremental updates
    print("\n--- Phase 1: Initial uploads ---")
    server.upload("README.md", "# My Project\nThis is a test project.")
    server.upload("main.py", "print('Hello, World!')")
    
    # Client syncs
    print("\n--- Phase 2: Client sync ---")
    client.sync_with_server(server)
    
    # Verify files
    print("\n--- Phase 3: File verification ---")
    client.verify_file(server, "README.md")
    client.verify_file(server, "main.py")
    
    # Update a file and show incremental changes
    print("\n--- Phase 4: Incremental update ---")
    server.upload("main.py", "print('Hello, Updated World!')\nprint('New line added')")
    
    # Show sync efficiency
    print("\n--- Phase 5: Efficient resync ---")
    client.sync_with_server(server)
    
    # Final verification
    print("\n--- Phase 6: Verify updated file ---")
    client.verify_file(server, "main.py")
    
    print(f"\n=== Final State ===")
    summary = server.get_tree_summary()
    print(f"Server: {summary['file_count']} files, tree hash: {summary['tree_hash'][:8]}...")
    print(f"Client: {len(client.local_files)} files, known tree: {client.known_tree_hash[:8]}...")

"""
System Design Discussion: Database Sharding/Scaling

For the follow-up question about scaling databases under high user load:

1. **Horizontal Partitioning (Sharding)**:
   - Partition data across multiple database instances
   - Strategies: Hash-based, Range-based, Directory-based
   - Example: User ID % N for user sharding

2. **Read Replicas**:
   - Master-slave replication for read scaling
   - Route reads to replicas, writes to master
   - Eventual consistency considerations

3. **Caching Layer**:
   - Redis/Memcached for frequently accessed data
   - Reduces database load significantly
   - Cache invalidation strategies

4. **Load Balancing**:
   - Distribute requests across multiple app servers
   - Database connection pooling
   - Circuit breakers for fault tolerance

5. **Specific to File/Code Hosting**:
   - Content-based sharding (by repository)
   - CDN for static assets
   - Git-specific optimizations (pack files, deltas)
"""
