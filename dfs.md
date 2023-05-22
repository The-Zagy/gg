# Algorithm Analysis

The program stores the given dataset in a graph data structure. The vertices represent the teams, and the Edges stores the match indices between the two connected vertices which are stored in an array. Then, it conducts a Depth-First Search (DFS) on the graph, by visiting all the edges (matches) from every Vertex to construct result in a hash table. 

```tsx
type teams_data = {
                    "name": string,
                    "match_played": number,
                    "w": number,
                    "d": number,
                    "l": number,
                    "gf": number,
                    "ga": number,
                    "gd": number,
                    "points": number
                }
```

Then, we sort the teams by their total_points.

Let Number of matches (rows in the csv file) = E

Let Number of teams = V

- Input:
O(E)
- DFS:
O(E + V)
- Sorting: O(V*logV)

O(E+V * log(V))

O(E+Vlog(V))

if number of rounds = X E = (V/2) * X O((VX)/2 + V*log(V))

E = (V/2) * X O((VX)/2 + V*log(V))

