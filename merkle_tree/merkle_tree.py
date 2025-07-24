import hashlib

class MerkleTree:
    """
    A simple Merkle Tree implementation.
    """

    def __init__(self, data_list):
        """
        Initializes the Merkle Tree with a list of data.
        :param data_list: A list of data blocks (e.g., transactions).
        """
        self.data_list = data_list
        self.levels = None
        self.root = self._build_tree(self.data_list)

    @staticmethod
    def _hash(data):
        """
        Hashes data using SHA-256.
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _build_tree(self, data_list):
        """
        Builds the Merkle Tree and returns the root.
        """
        if not data_list:
            self.levels = []
            return None

        self.levels = []
        nodes = [self._hash(str(data)) for data in data_list]
        self.levels.append(nodes)

        while len(nodes) > 1:
            if len(nodes) % 2 != 0:
                nodes.append(nodes[-1])

            next_level_nodes = []
            for i in range(0, len(nodes), 2):
                combined_hash = self._hash(nodes[i] + nodes[i+1])
                next_level_nodes.append(combined_hash)

            nodes = next_level_nodes
            self.levels.append(nodes)

        return nodes[0] if nodes else None

    def get_root(self):
        """
        Returns the Merkle root of the tree.
        """
        return self.root

    def get_proof(self, data):
        """
        Generates a proof for a given piece of data.
        The proof is a list of tuples (hash, position) where position is 'L' or 'R'.
        """
        data_hash = self._hash(str(data))

        try:
            index = self.levels[0].index(data_hash)
        except ValueError:
            return None # Data not in the tree

        proof = []
        for level in self.levels[:-1]:
            is_right_node = index % 2
            sibling_index = index - 1 if is_right_node else index + 1

            if sibling_index < len(level):
                sibling_hash = level[sibling_index]
                if is_right_node:
                    proof.append((sibling_hash, 'L'))
                else:
                    proof.append((sibling_hash, 'R'))

            index //= 2

        return proof

    @staticmethod
    def verify_proof(proof, data, root):
        """
        Verifies a proof for a given piece of data and root.
        """
        computed_hash = MerkleTree._hash(str(data))

        for p_hash, position in proof:
            if position == 'L':
                computed_hash = MerkleTree._hash(p_hash + computed_hash)
            else:
                computed_hash = MerkleTree._hash(computed_hash + p_hash)

        return computed_hash == root

if __name__ == '__main__':
    # Example usage:
    # 1. A list of transactions
    transactions = ["tx1", "tx2", "tx3", "tx4", "tx5"]

    # 2. Create a Merkle Tree from the transactions
    merkle_tree = MerkleTree(transactions)

    # 3. Get the Merkle root
    merkle_root = merkle_tree.get_root()

    # 4. Print the root
    print(f"Transactions: {transactions}")
    print(f"Merkle Root: {merkle_root}")

    # --- Proof of Inclusion Example ---
    # 1. Get a proof for a specific transaction
    tx_to_prove = "tx3"
    proof = merkle_tree.get_proof(tx_to_prove)
    print(f"\nProof for '{tx_to_prove}': {proof}")

    # 2. Verify the proof
    is_valid = MerkleTree.verify_proof(proof, tx_to_prove, merkle_root)
    print(f"Is '{tx_to_prove}' included in the tree? {is_valid}")

    # --- Tampering Example ---
    # 1. Try to verify a transaction that is not in the tree
    fake_tx = "tx6"
    is_valid_fake = MerkleTree.verify_proof(proof, fake_tx, merkle_root)
    print(f"Is '{fake_tx}' included in the tree? {is_valid_fake}")

    # Example with a different number of transactions
    transactions_2 = ["a", "b", "c"]
    merkle_tree_2 = MerkleTree(transactions_2)
    merkle_root_2 = merkle_tree_2.get_root()
    print(f"\nTransactions: {transactions_2}")
    print(f"Merkle Root: {merkle_root_2}")
