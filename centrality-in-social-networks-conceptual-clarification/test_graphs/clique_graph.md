**Connected graph with a central node (A) connected to all other nodes (B, C, D, E):**

```py
A - B
| \ |
C - D

graph = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['A', 'B', 'C']
}
```

| Node | Degree (norm) | Degree (raw) | Closeness (norm) | Betweenness (norm) | Betweenness (raw) |
| ---- | ------------- | ------------ | ---------------- | ------------------ | ----------------- |
| A    | 1.00          | 3.00         | 1.00             | 0.00               | 0.00              |
| B    | 1.00          | 3.00         | 1.00             | 0.00               | 0.00              |
| C    | 1.00          | 3.00         | 1.00             | 0.00               | 0.00              |
| D    | 1.00          | 3.00         | 1.00             | 0.00               | 0.00              |