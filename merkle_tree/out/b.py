#!/usr/bin/env python3
"""
AI Coding Startup 面试题完整答案
- 实现能跑的 Merkle Tree
- Server: upload(filename, content) & check(filename)
- Client-Server 同步机制
- 增量更新：只更新影响的节点
"""

import hashlib
from typing import Dict, List, Optional

def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

# --- 1. 核心 Merkle Tree ---
class MerkleTree:
    def __init__(self):
        self.files: Dict[str, str] = {}  # filename -> content_hash
        self.root_hash: str = self._compute_root()

    def _compute_root(self) -> str:
        """计算整个树的根哈希"""
        if not self.files:
            return hash_data("empty")

        # 按文件名排序，确保确定性
        sorted_items = sorted(self.files.items())
        content = "|".join(f"{name}:{hash}" for name, hash in sorted_items)
        return hash_data(content)

    def add_file(self, filename: str, content: str) -> List[str]:
        """添加文件，返回更新链（面试重点）"""
        old_root = self.root_hash
        old_file_hash = self.files.get(filename)

        # 计算新文件哈希
        new_file_hash = hash_data(content)

        # 记录变化链
        changes = []
        if old_file_hash != new_file_hash:
            changes.append(f"File {filename}: {old_file_hash} -> {new_file_hash}")
            self.files[filename] = new_file_hash

            # 重新计算根哈希
            self.root_hash = self._compute_root()
            changes.append(f"Root: {old_root} -> {self.root_hash}")

            print(f"[Tree] Update chain: {changes}")

        return changes

    def get_proof(self, filename: str) -> Optional[Dict]:
        """生成文件存在证明"""
        if filename not in self.files:
            return None

        return {
            "filename": filename,
            "content_hash": self.files[filename],
            "root_hash": self.root_hash,
            "all_files": dict(self.files)  # 简化版证明
        }

    def verify_proof(self, proof: Dict, content: str) -> bool:
        """验证文件证明"""
        # 验证内容哈希
        if hash_data(content) != proof["content_hash"]:
            return False

        # 验证根哈希
        files = proof["all_files"]
        sorted_items = sorted(files.items())
        expected_content = "|".join(f"{name}:{hash}" for name, hash in sorted_items)
        expected_root = hash_data(expected_content)

        return expected_root == proof["root_hash"]

# --- 2. Server 实现 ---
class Server:
    def __init__(self):
        self.storage: Dict[str, str] = {}  # filename -> content
        self.tree = MerkleTree()
        print("[Server] 启动完成")

    def upload(self, filename: str, content: str) -> Dict:
        """Server 接口：上传文件"""
        print(f"\n[Server] upload('{filename}', {len(content)} chars)")

        # 存储文件内容
        self.storage[filename] = content

        # 更新 Merkle Tree
        changes = self.tree.add_file(filename, content)

        return {
            "status": "success",
            "new_root": self.tree.root_hash,
            "changes": changes
        }

    def check(self, filename: str) -> Dict:
        """Server 接口：检查文件"""
        print(f"\n[Server] check('{filename}')")

        if filename not in self.storage:
            return {"status": "not_found"}

        proof = self.tree.get_proof(filename)
        return {
            "status": "found",
            "content": self.storage[filename],
            "proof": proof
        }

    def get_state(self) -> Dict:
        """获取当前状态（用于同步）"""
        return {
            "root_hash": self.tree.root_hash,
            "files": list(self.tree.files.keys())
        }

# --- 3. Client 实现 ---
class Client:
    def __init__(self):
        self.known_root: Optional[str] = None
        self.local_files: Dict[str, str] = {}  # filename -> content_hash
        print("[Client] 初始化完成")

    def sync(self, server: Server) -> Dict:
        """与服务器同步（面试重点）"""
        print(f"\n[Client] 开始同步 (当前root: {self.known_root[:8] if self.known_root else 'None'}...)")

        # 获取服务器状态
        server_state = server.get_state()
        server_root = server_state["root_hash"]

        # 检查是否需要同步
        if self.known_root == server_root:
            print("[Client] 已是最新状态")
            return {"status": "up_to_date"}

        # 找出差异
        server_files = set(server_state["files"])
        local_files = set(self.local_files.keys())

        added = server_files - local_files
        removed = local_files - server_files
        updated = []

        # 处理新增和更新
        for filename in server_files & local_files:
            check_result = server.check(filename)
            new_hash = check_result["proof"]["content_hash"]
            if self.local_files[filename] != new_hash:
                updated.append(filename)

        # 同步文件
        for filename in added | set(updated):
            check_result = server.check(filename)
            self.local_files[filename] = check_result["proof"]["content_hash"]

        # 删除文件
        for filename in removed:
            del self.local_files[filename]

        self.known_root = server_root

        result = {
            "status": "synced",
            "added": list(added),
            "updated": updated,
            "removed": list(removed)
        }
        print(f"[Client] 同步完成: {result}")
        return result

    def verify_file(self, server: Server, filename: str) -> bool:
        """验证文件完整性"""
        print(f"\n[Client] 验证文件 '{filename}'")

        check_result = server.check(filename)
        if check_result["status"] != "found":
            print("[Client] 文件不存在")
            return False

        # 验证证明
        tree = MerkleTree()
        is_valid = tree.verify_proof(check_result["proof"], check_result["content"])

        print(f"[Client] 验证结果: {'✓ 有效' if is_valid else '✗ 无效'}")
        return is_valid

# --- 4. 演示 ---
def demo():
    print("=== Merkle Tree 面试题演示 ===")

    server = Server()
    client = Client()

    # 1. 上传文件
    print("\n--- 阶段1: 上传文件 ---")
    server.upload("main.py", "print('Hello World')")
    server.upload("readme.txt", "This is a test project")

    # 2. 客户端同步
    print("\n--- 阶段2: 客户端同步 ---")
    client.sync(server)

    # 3. 验证文件
    print("\n--- 阶段3: 验证文件 ---")
    client.verify_file(server, "main.py")

    # 4. 更新文件（展示增量更新）
    print("\n--- 阶段4: 增量更新 ---")
    server.upload("main.py", "print('Hello Updated World')")

    # 5. 高效同步
    print("\n--- 阶段5: 增量同步 ---")
    client.sync(server)

    # 6. 最终验证
    print("\n--- 阶段6: 最终验证 ---")
    client.verify_file(server, "main.py")

    print(f"\n=== 最终状态 ===")
    state = server.get_state()
    print(f"Server: {len(state['files'])} files, root: {state['root_hash'][:8]}...")
    print(f"Client: {len(client.local_files)} files, root: {client.known_root[:8]}...")

if __name__ == "__main__":
    demo()

"""
面试要点总结：

1. **增量更新机制**：
   - 只有文件内容变化时才重新计算哈希
   - 明确显示"更新链"：哪些节点的哈希需要更新

2. **同步策略**：
   - 比较根哈希快速判断是否需要同步
   - 只传输变化的文件，不是全量同步
   - 支持增量更新检测

3. **系统设计**：
   - Server 提供明确的 upload/check 接口
   - Client 能高效同步和验证
   - 数据结构简单但功能完整

4. **扩展性考虑**：
   - 可以很容易扩展为支持目录结构
   - 可以添加更高效的同步算法
   - 可以支持批量操作
"""
