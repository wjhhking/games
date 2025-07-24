import hashlib


# class MerkleTree:

#     def __init__(self, data_list):
#         self.data_list = data_list
#         self.levels = [[]]
#         self.root = self.levels[-1][0]

#     def get_proof(self, data):
#         return [('a', 'L'), ('b', 'R')]

#     def verify_proof(self, proof, root, data):
#         return True


def hash256(s: str):
    return hashlib.sha256(s.encode()).hexdigest()


class MerkleTree:

    def __init__(self, data_list):
        if not data_list:
            self.data = []
            self.levels = [[]]
            self.root = None
            return

        self.data = data_list

        data_hashes = [hash256(d) for d in data_list]

        self.levels = [data_hashes]

        while len(data_hashes) > 1:
            new_hashes = []
            if len(data_hashes) % 2 == 1:
                data_hashes.append(data_hashes[-1])
            for i in range(0, len(data_hashes), 2):
                new_hashes.append(hash256(data_hashes[i] + data_hashes[i+1]))
            self.levels.append(new_hashes)
            data_hashes = new_hashes

        self.root = data_hashes[0]


    def get_proof(self, data):
        try:
            data_index = self.levels[0].index(hash256(data))
        except ValueError:
            return []

        ans = []

        for level in self.levels[:-1]:
            position = 'L'
            hash_index = data_index - 1
            if data_index % 2 == 0:
                position = 'R'
                hash_index = data_index + 1

            ans.append((level[hash_index], position))
            data_index = data_index // 2

        return ans

    @staticmethod
    def verify_proof(proof, data, root):
        data_hash = hash256(data)

        for sibling_hash, position in proof:
            if position == 'L':
                data_hash = hash256(sibling_hash + data_hash)
            else:
                data_hash = hash256(data_hash + sibling_hash)

        return data_hash == root

def test_merkle_tree():
    data_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    merkle_tree = MerkleTree(data_list)
    print(merkle_tree.root)
    print(merkle_tree.get_proof('a'))
    print(merkle_tree.verify_proof(merkle_tree.get_proof('a'), 'a', merkle_tree.root))
    print(merkle_tree.verify_proof(merkle_tree.get_proof('a'), 'b', merkle_tree.root))

# The main execution block was moved from here to the end of the file.
# if __name__ == '__main__':
# ...

# Q2: Client-Server synchronization using Merkle Tree

class Server:
    """
    The Server maintains a collection of files and a single Merkle Tree
    representing the state of all files.
    """
    def __init__(self):
        self.files = {}  # Stores file content: {filename: content}
        self.file_order = []  # Maintain a consistent order for leaves
        self.merkle_tree = None
        self.root = None
        self._build_tree()

    def _build_tree(self):
        """Builds/rebuilds the Merkle tree from the current file contents."""
        if not self.file_order:
            # Handle case with no files
            self.merkle_tree = MerkleTree([])
        else:
            all_content = [self.files[fname] for fname in self.file_order]
            self.merkle_tree = MerkleTree(all_content)
        self.root = self.merkle_tree.root if self.merkle_tree else None

    def upload(self, filename: str, content: str):
        """
        Uploads a file. If the file is new, it's added. If it exists,
        it's updated. The Merkle tree is rebuilt to reflect the change.
        """
        if filename not in self.files:
            self.file_order.append(filename)
        self.files[filename] = content

        # For a real system, you would update the tree more efficiently
        # instead of a full rebuild. But for an interview, this is a solid approach.
        self._build_tree()
        print(f"Server: Uploaded '{filename}'. New root: {self.root}")


    def check(self, filename: str) -> list[tuple[str, str]] | None:
        """
        Returns the Merkle proof for a given file's content.
        Returns None if the file doesn't exist.
        """
        if filename not in self.files or not self.merkle_tree:
            return None

        content = self.files[filename]
        return self.merkle_tree.get_proof(content)


class Client:
    """
    The Client interacts with the server to upload and verify files.
    """
    def __init__(self, server: Server):
        self.server = server
        # In a real scenario, the client might cache the files it cares about.
        self.local_files = {}

    def add_file(self, filename: str, content: str):
        """Adds a file to local cache and uploads to the server."""
        self.local_files[filename] = content
        self.server.upload(filename, content)

    def verify_file(self, filename: str) -> bool:
        """
        Verifies a local file against the server's Merkle Tree.
        """
        if filename not in self.local_files:
            print(f"Client: File '{filename}' not found locally.")
            return False

        content = self.local_files[filename]

        # 1. Get the proof from the server for this file.
        proof = self.server.check(filename)
        if proof is None:
            # This can happen if the server doesn't have the file.
            print(f"Client: Server has no record of '{filename}'.")
            return False

        # 2. Get the server's current master root hash.
        server_root = self.server.root
        if server_root is None:
            print("Client: Server has no root hash.")
            return False

        # 3. Perform verification using the static method.
        is_valid = MerkleTree.verify_proof(proof, content, server_root)
        print(f"Client: Verifying '{filename}'. Valid: {is_valid}")
        return is_valid


def test_client_server_sync():
    """
    A test scenario to demonstrate the client-server synchronization.
    """
    # 1. Setup Client and Server
    server = Server()
    client = Client(server)
    print(f"Initial server root: {server.root}\n")

    # 2. Client uploads two files
    client.add_file("file1.txt", "Hello Merkle!")
    client.add_file("file2.txt", "Second file.")
    print("")

    # 3. Client verifies its files. Both should be valid.
    assert client.verify_file("file1.txt") is True
    assert client.verify_file("file2.txt") is True
    print("")

    # 4. Another client (or the same one) updates a file.
    print("--- Simulating file update ---")
    client.add_file("file1.txt", "Hello Merkle Tree!") # Content has changed
    print("")

    # 5. The client verifies again. file1.txt is still valid because
    # the client has the updated content and the server has the new root.
    assert client.verify_file("file1.txt") is True
    assert client.verify_file("file2.txt") is True # Unchanged file is also valid.
    print("")

    # 6. Let's simulate a data corruption or mismatch scenario.
    print("--- Simulating data mismatch ---")
    # Server has the "updated" content for file1.txt.
    # Let's pretend the client has an old version of the content.
    client.local_files["file1.txt"] = "Hello Merkle!" # Old content

    # Verification should now fail for file1.txt because the client's
    # local content no longer matches what's on the server.
    assert client.verify_file("file1.txt") is False

if __name__ == '__main__':
    # The original test for the MerkleTree class itself
    print("--- Testing MerkleTree class standalone ---")
    test_merkle_tree()
    print("\n--- Testing Client-Server interaction ---")
    test_client_server_sync()


