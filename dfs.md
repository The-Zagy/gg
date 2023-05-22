# Algorithm Analysis

## Time Complexity

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
<br>
O(E+V * log(V))
<br>
O(E+Vlog(V))
<br>
if number of rounds = X 
<br>
E = (V/2) * X 
<br>
O((VX)/2 + V*log(V))

## Space Complexity

The space complexity of the code can be analyzed based on the additional memory used by the data structures and variables during the execution of the program. Let's examine the main components:

- Graph and Match Data: 
 The code creates a NetworkX graph object (G) to represent the teams and their matches. The space required for storing the graph depends on the number of edges (matches) and nodes (teams). In the worst case, the graph can have O(E) edges and O(V) nodes. Additionally, the match data (matches list and teams_data dictionary) is stored in memory. Thus, the space complexity for the graph and match data is O(E + V).

- Teams Data:
 The teams_data dictionary stores the statistics and information for each team. The dictionary size is proportional to the number of teams (V), with each team occupying a fixed amount of space for its data. Therefore, the space complexity for the teams_data dictionary is O(V).

