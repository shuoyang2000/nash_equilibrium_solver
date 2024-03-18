import numpy as np
from solver import NashEqulibriumSolver
import os
import argparse
import yaml

# solve the game
def solve(game_step: int, p1_action_choice: dict, p2_action_choice: dict, payoff_matrix: np.array, verbose: bool=False):

    # some basic setup
    p1_action_num = len(p1_action_choice)
    p2_action_num = len(p2_action_choice)

    # solving
    solver = NashEqulibriumSolver(game_step, p1_action_num=p1_action_num, 
                                    p2_action_num=p2_action_num, payoff_matrix=payoff_matrix)
    player1_sol = solver.solve_linear_program_player1(verbose=verbose)
    player2_sol = solver.solve_linear_program_player2(verbose=verbose)

    # results
    print("-------------Player 2 strategy-------------")
    if player2_sol is not None:
        player2_strategy = player2_sol[0]
        for k, v in player2_strategy.items():
            action = p2_action_choice[k]
            print(action, v)
    else:
        print('')

    print("-------------Player 1 strategy-------------")
    if player1_sol is not None:
        player1_strategy = player1_sol[0]
        for k, v in player1_strategy.items():
            action = p1_action_choice[k]
            print(action, v)
    else:
        print('')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='game_example')
    parser.add_argument('--verbose', action=argparse.BooleanOptionalAction, help='Verbose output')
    parser.add_argument('--example', type=str, required=True, 
                        help="Which example you want to try? (e.g., rock_paper_scissor, presidential_election, matching_pennies)")
    args = parser.parse_args()

    # extract game rules from .yaml file
    example_name = args.example
    example_dir = os.path.join('examples', example_name)
    try:
        with open(example_dir+'.yaml', 'r') as stream:
            example_setup = yaml.safe_load(stream)
    except:
        raise ValueError(f"The example {example_name} is not included yet, please check out the example folder to see all current examples.")

    payoff_matrix = np.array(example_setup['payoff_matrix'])
    game_step = example_setup['game_step']
    p1_actions = example_setup['p1_actions']
    p2_actions = example_setup['p2_actions']

    # solve the game
    solve(p1_action_choice=p1_actions, p2_action_choice=p2_actions, payoff_matrix=payoff_matrix, game_step=game_step, verbose=args.verbose)