import numpy as np
from solver import nash_equlibrium_solver
import os

"""
Payoff matrix of matching pennies game

    p1\p2  |  Heads       Tails
    -----------------------------
    Heads  | (+1, -1)    (-1, +1)

    Tails  | (-1, +1)    (+1, -1)

"""
example_dir = os.path.dirname(os.path.abspath(__file__))
payoff_matrix_dir = os.path.join(example_dir, "payoff_matrix.npy")

def generate_payoff_matrix():
    p1_payoff_matrix = np.array([[+1, -1], [-1, +1]])
    np.save(payoff_matrix_dir, p1_payoff_matrix)
    return p1_payoff_matrix

def solve():

    game_step = 1
    action_choice = 2

    all_actions = {0: "head", 1: "tail"}

    payoff_matrix = np.load(payoff_matrix_dir)
    solver = nash_equlibrium_solver(game_step, action_choice_player1=action_choice, action_choice_player2=action_choice, payoff_matrix=payoff_matrix)
    player2_sol = solver.solve_linear_program_player2()
    player1_sol = solver.solve_linear_program_player1()

    print("-------------Player 2 strategy-------------")
    if player2_sol is not None:
        player2_strategy = player2_sol[0]
        for k, v in player2_strategy.items():
            action = all_actions[k]
            print(action, v)
    else:
        print('')

    print("-------------Player 1 strategy-------------")
    if player1_sol is not None:
        player1_strategy = player1_sol[0]
        for k, v in player1_strategy.items():
            action = all_actions[k]
            print(action, v)
    else:
        print('')

if __name__ == '__main__':

    # if the payoff matrix is not generated
    if not os.path.isfile(payoff_matrix_dir):
        p1_payoff_matrix = generate_payoff_matrix()
    solve()

