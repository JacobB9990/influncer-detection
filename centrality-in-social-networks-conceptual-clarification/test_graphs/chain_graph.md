Simple chain graph with 5 nodes:

```py
A - B - C - D - E

graph = {
    'A': ['B'],
    'B': ['A', 'C'],
    'C': ['B', 'D'],
    'D': ['C', 'E'],
    'E': ['D']
}
```