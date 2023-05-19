import networkx as nx
import csv

# Define the matches data
matches = [
    ["1", "2022-01-01", "a", "b", 2, 1],
    # a b c d
    # 5 4 4 2
    ["1", "2022-01-01", "c", "d", 1, 0],
    ["2", "2022-01-08", "a", "c", 1, 1],
    ["2", "2022-01-08", "b", "d", 2, 2],
    ["3", "2022-01-15", "a", "d", 1, 1],
    ["3", "2022-01-15", "b", "c", 3, 0],
    ["4", "2022-01-15", "a", "b", 1, 2],
    ["4", "2022-01-15", "c", "d", 3, 0],
]
# 6 7 7 2
# Create an empty directed graph using the networkx library
G = nx.DiGraph()


def topological_sort(graph):
    """
    Perform topological sort on a directed acyclic graph.

    Parameters:
        graph (nx.DiGraph): A directed acyclic graph to be sorted.

    Returns:
        list: A list of nodes in topologically sorted order.

    Raises:
        ValueError: If the graph contains cycles.
    """
    # Create a copy of the graph to avoid modifying the original
    graph = graph.copy()

    # Create a list to hold the sorted nodes
    sorted_nodes = []

    # Create a dictionary to store the number of incoming edges for each node
    incoming_edges = {node: 0 for node in graph.nodes()}

    # Iterate over the edges in the graph and update the incoming edges count
    for from_node, to_node in graph.edges():
        if to_node == "virtual":
            incoming_edges[from_node] = -1
        incoming_edges[to_node] += 1

    # Create a queue to hold the nodes with no incoming edges
    # losers
    queue = [
        node
        for node, count in incoming_edges.items()
        if count == 0 and node != "virtual"
    ]
    print(queue)
    print(incoming_edges["virtual"])
    for from_node, to_node in graph.in_edges("virtual"):
        print("from " + from_node)
        print("to " + to_node)
        queue.append(from_node)
        incoming_edges["virtual"] -= 1
        # incoming_edges[to_node] -= 1
    print(incoming_edges["virtual"])
    # Iterate over the queue and remove nodes with no incoming edges
    while queue:
        # Remove the first node from the queue
        node = queue.pop(0)

        # Add the node to the sorted list
        sorted_nodes.append(node)

        # Iterate over the edges coming out of the node and decrease the incoming edges count

        for _, to_node in graph.edges(node):
            incoming_edges[to_node] -= 1
            # If the incoming edges count for a node is zero, add it to the queue
            if incoming_edges[to_node] == 0:
                queue.append(to_node)
    # If not all nodes were added to the sorted list, the graph contains cycles
    if len(sorted_nodes) != len(graph.nodes()) - 1:
        raise ValueError("Graph contains cycles.")

    return [sorted_nodes]


def construct_rounds(till_round):
    with open("matches.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header row
        rounds = {}
        for row in reader:
            round_num = int(row[0].strip())
            if round_num > till_round:
                break
            match_date = row[1]
            home_team = row[2]
            away_team = row[3]
            home_score = int(row[4])
            away_score = int(row[5])
            result = row[6]
            if round_num not in rounds:
                rounds[round_num] = []
            rounds[round_num].append(
                [
                    round_num,
                    match_date,
                    home_team,
                    away_team,
                    home_score,
                    away_score,
                ]
            )
    return rounds


# Calculate the total points for each team


def calc_score_for_round(round):
    team_points = {}
    for match in round:
        home_team = match[2]
        away_team = match[3]
        home_score = match[4]
        away_score = match[5]

        if home_team not in team_points:
            team_points[home_team] = 0
        if away_team not in team_points:
            team_points[away_team] = 0

        if home_score > away_score:
            team_points[home_team] += 3
        elif home_score < away_score:
            team_points[away_team] += 3
        else:
            team_points[home_team] += 1
            team_points[away_team] += 1
    return team_points


# Add nodes for each team to the graph


# Add edges for each match outcome to the graph, with weights representing the points gained
def sort_round(round):
    teams = {"virtual": True}
    for match in round:
        teams[match[2]] = True
        teams[match[3]] = True
    G = nx.DiGraph()
    G.add_nodes_from(teams)
    for match in round:
        home_team = match[2]
        away_team = match[3]
        home_score = match[4]
        away_score = match[5]
        if home_score > away_score:
            G.add_edge(away_team, home_team, weight=3)
        elif home_score < away_score:
            G.add_edge(home_team, away_team, weight=3)
        else:
            G.add_edge(home_team, "virtual", weight=1)
            G.add_edge(away_team, "virtual", weight=1)
    return topological_sort(G)
    # return list(nx.dag.topological_sort(G))


# Calculate the total points for each team after considering the feedback arc set
def get_sorted_rounds(rounds):
    sorted_rounds = []
    for round in rounds:
        sorted_round = sort_round(rounds[round])
        round_score = calc_score_for_round(rounds[round])
        temp = []
        for team in sorted_round[0]:
            if team == "virtual":
                continue
            temp.append([team, round_score[team]])
        sorted_rounds.append(temp)
    return sorted_rounds

# public static void merge(Comparable[] a, int lo, int mid, int hi)
# { // Merge a[lo..mid] with a[mid+1..hi].
#  int i = lo, j = mid+1;
#  for (int k = lo; k <= hi; k++) // Copy a[lo..hi] to aux[lo..hi].
#  aux[k] = a[k];
#  for (int k = lo; k <= hi; k++) // Merge back to a[lo..hi].
#  if (i > mid) a[k] = aux[j++];
#  else if (j > hi ) a[k] = aux[i++];
#  else if (less(aux[j], aux[i])) a[k] = aux[j++];
#  else a[k] = aux[i++];
# }
rounds_unsorted = construct_rounds(20)
G.add_nodes_from(rounds_unsorted)
sorted_rounds = get_sorted_rounds(rounds_unsorted)
def sort_critera(i):
    return i[1]
def merge_rounds(rounds):
    
    res = []
    hash = {}
    for round in rounds:
        for team in round:
            if(team[0] not in hash):
                hash[team[0]] =0
            hash[team[0]]+= team[1]
    for team in hash:
        res.append([team,hash[team]])
    
    return sorted(res,key=sort_critera)


print(merge_rounds(sorted_rounds))
        

# for i in sorted_rounds:
    # None
