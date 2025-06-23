**Simple star graph with 5 nodes:**

```py
    B
    |
D - A - C
    |
    E

graph = {
    'A': ['B', 'C', 'D', 'E'],
    'B': ['A'],
    'C': ['A'],
    'D': ['A'],
    'E': ['A']
}
```