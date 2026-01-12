import pandas as pd
import numpy as np
import os

# Force the script to look in the folder where it is saved
os.chdir(os.path.dirname(os.path.abspath(__file__)))

FILE_NAME = 'simulation.csv'

def get_sos(team, all_matches, standings):
    """Calculates SOS: (Sum of Opponent Wins) / (Sum of Opponent Maps Played)"""
    opponents = []
    team_matches = all_matches[(all_matches['TeamA'] == team) | (all_matches['TeamB'] == team)]
    
    opp_wins = 0
    opp_maps = 0
    
    for _, row in team_matches.iterrows():
        opp = row['TeamB'] if row['TeamA'] == team else row['TeamA']
        opp_wins += standings[opp]['wins']
        # In this sim, every match is 1 map. If your CSV has Bo3s, adjust maps_played.
        opp_maps += standings[opp]['matches_played'] 
        
    return opp_wins / opp_maps if opp_maps > 0 else 0

def resolve_ties(teams_to_fix, all_matches, standings):
    """
    Recursive tiebreaker following Rule 16.1.2.
    Groups teams by advantage and breaks them down further if ties remain.
    """
    if len(teams_to_fix) <= 1:
        return teams_to_fix

    # Filter matches only between the tied teams for H2H
    h2h_matches = all_matches[
        all_matches['TeamA'].isin(teams_to_fix) & 
        all_matches['TeamB'].isin(teams_to_fix)
    ]

    # Calculate Tiebreaker Metrics
    metrics = []
    for team in teams_to_fix:
        # H2H Record
        h2h_wins = 0
        h2h_rd = 0
        for _, m in h2h_matches.iterrows():
            if m['TeamA'] == team:
                if m['ScoreA'] > m['ScoreB']: h2h_wins += 1
                h2h_rd += (m['ScoreA'] - m['ScoreB'])
            elif m['TeamB'] == team:
                if m['ScoreB'] > m['ScoreA']: h2h_wins += 1
                h2h_rd += (m['ScoreB'] - m['ScoreA'])
        
        # Overall Round Win %
        total_r_won = standings[team]['rd_plus']
        total_r_played = standings[team]['rd_plus'] + standings[team]['rd_minus']
        win_pct = total_r_won / total_r_played if total_r_played > 0 else 0
        
        # Strength of Schedule
        sos = get_sos(team, all_matches, standings)
        
        metrics.append({
            'team': team,
            'h2h_w': h2h_wins,
            'h2h_rd': h2h_rd,
            'win_pct': win_pct,
            'sos': sos,
            'random': np.random.random() # Coin Flip
        })

    # Sort by the priority list
    metrics.sort(key=lambda x: (x['h2h_w'], x['h2h_rd'], x['win_pct'], x['sos'], x['random']), reverse=True)
    
    # Check for sub-ties (separating into new tiebreakers)
    final_ordered = []
    i = 0
    while i < len(metrics):
        j = i + 1
        while j < len(metrics) and \
              metrics[i]['h2h_w'] == metrics[j]['h2h_w'] and \
              metrics[i]['h2h_rd'] == metrics[j]['h2h_rd'] and \
              metrics[i]['win_pct'] == metrics[j]['win_pct'] and \
              metrics[i]['sos'] == metrics[j]['sos']:
            j += 1
        
        if j - i > 1:
            # Sub-tie found, resolve from scratch for these specific teams
            sub_group = [m['team'] for m in metrics[i:j]]
            final_ordered.extend(resolve_ties(sub_group, all_matches, standings))
        else:
            final_ordered.append(metrics[i]['team'])
        i = j
        
    return final_ordered

def run_sim(iterations=10000):
    df_raw = pd.read_csv(FILE_NAME, header=None, names=['TeamA', 'TeamB', 'ScoreA', 'ScoreB'])
    teams = pd.unique(df_raw[['TeamA', 'TeamB']].values.ravel('K'))
    played_orig = df_raw.dropna(subset=['ScoreA', 'ScoreB']).copy()
    remaining_orig = df_raw[df_raw['ScoreA'].isna()].copy()

    results = []

    for _ in range(iterations):
        # 1. Simulate matches
        sim_matches = played_orig.copy()
        for _, row in remaining_orig.iterrows():
            winner_a = np.random.random() > 0.5
            sA, sB = (13, np.random.randint(0, 13)) if winner_a else (np.random.randint(0, 13), 13)
            sim_matches = pd.concat([sim_matches, pd.DataFrame([{
                'TeamA': row['TeamA'], 'TeamB': row['TeamB'], 'ScoreA': sA, 'ScoreB': sB
            }])])

        # 2. Calculate Base Standings
        standings = {team: {'wins': 0, 'rd_plus': 0, 'rd_minus': 0, 'matches_played': 0} for team in teams}
        for _, row in sim_matches.iterrows():
            standings[row['TeamA']]['rd_plus'] += row['ScoreA']
            standings[row['TeamA']]['rd_minus'] += row['ScoreB']
            standings[row['TeamB']]['rd_plus'] += row['ScoreB']
            standings[row['TeamB']]['rd_minus'] += row['ScoreA']
            standings[row['TeamA']]['matches_played'] += 1
            standings[row['TeamB']]['matches_played'] += 1
            if row['ScoreA'] > row['ScoreB']: standings[row['TeamA']]['wins'] += 1
            else: standings[row['TeamB']]['wins'] += 1

        # 3. Group by Win Count and Resolve Ties
        win_groups = {}
        for team, stats in standings.items():
            w = stats['wins']
            if w not in win_groups: win_groups[w] = []
            win_groups[w].append(team)
            
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

# Last updated 2025-12-20
