# How to Use

## Requirements

Make sure Python 3 is installed on your system.

Check version:

```bash
python --version
```

---

## Run the Program

Execute the file using:

```bash
python program.py
```

---

## What the Program Does

The program will:

1. Initialize the JproteraiodendroTree (JDT)
2. Insert sample nodes into the tree
3. Display the initial tree structure
4. Simulate repeated searches on a hot node
5. Adaptively rebalance the tree
6. Display the optimized tree structure

---

## Example Workflow

```python
jdt = JproteraiodendroTree()

jdt.insert(50, "Value_50")
jdt.insert(20, "Value_20")

jdt.search(20)

jdt.display_structure()
```

---

## Expected Output

```text
Inserted: 50
Inserted: 20

Found 20 (Priority 10)

Tree Structure Updated
```

---

## Customization

You can modify:

- Inserted data values
- Search frequency
- Priority calculation algorithm
- Rebalancing logic
- Tree visualization methods

---

## File Structure

```text
project/
│
├── program.py
├── README.md
└── HOW_TO_USE.md
```