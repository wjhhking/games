
import unittest
from merkle_tree import MerkleTree, hash256

class TestMerkleTree(unittest.TestCase):

    def test_empty_tree(self):
        mt = MerkleTree([])
        self.assertIsNone(mt.root)

    def test_single_leaf(self):
        data = [b'leaf1']
        mt = MerkleTree(data)
        self.assertEqual(mt.root, hash256(data[0]))

    def test_even_leaves(self):
        data = [b'leaf1', b'leaf2', b'leaf3', b'leaf4']
        mt = MerkleTree(data)
        
        h1 = hash256(data[0])
        h2 = hash256(data[1])
        h3 = hash256(data[2])
        h4 = hash256(data[3])

        h12 = hash256((h1 + h2).encode())
        h34 = hash256((h3 + h4).encode())

        root = hash256((h12 + h34).encode())
        self.assertEqual(mt.root, root)

    def test_odd_leaves(self):
        data = [b'leaf1', b'leaf2', b'leaf3']
        mt = MerkleTree(data)

        h1 = hash256(data[0])
        h2 = hash256(data[1])
        h3 = hash256(data[2])

        h12 = hash256((h1 + h2).encode())
        h33 = hash256((h3 + h3).encode()) # Duplicated last leaf

        root = hash256((h12 + h33).encode())
        self.assertEqual(mt.root, root)

    def test_get_and_validate_proof_even(self):
        data = [b'leaf1', b'leaf2', b'leaf3', b'leaf4']
        mt = MerkleTree(data)
        
        target_data = b'leaf3'
        proof = mt.get_proof(target_data)
        
        self.assertIsNotNone(proof)
        self.assertTrue(mt.validate_proof(target_data, proof))

    def test_get_and_validate_proof_odd(self):
        data = [b'leaf1', b'leaf2', b'leaf3']
        mt = MerkleTree(data)

        target_data = b'leaf1'
        proof = mt.get_proof(target_data)

        self.assertIsNotNone(proof)
        self.assertTrue(mt.validate_proof(target_data, proof))

    def test_invalid_proof_wrong_data(self):
        data = [b'a', b'b', b'c', b'd']
        mt = MerkleTree(data)
        
        target_data = b'a'
        proof = mt.get_proof(target_data)
        
        self.assertIsNotNone(proof)
        self.assertFalse(mt.validate_proof(b'x', proof))

    def test_invalid_proof_modified(self):
        data = [b'a', b'b', b'c', b'd']
        mt = MerkleTree(data)
        
        target_data = b'b'
        proof = mt.get_proof(target_data)
        self.assertIsNotNone(proof)

        # Tamper with the proof
        proof[0] = (hash256(b'z'), proof[0][1])
        self.assertFalse(mt.validate_proof(target_data, proof))

    def test_proof_for_nonexistent_data(self):
        data = [b'one', b'two', b'three']
        mt = MerkleTree(data)
        
        proof = mt.get_proof(b'four')
        self.assertIsNone(proof)

    def test_duplicate_leaves(self):
        data = [b'A', b'B', b'A']
        mt = MerkleTree(data)

        # Proof should still work for the first 'A'
        proof1 = mt.get_proof(b'A')
        self.assertIsNotNone(proof1)
        self.assertTrue(mt.validate_proof(b'A', proof1))


if __name__ == '__main__':
    unittest.main()

