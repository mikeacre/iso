"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO:

    #check if result is a loser or winner and return a max or min value
    if game.is_loser(game.active_player):
        return float("-inf")

    if game.is_winner(game.active_player):
        return float("inf")

    if len(game.get_legal_moves()) == 0:
        return -72.0

    #get location of position
    loc_h, loc_w = game.get_player_location(game.active_player) if game.get_player_location(game.active_player) else (-1,-1)
    loc_h_in, loc_w_in = game.get_player_location(game.inactive_player) if game.get_player_location(game.inactive_player) else (-1,-1)

    #check the board size and add a bias to a location that is closer to the center.
    #subtract half the board size in order to give the highest value for a centered move
    board_size = (game.height-1)/2
    loc_h = loc_h - board_size if loc_h > board_size else loc_h
    loc_w = loc_w - board_size if loc_w > board_size else loc_w

    #create a bias for the inactive_player as well
    loc_h_in = loc_h_in - board_size if loc_h_in > board_size else loc_h_in
    loc_w_in = loc_w_in - board_size if loc_w_in > board_size else loc_w_in

    bias = 0
    bias += (loc_h * loc_w )
    #bias -= (loc_h_in * loc_w_in )*0.25

    utility = float(len(game.get_legal_moves())*1.25)+bias
    return utility



def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(game.active_player):
        return -72.0

    if game.is_winner(game.active_player):
        return 72.0

    if len(game.get_legal_moves()) == 0:
        return -72.0

    #get location of position
    loc_h, loc_w = game.get_player_location(game.active_player) if game.get_player_location(game.active_player) else (-1,-1)
    loc_h_in, loc_w_in = game.get_player_location(game.inactive_player) if game.get_player_location(game.inactive_player) else (-1,-1)

    #check the board size and add a bias to a location that is closer to the center.
    #subtract half the board size in order to give the highest value for a centered move
    board_size = (game.height-1)/2
    loc_h = loc_h - board_size if loc_h > board_size else loc_h
    loc_w = loc_w - board_size if loc_w > board_size else loc_w

    bias = 1
    bias += (loc_h * loc_w )*0.5

    utility = (len(game.get_legal_moves()) - len(game.get_legal_moves(game.inactive_player)))*bias
    return utility


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    #check if result is a loser or winner and return a max or min value
    utility = len(game.get_legal_moves())*1.5-len(game.get_legal_moves(game.inactive_player))
    return utility


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def poss_moves(self, state, player):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        return state.get_legal_moves(player)


    def max_value(self, state, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0 or not state.get_legal_moves():
             return self.score(state, self)

        util = float("-inf")
        moves = state.get_legal_moves()
        for m in moves:
            util = max(util, self.min_value(state.forecast_move(m), depth-1))
        #util = max([self.min_value(state.forecast_move(m), depth-1) for m in moves])
        return util


    def min_value(self, state, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0 or not state.get_legal_moves():
             return self.score(state, self)
        util = float("inf")
        moves = state.get_legal_moves()
        for m in moves:
            util = min(util, self.max_value(state.forecast_move(m), depth-1))
        #util = min([self.max_value(state.forecast_move(m), depth-1) for m in moves])
        return util


    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #game [x,y] is the game board a multiple demensional array

        #depth is how many layers deep to look in the tree
        curr_player = game._active_player
        curr_location = game.get_player_location(curr_player)
        legal_moves = self.poss_moves(game, curr_player)
        utility = float("-inf")
        best_move = (2,2)
        if not legal_moves:
            return (-1, -1)

        for m in  legal_moves:
            util = self.min_value(game.forecast_move(m), depth-1)
            if util > utility:
                utility = util
                best_move = m
        return best_move

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def max_value(self, state, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0 or not state.get_legal_moves():
             return self.score(state, self)

        best = float('-inf')
        moves = state.get_legal_moves()
        for m in moves:
            best = max(best, self.min_value(state.forecast_move(m), depth-1, alpha, beta))
            if best >= beta:
                return best
            alpha = max(alpha, best)
        return best


    def min_value(self, state, depth, alpha, beta):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0 or not state.get_legal_moves():
             return self.score(state, self)

        best = float('inf')
        moves = state.get_legal_moves()
        for m in moves:
            best = min(best, self.max_value(state.forecast_move(m), depth-1, alpha, beta))
            if best <= alpha:
                return best
            beta = min(best, beta)
        return best


    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        i = 0
        best = (-1,-1)

        try:

            while True:
                i +=1
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
                best = self.alphabeta(game, i)

        except SearchTimeout:
            pass

        return best


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        highest = float("-inf")

        if not legal_moves:
            return (-1, -1)

        best_move = legal_moves[0]

        for m in  legal_moves:
            util = self.min_value(game.forecast_move(m), depth-1, alpha, beta)
            if util > highest:
                best_move = m
                highest = util
            alpha = max(alpha,highest)



        return best_move
