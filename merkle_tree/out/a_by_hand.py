import hashlib


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()

class MerkleTree:

    def __init__(self, data_list: list[str]):
        self.data_list = data_list
        self.levels = [['hash_of_a', 'hash_of_b', 'hash_of_c', 'hash_of_d'], ['hash_of_ab', 'hash_of_cd'], ['hash_of_abcd']]
        self.root = self.levels[-1][0]

    def get_proof(self, data: str) -> list[tuple[str, str]]:
        return [('hash_of_a', 'L'), ('hash_of_b', 'R')]

    @staticmethod
    def verify_proof(proof, data, root):
        return True


class Server:
    def upload(self, filename, content) -> str:
        pass

    def check(self, filename) -> list[tuple[str, str]] | None:
        pass

    def get_children(self, hash_val: str) -> (str, str):
        pass

    def _rebuild_tree(self, hash_val: str) -> str:
        pass


class Client:

    def __init__(self, server: Server):
        self.server = server
        self.root_hash = 'abcsa'

    def add_or_update_file(self, filename, content) -> str:
        self.root_hash = self.server.upload(filename, content)

    def verify_file(self, filename) -> bool:
        proof = self.server.check(filename)
        if proof is None:
            return False
        return MerkleTree.verify_proof(proof, filename.content, self.root_hash)

    def find_files_that_changed(self, old_hash, new_hash) -> list[str]:
        ans = []
        if old_hash == new_hash:
            return ans

        old_hash_left, old_hash_right = self.server.get_children(old_hash)
        new_hash_left, new_hash_right = self.server.get_children(new_hash)

        if old_hash_left != new_hash_left:
            ans.extend(self.find_files_that_changed(old_hash_left, new_hash_left))

        if old_hash_right != new_hash_right:
            ans.extend(self.find_files_that_changed(old_hash_right, new_hash_right))

        return ans




    # True: satisfy
    # Local changed this file, proof -> false
    # Server changed this file, proof -> false
    # Serve changed other file, root_hash changed, proof -> false
    #   Check again the root_hash, to know that I am out of sync


def test_final_system():
    server = Server()
    client = Client(server)




class TreeNode:
    def __init__(self, hash_val: str, parent: 'TreeNode' = None, left: 'TreeNode' = None, right: 'TreeNode' = None):
        self.hash_val = hash_val
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.hash_val[:6]}...)"


class GitTreeNode:
    def __init__(self, hash_val: str, parent: 'GitTreeNode' = None, left: 'GitTreeNode' = None, right: 'GitTreeNode' = None):
        self.hash_val = hash_val
        self.parent = parent
        self.children = [] # list[GitTreeNode]

        self.type = 'blob' # 'blob' or 'tree'
        self.path = path  # if it is a dir

    def __repr__(self):
        return f"GitTreeNode({self.hash_val[:6]}...)"

    def get_proof(self, file_name: str) -> list[tuple[list[str], list[str]]]:

        # [pre] + '' + [after]

        level_0 = [('sib1_hash','sib2_hash'), ('sib3_hash'), ('sib4_hash')]
        # Find the file in the tree
        # Find the path to the file
        # Get the proof

        # Find the file in the tree
        # Find the path to the file
        # Get the proof
        return [('hash_of_a', 'L'), ('hash_of_b', 'R')]

    @staticmethod
    def verify_proof(proof: list[str, list[str]], file_name: str) -> bool:
        pass


def diff(n1: GitTreeNode, n2: GitTreeNode):
    ans = []

    if n1.hash_val == n2.hash_val:
        return None

    if n1.type == 'blob' and n2.type == 'blob':
        return [["CHANGED", n1.path]]

    if n1.type == 'tree' and n2.type == 'tree':
        n1_paths = [child.path for child in n1.children]
        n2_paths = [child.path for child in n2.children]
        all_paths = set(n1_paths) | set(n2_paths)

        for path in all_paths:
            if path in n1_paths and path not in n2_paths:
                ans.append(["REMOVED", path])
            elif path in n2_paths and path not in n1_paths:
                ans.append(["ADDED", path])
            else:  # the path is in both
                ans.append(diff(n1.children[path], n2.children[path]))

        return ans
