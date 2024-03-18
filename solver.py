from gurobipy import *
import numpy as np
import time

class NashEqulibriumSolver:

    def __init__(self, game_step:int, p1_action_num:int, p2_action_num:int, payoff_matrix:np.array):
        
        """
        game_step: step number of the game; normal game step is 1, extensive game step is more than 1
        p1_action_num: player 1's action number
        p2_action_num: player 2's action number
        payoff_matrix: the generated payoff matrix of the game
        """

        self.game_step = game_step
        self.action_choice_player1 = p1_action_num
        self.action_choice_player2 = p2_action_num
        self.action_total_num_player1 = self.action_choice_player1 ** game_step
        self.action_total_num_player2 = self.action_choice_player2 ** game_step
        self.payoff_matrix = payoff_matrix
        
        assert self.payoff_matrix.shape[0] == self.action_total_num_player1, "Payoff matrix row number does not match Player 1 pure strategy number"
        assert self.payoff_matrix.shape[1] == self.action_total_num_player2, "Payoff matrix column number does not match Player 2 pure strategy number"
    
    def solve_linear_program_player1(self, verbose: bool=False):

        """
        Solve the NE profile strategy for player 1

        verbose: output result details or not

        Return (filtered_player1_NE, NE_utility), where filtered_player1_NE is player 1's strategy, 
                                                        and NE_utility is its NE profile utility
        """

        start_time = time.time()

        ## setup model
        LP_model = Model()
        LP_model.setParam('OutputFlag', 0)

        ## define variables
        game_value = LP_model.addVar(name='game_value', vtype=GRB.CONTINUOUS) # the NE profile utility, i.e., the value of the zero-sum two-player game
        player1_actions = LP_model.addVars(self.action_total_num_player1, vtype=GRB.CONTINUOUS) # the probabilities for all actions of player 1

        ## add constraints

        # all player 1 actions' probability should be non-negative, and their sum is 1
        LP_model.addConstr(player1_actions.sum() == 1)
        LP_model.addConstrs(player1_actions[i] >= 0 for i in range(self.action_total_num_player1))
       
        # bound player 1's utility by game_value (for each player 1's pure strategy)
        for player2_action_index in range(self.action_total_num_player2):
            lhs = 0
            for player1_action_index in range(self.action_total_num_player1):
                # if the payoff matrix is huge (e.g., converted from extensive game), we can store it with bool utilities to save space
                if type(self.payoff_matrix[player1_action_index, player2_action_index]) is np.bool_:
                    p1_utility = 1 if self.payoff_matrix[player1_action_index, player2_action_index] else -1
                # for simple normal form game, just store all payoff values
                else:
                    p1_utility = self.payoff_matrix[player1_action_index, player2_action_index]
                lhs += p1_utility * player1_actions[player1_action_index]
            LP_model.addConstr(lhs >= game_value)


        ## setup objective func and solve
        obj = game_value
        LP_model.setObjective(obj, GRB.MAXIMIZE)

        LP_model.optimize()

        ## return solved outcomes
        if LP_model.Status == GRB.Status.OPTIMAL:
            player1_NE = LP_model.getAttr('x', player1_actions)
            filtered_player1_NE = {k: v for k,v in player1_NE.items() if v > 0.}
            NE_utility = LP_model.ObjVal
            if verbose:
                print("Player 1 strategy solving time: ", time.time() - start_time)
                print("Nash Equlibrium Profile Utility for Player 1: ", NE_utility)
                print("Nash Equlibrium Player 1 Strategy: ", filtered_player1_NE)
                print("------------------------------------------")
            return (filtered_player1_NE, NE_utility)
        else:
            print(LP_model.Status, GRB.Status.OPTIMAL)
            print("The linear programming for player 1 is infeasible, please double check.")
            return None
    
    def solve_linear_program_player2(self, verbose: bool=False):

        """
        Solve the NE profile strategy for player 2

        verbose: output result details or not

        Return (filtered_player2_NE, NE_utility), where filtered_player2_NE is player 2's strategy, 
                                                        and NE_utility is its NE profile utility
        """

        start_time = time.time()

        ## setup model
        LP_model = Model()
        LP_model.setParam('OutputFlag', 0)

        ## define variables
        game_value = LP_model.addVar(name='game_value', vtype=GRB.CONTINUOUS) # the NE profile utility, i.e., the value of the zero-sum two-player game
        player2_actions = LP_model.addVars(self.action_total_num_player2, vtype=GRB.CONTINUOUS) # the probabilities for all actions of player 2

        ## add constraints

        # all player 2 actions' probability should be non-negative, and their sum is 1
        LP_model.addConstr(player2_actions.sum() == 1)
        LP_model.addConstrs(player2_actions[i] >= 0 for i in range(self.action_total_num_player2))
       
        # bound player 2's utility by game_value (for each player 1's pure strategy)
        for player1_action_index in range(self.action_total_num_player1):
            lhs = 0
            for player2_action_index in range(self.action_total_num_player2):
                # if the payoff matrix is huge (e.g., converted from extensive game), we can store it with bool utilities to save space
                if type(self.payoff_matrix[player1_action_index, player2_action_index]) is np.bool_:
                    p1_utility = 1 if self.payoff_matrix[player1_action_index, player2_action_index] else 1
                # for simple normal form game, just store all payoff values
                else:
                    p1_utility = self.payoff_matrix[player1_action_index, player2_action_index]
                lhs += p1_utility * player2_actions[player2_action_index]
            LP_model.addConstr(lhs <= game_value)


        ## setup objective func and solve
        obj = game_value
        LP_model.setObjective(obj, GRB.MINIMIZE)

        LP_model.optimize()

        ## return solved outcomes
        if LP_model.Status == GRB.Status.OPTIMAL:
            player2_NE = LP_model.getAttr('x', player2_actions)
            filtered_player2_NE = {k: v for k,v in player2_NE.items() if v > 0.}
            NE_utility = LP_model.ObjVal
            if verbose:
                print("Player 2 strategy solving time: ", time.time() - start_time)
                print("Nash Equlibrium Profile Utility for Player 2: ", - NE_utility)
                print("Nash Equlibrium Player 2 Strategy: ", filtered_player2_NE)
                print("------------------------------------------")
            return (filtered_player2_NE, NE_utility)
        else:
            print(LP_model.Status, GRB.Status.OPTIMAL)
            print("The linear programming for player 2 is infeasible, please double check.")
            return None