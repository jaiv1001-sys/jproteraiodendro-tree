# JproteraiodendroTree (JDT)

An adaptive self-optimizing tree data structure implemented in Python.

This project demonstrates a dynamic binary tree that reorganizes itself based on node access frequency using priority-based adaptive balancing inspired by splay trees.

---

## Features

- Smart node insertion
- Adaptive search optimization
- Dynamic priority scoring
- Self-balancing rotations
- Hot-node promotion
- Tree structure visualization
- Simulated distributed node mapping

---

## Project Structure

```bash
program.py
```

---

## How It Works

### Priority Assignment

Each node tracks:

- Access count
- Priority score

Priority is calculated using:

```python
score = log2(access_count + 1) * 10
```

Frequently accessed nodes gain higher priority and move closer to the root for faster future searches.

---

## Core Components

### `JDTNode`

Represents a node in the tree.

Attributes:

- `key`
- `value`
- `priority`
- `access_count`
- `left`
- `right`
- `shortcuts`

---

### `JproteraiodendroTree`

Main adaptive tree structure.

Methods include:

| Method | Description |
|---|---|
| `insert()` | Inserts new nodes |
| `search()` | Searches and adapts tree |
| `_rebalance_adaptive()` | Performs adaptive rotations |
| `display_structure()` | Prints tree hierarchy |

---

## Adaptive Rebalancing

The tree uses:

- Zig-Zig rotations
- Zig-Zag rotations
- Zag-Zag rotations
- Zag-Zig rotations

to optimize frequently accessed ("hot") nodes.

---

## Example Output

### Before Adaptation

```text
        50
       /  \
     20    80
    / \   / \
  10 30 70 90
```

### After Frequent Access to Node 10

```text
10 becomes closer to the root
for faster future access.
```

---

## Run the Project

### Requirements

- Python 3.x

### Execute

```bash
python program.py
```

---

## Sample Simulation

The script:

1. Creates the tree
2. Inserts sample data
3. Displays initial structure
4. Simulates repeated access to node `10`
5. Rebalances automatically
6. Displays optimized structure

---

## Future Improvements

- True distributed/sharded implementation
- Graph-based shortcut routing
- Persistence support
- Concurrent operations
- Performance benchmarking
- Visualization GUI

---

## Concepts Used

- Binary Search Trees (BST)
- Self-adjusting Trees
- Splay Tree Concepts
- Adaptive Algorithms
- Graph-assisted Routing
- Performance Optimization

---

## License

MIT License

---

## Author

Created by JAYAPRAKASH V
