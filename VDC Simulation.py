import pandas as pd
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
FILE_NAME = 'simulation.csv'

def get_sos(team, all_matches_list, standings):
    opp_wins = 0
    opp_maps = 0
    for m in all_matches_list:
        if m['TeamA'] == team or m['TeamB'] == team:
            opp = m['TeamB'] if m['TeamA'] == team else m['TeamA']
            opp_wins += standings[opp]['wins']
            opp_maps += standings[opp]['matches_played']
    return opp_wins / opp_maps if opp_maps > 0 else 0

def resolve_ties(teams_to_fix, all_matches_list, standings):
    if len(teams_to_fix) <= 1:
        return teams_to_fix

    # Filter matches for H2H using list comprehension
    h2h_matches = [m for m in all_matches_list if m['TeamA'] in teams_to_fix and m['TeamB'] in teams_to_fix]

    metrics = []
    for team in teams_to_fix:
        h2h_wins = 0
        h2h_rd = 0
        for m in h2h_matches:
            if m['TeamA'] == team:
                if m['ScoreA'] > m['ScoreB']: h2h_wins += 1
                h2h_rd += (m['ScoreA'] - m['ScoreB'])
            elif m['TeamB'] == team:
                if m['ScoreB'] > m['ScoreA']: h2h_wins += 1
                h2h_rd += (m['ScoreB'] - m['ScoreA'])
        
        total_r_won = standings[team]['rd_plus']
        total_r_played = standings[team]['rd_plus'] + standings[team]['rd_minus']
        win_pct = total_r_won / total_r_played if total_r_played > 0 else 0
        sos = get_sos(team, all_matches_list, standings)
        
        metrics.append({
            'team': team, 'h2h_w': h2h_wins, 'h2h_rd': h2h_rd,
            'win_pct': win_pct, 'sos': sos, 'random': np.random.random()
        })

    metrics.sort(key=lambda x: (x['h2h_w'], x['h2h_rd'], x['win_pct'], x['sos'], x['random']), reverse=True)
    
    final_ordered = []
    i = 0
    while i < len(metrics):
        j = i + 1
        while j < len(metrics) and all(metrics[i][k] == metrics[j][k] for k in ['h2h_w', 'h2h_rd', 'win_pct', 'sos']):
            j += 1
        if j - i > 1:
            final_ordered.extend(resolve_ties([m['team'] for m in metrics[i:j]], all_matches_list, standings))
        else:
            final_ordered.append(metrics[i]['team'])
        i = j
    return final_ordered

def run_sim(iterations=10000):
    df_raw = pd.read_csv(FILE_NAME, header=None, names=['TeamA', 'TeamB', 'ScoreA', 'ScoreB'])
    teams = pd.unique(df_raw[['TeamA', 'TeamB']].values.ravel('K'))
    
    # Convert to list of dicts.
    played_orig = df_raw.dropna(subset=['ScoreA', 'ScoreB']).to_dict('records')
    remaining_orig = df_raw[df_raw['ScoreA'].isna()][['TeamA', 'TeamB']].to_dict('records')

    results = []

    for _ in range(iterations):
        # 1. Simulate matches using lists
        sim_matches = list(played_orig) 
        for row in remaining_orig:
            winner_a = np.random.random() > 0.5
            sA, sB = (13, np.random.randint(0, 13)) if winner_a else (np.random.randint(0, 13), 13)
            sim_matches.append({'TeamA': row['TeamA'], 'TeamB': row['TeamB'], 'ScoreA': sA, 'ScoreB': sB})

        # 2. Calculate Standings
        standings = {team: {'wins': 0, 'rd_plus': 0, 'rd_minus': 0, 'matches_played': 0} for team in teams}
        for m in sim_matches:
            sA, sB = m['ScoreA'], m['ScoreB']
            tA, tB = m['TeamA'], m['TeamB']
            standings[tA]['rd_plus'] += sA
            standings[tA]['rd_minus'] += sB
            standings[tB]['rd_plus'] += sB
            standings[tB]['rd_minus'] += sA
            standings[tA]['matches_played'] += 1
            standings[tB]['matches_played'] += 1
            if sA > sB: standings[tA]['wins'] += 1
            else: standings[tB]['wins'] += 1

        # 3. Resolve Ties
        win_groups = {}
        for team, stats in standings.items():
            win_groups.setdefault(stats['wins'], []).append(team)
            
        final_rankings = []
        for w in sorted(win_groups.keys(), reverse=True):
            tied_teams = win_groups[w]
            if len(tied_teams) > 1:
                final_rankings.extend(resolve_ties(tied_teams, sim_matches, standings))
            else:
                final_rankings.append(tied_teams[0])

        for rank, team in enumerate(final_rankings):
            results.append({'Team': team, 'Rank': rank + 1})

    # 4. Output
    res_df = pd.DataFrame(results)
    pivot = pd.crosstab(res_df['Team'], res_df['Rank'], normalize='index') * 100
    print(pivot.round(2).to_string())
    pivot.to_csv('detailed_sim_results.csv')

if __name__ == "__main__":
    run_sim()

# Last updated 2026-1-12
