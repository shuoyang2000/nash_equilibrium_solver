import numpy as np
from solver import nash_equlibrium_solver

# takes around 30 seconds
def solve_grid():

    game_step = 4
    action_choice = 8
    action_total_num = action_choice ** game_step

    action_1 = np.linspace(0, action_choice-1, action_choice, dtype=int)
    action_2 = np.linspace(0, action_choice-1, action_choice, dtype=int)
    action_3 = np.linspace(0, action_choice-1, action_choice, dtype=int)
    action_4 = np.linspace(0, action_choice-1, action_choice, dtype=int)

    act1, act2, act3, act4 = np.meshgrid(action_1, action_2, action_3, action_4, indexing='ij')
    all_actions = np.stack((act1, act2, act3, act4), axis=-1).reshape(action_total_num, game_step)

    payoff_matrix = np.load('examples/grid_world/payoff_matrix_grid.npy')
    solver = nash_equlibrium_solver(game_step, action_choice_player1=action_choice, action_choice_player2=action_choice, payoff_matrix=payoff_matrix)
    player2_sol = solver.solve_linear_program_player2()
    player1_sol = solver.solve_linear_program_player1()

    print("-------------Player 2 strategy-------------")
    if player2_sol is not None:
        player2_strategy = player2_sol[0]
        for k, v in player2_strategy.items():
            action = all_actions[k, :]
            print(action, v)
    else:
        print('')

    print("-------------Player 1 strategy-------------")
    if player1_sol is not None:
        player1_strategy = player1_sol[0]
        for k, v in player1_strategy.items():
            action = all_actions[k, :]
            print(action, v)
    else:
        print('')

if __name__ == '__main__':
    solve_grid()