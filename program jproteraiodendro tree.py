import math
import time

class JDTNode:
    def __init__(self, key, value, priority=0):
        self.key = key
        self.value = value
        self.priority = priority
        self.access_count = 0
        self.left = None
        self.right = None
        # Graph-based routing: shortcuts to other related nodes
        self.shortcuts = [] 

    def __repr__(self):
        return f"[Key: {self.key}, Priority: {self.priority}]"

class JproteraiodendroTree:
    def __init__(self):
        self.root = None
        self.node_map = {} # For O(1) lookup in distributed/sharded simulation

    def _calculate_score(self, access_count):
        """Priority Assignment Algorithm (Simplified)"""
        return int(math.log2(access_count + 1) * 10)

    def insert(self, key, value):
        """Smart Insertion: Adds data and initializes position."""
        new_node = JDTNode(key, value)
        self.node_map[key] = new_node
        
        if not self.root:
            self.root = new_node
        else:
            self.root = self._insert_recursive(self.root, new_node)
        print(f"Inserted: {key}")

    def _insert_recursive(self, root, node):
        if not root:
            return node
        if node.key < root.key:
            root.left = self._insert_recursive(root.left, node)
        else:
            root.right = self._insert_recursive(root.right, node)
        return root

    def search(self, key):
        """Adaptive Search: Locates node and triggers Adaptive Positioning."""
        start_time = time.perf_counter()
        node, path = self._find_node_and_path(self.root, key, [])
        
        if node:
            node.access_count += 1
            old_priority = node.priority
            node.priority = self._calculate_score(node.access_count)
            
            # Trigger Dynamic Branching Algorithm if priority increases
            if node.priority > old_priority:
                self.root = self._rebalance_adaptive(self.root, key)
            
            end_time = time.perf_counter()
            print(f"Found {key} (Priority {node.priority}) in {end_time - start_time:.6f}s")
            return node.value
        
        print(f"Key {key} not found.")
        return None

    def _find_node_and_path(self, root, key, path):
        if not root or root.key == key:
            return root, path
        path.append(root)
        if key < root.key:
            return self._find_node_and_path(root.left, key, path)
        return self._find_node_and_path(root.right, key, path)

    def _rebalance_adaptive(self, root, key):
        """
        Adaptive Positioning: Moves 'hot nodes' closer to root.
        Uses a Splay-inspired rotation based on the priority score.
        """
        if not root or root.key == key:
            return root

        if key < root.key:
            if not root.left: return root
            if key < root.left.key: # Zig-Zig
                root.left.left = self._rebalance_adaptive(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key: # Zig-Zag
                root.left.right = self._rebalance_adaptive(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left else root
        else:
            if not root.right: return root
            if key > root.right.key: # Zag-Zag
                root.right.right = self._rebalance_adaptive(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key: # Zag-Zig
                root.right.left = self._rebalance_adaptive(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)
            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def display_structure(self):
        """Visualizes the tree hierarchy."""
        lines, *_ = self._display_aux(self.root)
        for line in lines:
            print(line)

    def _display_aux(self, node):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        if not node: return [], 0, 0, 0
        if not node.right and not node.left:
            line = f"{node.key}(P{node.priority})"
            return [line], len(line), 1, len(line) // 2
        
        left, n, p, x = self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)
        s = f"{node.key}(P{node.priority})"
        u = len(s)
        
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q: left += [n * ' '] * (q - p)
        elif q < p: right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

# --- Execution Simulation ---
jdt = JproteraiodendroTree()
data = [50, 20, 80, 10, 30, 70, 90]

print("--- Initializing JDT ---")
for d in data:
    jdt.insert(d, f"Value_{d}")

print("\n--- Tree Structure Before Adaptation ---")
jdt.display_structure()

print("\n--- Simulating High Traffic on Node '10' (Hot Node) ---")
for _ in range(5):
    jdt.search(10)

print("\n--- Tree Structure After Adaptation ---")
jdt.display_structure()