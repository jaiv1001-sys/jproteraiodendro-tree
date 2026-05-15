import math
import time
from collections import defaultdict, OrderedDict


class JDTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value

        # Adaptive intelligence
        self.access_count = 0
        self.priority = 0
        self.last_access = time.time()

        # BST links
        self.left = None
        self.right = None

        # Graph-routing shortcuts
        self.shortcuts = {}

    def __repr__(self):
        return f"[{self.key}:P{self.priority}]"


class JproteraiodendroTree:
    def __init__(
        self,
        decay_factor=0.95,
        rotation_threshold=5,
        max_hot_cache_size=128,
        max_shortcuts_per_node=8,
        shortcut_probability_threshold=0.35,
        rebuild_cooldown=5,
    ):
        self.root = None

        # Thread safety
        import threading
        self.lock = threading.RLock()

        # O(1) node lookup
        self.node_map = {}

        # Predictive access tracking
        self.transition_map = defaultdict(lambda: defaultdict(int))

        # Hot node cache
        self.hot_cache = OrderedDict()

        self.last_accessed_node = None

        # Safety limits
        self.max_hot_cache_size = max_hot_cache_size
        self.max_shortcuts_per_node = max_shortcuts_per_node
        self.shortcut_probability_threshold = shortcut_probability_threshold

        # Rebuild control
        self.last_rebuild_time = 0
        self.rebuild_cooldown = rebuild_cooldown

        # Metrics
        self.metrics = {
            "searches": 0,
            "cache_hits": 0,
            "shortcut_hits": 0,
            "rebuilds": 0,
            "failed_searches": 0,
        }

        self.decay_factor = decay_factor
        self.rotation_threshold = rotation_threshold

    # ------------------------------------------------------------
    # PRIORITY SYSTEM
    # ------------------------------------------------------------

    def _calculate_priority(self, access_count):
        return int(math.log2(access_count + 1) * 10)

    def _apply_decay(self, node):
        """
        Priority decay based on inactivity.
        Older hot nodes cool down automatically.
        """
        current_time = time.time()
        elapsed = current_time - node.last_access

        # Simple decay model
        decay_multiplier = self.decay_factor ** elapsed

        node.access_count *= decay_multiplier
        node.priority = self._calculate_priority(node.access_count)

    # ------------------------------------------------------------
    # INSERTION
    # ------------------------------------------------------------

    def insert(self, key, value):
        with self.lock:
            new_node = JDTNode(key, value)
        self.node_map[key] = new_node

        if not self.root:
            self.root = new_node
        else:
            self.root = self._insert_recursive(self.root, new_node)

        print(f"Inserted: {key}")

    def _insert_recursive(self, root, node):
        if root is None:
            return node

        if node.key < root.key:
            root.left = self._insert_recursive(root.left, node)
        else:
            root.right = self._insert_recursive(root.right, node)

        return root

    # ------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------

    def search(self, key):
        with self.lock:
            self.metrics["searches"] += 1
            start_time = time.perf_counter()

        # --------------------------------------------------------
        # 1. HOT CACHE FAST PATH
        # --------------------------------------------------------

        if key in self.hot_cache:
            node = self.hot_cache[key]

            # Validate cache entry
            if node.key not in self.node_map:
                del self.hot_cache[key]
                return None

            self.metrics["cache_hits"] += 1
            self._update_node(node)

            elapsed = time.perf_counter() - start_time
            print(f"[HOT CACHE HIT] {key} found in {elapsed:.8f}s")
            return node.value

        # --------------------------------------------------------
        # 2. GRAPH SHORTCUT ROUTING
        # --------------------------------------------------------

        previous_node = self.last_accessed_node
        if previous_node:
            shortcuts = previous_node.shortcuts
            if key in shortcuts:
                node = shortcuts[key]

                # Validate shortcut
                if node.key != key or node.key not in self.node_map:
                    del shortcuts[key]
                else:
                    self.metrics["shortcut_hits"] += 1
                    self._update_node(node)

                    elapsed = time.perf_counter() - start_time
                    print(f"[SHORTCUT HIT] {key} found in {elapsed:.8f}s")
                    return node.value

        # --------------------------------------------------------
        # 3. NORMAL BST SEARCH
        # --------------------------------------------------------

        node = self._search_iterative(key)

        if not node:
            self.metrics["failed_searches"] += 1
            print(f"Key {key} not found")
            return None

        # --------------------------------------------------------
        # 4. UPDATE INTELLIGENCE
        # --------------------------------------------------------

        self._update_node(node)

        # Learn transitions safely
        self._learn_shortcut(previous_node, node)

        # last_accessed_node updated later safely

        # Adaptive restructuring
        self._adaptive_rebalance(node)

        elapsed = time.perf_counter() - start_time

        print(
            f"Found {key} | Priority={node.priority} | Time={elapsed:.8f}s"
        )

        return node.value

    def _search_iterative(self, key):
        current = self.root

        while current:
            if current.key == key:
                return current

            if key < current.key:
                current = current.left
            else:
                current = current.right

        return None

    def _search_recursive(self, root, key):
        if root is None:
            return None

        if root.key == key:
            return root

        if key < root.key:
            return self._search_recursive(root.left, key)

        return self._search_recursive(root.right, key)

    # ------------------------------------------------------------
    # NODE UPDATE
    # ------------------------------------------------------------

    def _update_node(self, node):
        old_priority = node.priority

        self._apply_decay(node)

        node.access_count += 1
        node.priority = self._calculate_priority(node.access_count)
        node.last_access = time.time()

        # Maintain hot cache
        if node.priority >= 30:
            self.hot_cache[node.key] = node
            self.hot_cache.move_to_end(node.key)

            # Bounded cache
            while len(self.hot_cache) > self.max_hot_cache_size:
                self.hot_cache.popitem(last=False)

        # Store for predictive routing
        self.last_accessed_node = node

        return old_priority

    # ------------------------------------------------------------
    # GRAPH SHORTCUT LEARNING
    # ------------------------------------------------------------

    def _learn_shortcut(self, prev, current_node):
        if prev and prev != current_node:

            # Track transitions
            total_before = sum(self.transition_map[prev.key].values())
            self.transition_map[prev.key][current_node.key] += 1

            count = self.transition_map[prev.key][current_node.key]

            probability = count / max(total_before + 1, 1)

            # Create statistically meaningful shortcut
            if probability >= self.shortcut_probability_threshold:
                prev.shortcuts[current_node.key] = current_node

                # Bound shortcut growth
                if len(prev.shortcuts) > self.max_shortcuts_per_node:
                    weakest = min(
                        prev.shortcuts,
                        key=lambda k: self.transition_map[prev.key][k]
                    )
                    del prev.shortcuts[weakest]

    # ------------------------------------------------------------
    # ADAPTIVE REBALANCING
    # ------------------------------------------------------------

    def _adaptive_rebalance(self, node):
        # Only rebalance if node becomes significantly hot
        if node.priority >= self.rotation_threshold:
            self.root = self._splay(self.root, node.key)

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        # LEFT SIDE
        if key < root.key:
            if root.left is None:
                return root

            # Zig-Zig
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)

            # Zig-Zag
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)

                if root.left.right:
                    root.left = self._rotate_left(root.left)

            return self._rotate_right(root) if root.left else root

        # RIGHT SIDE
        else:
            if root.right is None:
                return root

            # Zag-Zag
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)

            # Zag-Zig
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)

                if root.right.left:
                    root.right = self._rotate_right(root.right)

            return self._rotate_left(root) if root.right else root

    # ------------------------------------------------------------
    # ROTATIONS
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # DISPLAY
    # ------------------------------------------------------------

    def display_structure(self):
        print("\n===== TREE STRUCTURE =====")
        lines, *_ = self._display_aux(self.root)

        for line in lines:
            print(line)

    def _display_aux(self, node):
        if node is None:
            return [], 0, 0, 0

        label = f"{node.key}(P{node.priority})"

        if node.left is None and node.right is None:
            width = len(label)
            return [label], width, 1, width // 2

        # Only left child
        if node.right is None:
            lines, n, p, x = self._display_aux(node.left)
            u = len(label)

            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + label
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '

            shifted_lines = [line + u * ' ' for line in lines]

            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child
        if node.left is None:
            lines, n, p, x = self._display_aux(node.right)
            u = len(label)

            first_line = label + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '

            shifted_lines = [u * ' ' + line for line in lines]

            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children
        left, n, p, x = self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)

        u = len(label)

        first_line = (
            (x + 1) * ' '
            + (n - x - 1) * '_'
            + label
            + y * '_'
            + (m - y) * ' '
        )

        second_line = (
            x * ' '
            + '/'
            + (n - x - 1 + u + y) * ' '
            + '\\'
            + (m - y - 1) * ' '
        )

        if p < q:
            left += [' ' * n] * (q - p)
        elif q < p:
            right += [' ' * m] * (p - q)

        zipped_lines = zip(left, right)
        lines = [
            first_line,
            second_line,
        ] + [a + u * ' ' + b for a, b in zipped_lines]

        return lines, n + m + u, max(p, q) + 2, n + u // 2

    # ------------------------------------------------------------
    # ANALYTICS
    # ------------------------------------------------------------

    def display_hot_cache(self):
        print("\n===== HOT CACHE =====")
        for k, v in self.hot_cache.items():
            print(f"{k} -> Priority {v.priority}")

    def validate_structure(self):
        """Production safety validation."""

        def validate_bst(node, low=float('-inf'), high=float('inf')):
            if not node:
                return True

            if not (low < node.key < high):
                return False

            return (
                validate_bst(node.left, low, node.key)
                and validate_bst(node.right, node.key, high)
            )

        valid = validate_bst(self.root)

        if valid:
            print("Structure validation passed")
        else:
            print("Structure corruption detected")

        return valid

    def display_metrics(self):
        print("\n===== METRICS =====")

        for k, v in self.metrics.items():
            print(f"{k}: {v}")

    def display_shortcuts(self):
        print("\n===== SHORTCUT ROUTING =====")

        for key, node in self.node_map.items():
            if node.shortcuts:
                print(f"{key} shortcuts -> {list(node.shortcuts.keys())}")

# ================================================================
# EXECUTION DEMO
# ================================================================

if __name__ == "__main__":
    jdt = JproteraiodendroTree()

    values = [50, 20, 80, 10, 30, 70, 90, 5, 15]

    print("\n===== INSERTING DATA =====")
    for v in values:
        jdt.insert(v, f"Value_{v}")

    jdt.display_structure()

    print("\n===== HOT NODE SIMULATION =====")

    for _ in range(10):
        jdt.search(10)

    print("\n===== ACCESS PATTERN TRAINING =====")

    for _ in range(5):
        jdt.search(10)
        jdt.search(70)

    jdt.display_structure()
    jdt.display_hot_cache()
    jdt.display_shortcuts()
    jdt.display_metrics()
    jdt.validate_structure()

    print("\n===== TESTING SHORTCUT =====")

    jdt.search(10)
    jdt.search(70)
