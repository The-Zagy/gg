import csv
import sys
import argparse

import networkx as nx
from tabulate import tabulate


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
            try:
                match_date = row[1]
                home_team = row[2]
                away_team = row[3]
                home_score = int(row[4])
                away_score = int(row[5])
                result = row[6]
            except:
                continue
            matches.append(
                [
                    round_num,
                    match_date,
                    home_team,
                    away_team,
                    home_score,
                    away_score,
                    result,
                ]
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
                    "name": home_team,
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
                    "name": away_team,
                    "match_played": 0,
                    "w": 0,
                    "d": 0,
                    "l": 0,
                    "gf": 0,
                    "ga": 0,
                    "gd": 0,
                    "points": 0,
                }
    # all_edges = list(G.edges()) + [(v, u) for u, v in G.edges()]
    # for i in all_edges:
    #     print(i)
    return [G, matches, teams_data]


def dfs(until_round):
    G, matches, teams_data = read_input(until_round)
    # unvisited = list(input[0].nodes)
    for teams in nx.edge_dfs(G):
        match_index = G.get_edge_data(teams[0], teams[1])["match_index"]
        print(teams)
        # update each match data in the team hash
        for match in match_index:
            # update home team
            teams_data[teams[0]]["match_played"] += 1

            # update away team
            teams_data[teams[1]]["match_played"] += 1

            teams_data[matches[match][2]]["gf"] += matches[match][4]
            teams_data[matches[match][2]]["ga"] += matches[match][5]
            teams_data[matches[match][2]]["gd"] = (
                teams_data[matches[match][2]]["gf"] - teams_data[matches[match][2]]["ga"]
            )

            teams_data[matches[match][3]]["gf"] += matches[match][5]
            teams_data[matches[match][3]]["ga"] += matches[match][4]
            teams_data[matches[match][3]]["gd"] = (
                teams_data[matches[match][3]]["gf"] - teams_data[matches[match][3]]["ga"]
            )

            if matches[match][6] == "H":
                teams_data[matches[match][2]]["w"] += 1
                teams_data[matches[match][2]]["points"] += 3
                teams_data[matches[match][3]]["l"] += 1
            if matches[match][6] == "A":
                teams_data[matches[match][3]]["w"] += 1
                teams_data[matches[match][3]]["points"] += 3
                teams_data[matches[match][2]]["l"] += 1
            if matches[match][6] == "D":
                teams_data[matches[match][3]]["d"] += 1
                teams_data[matches[match][2]]["points"] += 1
                teams_data[matches[match][3]]["points"] += 1
                teams_data[matches[match][2]]["d"] += 1

    res = list(teams_data.values())
    res.sort(reverse=True, key=lambda i: i["points"])

    # for t in res:
    #     print(t)
    headers = res[0].keys()
    table_data = [list(row.values()) for row in res]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))


def main():
    parser = argparse.ArgumentParser(
        description="""
    display the standing of the league for a given round or date
    """
    )
    parser.add_argument("-r", "--round", type=int, help="round number")
    parser.add_argument("-d", "--date", type=str, help="standing date")
    args = parser.parse_args()
    r = args.round
    date = args.date
    if r is None and date is None:
        print("use --help for help menu")
        sys.exit()
    dfs(r)


if __name__ == "__main__":
    main()
