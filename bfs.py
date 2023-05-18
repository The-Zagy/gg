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
            G.add_edge(home_team, away_team, match_index=len(matches) - 1)
            G.add_edge(away_team, home_team, match_index=len(matches) - 1)
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


res = read_input(7)
print(res)
