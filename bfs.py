import csv
import networkx as nx


def read_input(till_round):
    G = nx.Graph()
    teams_data = {}
    matches = []
    with open("matches.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header row
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

            matches.append(
                {
                    round_num,
                    match_date,
                    home_team,
                    away_team,
                    home_score,
                    away_score,
                    result,
                }
            )
            # add match data to home team's list of matches
            if G.has_edge(home_team, away_team):
                old = G.get_edge_data(home_team, away_team)["match_index"]
                old.append(len(matches) - 1)
                G.add_edge(home_team, away_team, match_index=old)
            else:
                G.add_edge(home_team, away_team, match_index=[len(matches) - 1])
            if home_team not in teams_data:
                teams_data[home_team] = {
                    "match_played": 0,
                    "w": 0,
                    "d": 0,
                    "l": 0,
                    "gf": 0,
                    "ga": 0,
                    "gd": 0,
                    "points": 0,
                }
            if away_team not in teams_data:
                teams_data[away_team] = {
                    "match_played": 0,
                    "w": 0,
                    "d": 0,
                    "l": 0,
                    "gf": 0,
                    "ga": 0,
                    "gd": 0,
                    "points": 0,
                }
    return [G, matches, teams_data]


def bfs():
    input = read_input(1)
    unvisited = list(input[0].nodes)
    # for v in unvisited:
    for i in nx.dfs_edges(input[0]):
        input[2][i[0]]["match_played"] += len(
            input[0].get_edge_data(i[0], i[1])["match_index"]
        )
        input[2][i[1]]["match_played"] += len(
            input[0].get_edge_data(i[0], i[1])["match_index"]
        )

        print(i)


bfs()
