from math import inf
from timeit import default_timer
from typing import Union

# Assume maximizing player is WHITE and minimizing player is BLACK.
# For now the AI is always BLACK.

NO_PIECE = 0
WHITE = 1
BLACK = 2
NODE_INDICES = range(24)

weights = {
    "mill": 20,
    "piece": 24,
    "free_move": 1
}

_best_node_id_to_take = -1
computation_count = 0


def ai_place_piece_at(position: list) -> int:
    """
    Args:
        position (list): The state of the game.

    Returns:
        int: The id of the node on which to put the piece.

    """
    global computation_count, _best_node_id_to_take
    best_evaluation = inf  # BLACK searches for the lowest evaluation!!!
    best_node_id = -1

    start = default_timer()
    for i in NODE_INDICES:
        if position[i] == NO_PIECE:  # If there is no piece
            position[i] = BLACK  # Put a BLACK piece
            if _check_is_windmill_formed(position, BLACK, i):
                best_eval_piece_to_take = inf
                for j in _get_nodes_pieces_to_take(position, WHITE):
                    position[j] = NO_PIECE
                    evaluation = _minimax_phase1(position, 3, -inf, inf, True)
                    position[j] = WHITE
                    if evaluation < best_eval_piece_to_take:
                        _best_node_id_to_take = j
                        best_eval_piece_to_take = evaluation
                    if evaluation < best_evaluation:
                        best_node_id = i
                        best_evaluation = evaluation
            else:
                evaluation = _minimax_phase1(position, 3, -inf, inf, True)  # It's maximizing player now, because we just put
                if evaluation < best_evaluation:                            # a black piece
                    best_node_id = i
                    best_evaluation = evaluation
            position[i] = NO_PIECE  # Undo the placement
            print(f"Checked spot {i}, evaluation is {evaluation}")
    print(f"Took {default_timer() - start} seconds")
    print(f"Nr. of computations is {computation_count}")
    computation_count = 0

    assert best_node_id != -1
    return best_node_id


def ai_remove_piece() -> int:
    """
    Returns:
        int: The id of the node from which to take the piece.

    """
    global _best_node_id_to_take
    assert _best_node_id_to_take != -1
    id = _best_node_id_to_take
    _best_node_id_to_take = -1
    return id


def ai_move_piece(position: list) -> tuple:
    """
    Args:
        position (list): The state of the game.

    Returns:
        tuple: The id of the source and destination nodes.

    """
    global computation_count, _best_node_id_to_take
    best_evaluation = inf
    best_node_id_src = -1
    best_node_id_dest = -1

    start = default_timer()
    for i in NODE_INDICES:
        if position[i] == BLACK:
            for j in _where_can_go(position, i, 2):  # TODO doesn't seem to return... 'position' wasn't correct
                if position[j] == NO_PIECE:
                    position[j] = BLACK
                    position[i] = NO_PIECE
                    if _check_is_windmill_formed(position, BLACK, j):
                        best_eval_piece_to_take = inf
                        for k in _get_nodes_pieces_to_take(position, WHITE):
                            position[k] = NO_PIECE
                            evaluation = _minimax_phase2(position, 3, -inf, inf, True)
                            position[k] = WHITE
                            if evaluation < best_eval_piece_to_take:
                                _best_node_id_to_take = k
                                best_eval_piece_to_take = evaluation
                            if evaluation < best_evaluation:
                                best_node_id_src = i
                                best_node_id_dest = j
                                best_evaluation = evaluation
                    else:
                        evaluation = _minimax_phase2(position, 3, -inf, inf, True)
                        if evaluation < best_evaluation:
                            best_node_id_src = i
                            best_node_id_dest = j
                            best_evaluation = evaluation
                    position[i] = BLACK  # Undo the taking
                    position[j] = NO_PIECE
                    print(f"Checked spot {j} for piece node {i}, evaluation is {evaluation}")
    print(f"Took {default_timer() - start} seconds")
    print(f"Nr. of computations is {computation_count}")
    computation_count = 0

    assert best_node_id_src != -1 and best_node_id_dest != -1  # TODO this assertion failed twice...
    return best_node_id_src, best_node_id_dest


def _get_evaluation_of_position_phase1(position: list) -> int:
    global computation_count
    computation_count += 1

    evaluation = 0

    for node in position:
        if node == WHITE:
            evaluation += weights["piece"]
        elif node == BLACK:
            evaluation -= weights["piece"]

    white_mills, black_mills = _get_number_of_windmills(position)
    for _ in range(white_mills):
        evaluation += weights["mill"]
    for _ in range(black_mills):
        evaluation -= weights["mill"]

    for i, node in enumerate(position):
        if node == WHITE:
            positions = _where_can_go(position, i, 1)
            for node_ in positions.values():
                if node_ == NO_PIECE:
                    evaluation += weights["free_move"]
        elif node == BLACK:
            positions = _where_can_go(position, i, 2)
            for node_ in positions.values():
                if node_ == NO_PIECE:
                    evaluation -= weights["free_move"]

    return evaluation


def _get_evaluation_of_position_phase2(position: list) -> Union[int, float]:
    global computation_count
    computation_count += 1

    white_pieces = 0  # Return absolute value if it's game over TODO maybe should also check if it's blocked
    black_pieces = 0
    for node in position:
        if node == WHITE:
            white_pieces += 1
        elif node == BLACK:
            black_pieces += 1
    if white_pieces == 2:
        return -inf
    elif black_pieces == 2:
        return inf

    evaluation = 0

    for node in position:
        if node == WHITE:
            evaluation += weights["piece"]
        elif node == BLACK:
            evaluation -= weights["piece"]

    white_mills, black_mills = _get_number_of_windmills(position)
    for _ in range(white_mills):
        evaluation += weights["mill"]
    for _ in range(black_mills):
        evaluation -= weights["mill"]

    for i, node in enumerate(position):
        if node == WHITE:
            positions = _where_can_go(position, i, 1)
            for node_ in positions.values():
                if node_ == NO_PIECE:
                    evaluation += weights["free_move"]
        elif node == BLACK:
            positions = _where_can_go(position, i, 2)
            for node_ in positions.values():
                if node_ == NO_PIECE:
                    evaluation -= weights["free_move"]

    return evaluation


def _minimax_phase1(position: list, depth: int, alpha: float, beta: float, maximizing_player: bool) -> int:
    if depth == 0:
        return _get_evaluation_of_position_phase1(position)

    if maximizing_player:
        max_eval = -inf
        for i in NODE_INDICES:
            if position[i] == NO_PIECE:
                position[i] = WHITE  # It's WHITE's turn
                if _check_is_windmill_formed(position, WHITE, i):
                    for j in _get_nodes_pieces_to_take(position, BLACK):
                        position[j] = 0
                        eval = _minimax_phase1(position, depth - 1, alpha, beta, False)
                        position[j] = 2
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            position[i] = NO_PIECE  # Remove the piece before breaking
                            return max_eval
                else:
                    eval = _minimax_phase1(position, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    if beta <= alpha:
                        position[i] = NO_PIECE  # Remove the piece before breaking
                        return max_eval
                position[i] = NO_PIECE
        return max_eval
    else:
        min_eval = inf
        for i in NODE_INDICES:
            if position[i] == NO_PIECE:
                position[i] = BLACK  # It's BLACK's turn
                if _check_is_windmill_formed(position, BLACK, i):
                    for j in _get_nodes_pieces_to_take(position, WHITE):
                        position[j] = NO_PIECE
                        eval = _minimax_phase1(position, depth - 1, alpha, beta, True)
                        position[j] = WHITE
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            position[i] = NO_PIECE  # Remove the piece before breaking
                            return min_eval
                else:
                    eval = _minimax_phase1(position, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        position[i] = NO_PIECE  # Remove the piece before breaking
                        return min_eval
                position[i] = NO_PIECE
        return min_eval


def _minimax_phase2(position: list, depth: int, alpha: float, beta: float, maximizing_player: bool) -> int:
    if depth == 0 or _is_game_over(position):
        return _get_evaluation_of_position_phase2(position)

    if maximizing_player:
        max_eval = -inf
        for i in NODE_INDICES:
            if position[i] == WHITE:
                for j in _where_can_go(position, i, 1):
                    if position[j] == NO_PIECE:
                        position[j] = WHITE
                        position[i] = NO_PIECE
                        if _check_is_windmill_formed(position, WHITE, i):
                            for k in _get_nodes_pieces_to_take(position, BLACK):
                                position[k] = NO_PIECE
                                eval = _minimax_phase2(position, depth - 1, alpha, beta, True)
                                position[k] = BLACK
                                max_eval = max(max_eval, eval)
                                alpha = max(alpha, eval)
                                if beta <= alpha:
                                    position[i] = WHITE  # Do the thing before breaking
                                    position[j] = NO_PIECE
                                    return max_eval
                        else:
                            eval = _minimax_phase2(position, depth - 1, alpha, beta, False)
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                position[i] = WHITE  # Do the thing before breaking
                                position[j] = NO_PIECE
                                return max_eval
                        position[i] = WHITE
                        position[j] = NO_PIECE
        return max_eval
    else:
        min_eval = inf
        for i in NODE_INDICES:
            if position[i] == BLACK:
                for j in _where_can_go(position, i, 2):
                    if position[j] == NO_PIECE:
                        position[j] = BLACK
                        position[i] = NO_PIECE
                        if _check_is_windmill_formed(position, BLACK, i):
                            for k in _get_nodes_pieces_to_take(position, WHITE):
                                position[k] = NO_PIECE
                                eval = _minimax_phase2(position, depth - 1, alpha, beta, True)
                                position[k] = WHITE
                                min_eval = min(min_eval, eval)
                                beta = min(beta, eval)
                                if beta <= alpha:
                                    position[i] = BLACK  # Do the thing before breaking
                                    position[j] = NO_PIECE
                                    return min_eval
                        else:
                            eval = _minimax_phase2(position, depth - 1, alpha, beta, True)
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                position[i] = BLACK  # Do the thing before breaking
                                position[j] = NO_PIECE
                                return min_eval
                        position[i] = BLACK
                        position[j] = NO_PIECE
        return min_eval


def _check_is_windmill_formed(position: list, color: int, node: int) -> bool:
    if position[0] == position[1] == position[2] == color:
        if node == 0 or node == 1 or node == 2:
            return True
    if position[0] == position[9] == position[21] == color:
        if node == 0 or node == 9 or node == 21:
            return True
    if position[21] == position[22] == position[23] == color:
        if node == 21 or node == 22 or node == 23:
            return True
    if position[23] == position[14] == position[2] == color:
        if node == 23 or node == 14 or node == 2:
            return True
    if position[3] == position[4] == position[5] == color:
        if node == 3 or node == 4 or node == 5:
            return True
    if position[3] == position[10] == position[18] == color:
        if node == 3 or node == 10 or node == 18:
            return True
    if position[18] == position[19] == position[20] == color:
        if node == 18 or node == 19 or node == 20:
            return True
    if position[20] == position[13] == position[5] == color:
        if node == 20 or node == 13 or node == 5:
            return True
    if position[6] == position[7] == position[8] == color:
        if node == 6 or node == 7 or node == 8:
            return True
    if position[6] == position[11] == position[15] == color:
        if node == 6 or node == 11 or node == 15:
            return True
    if position[15] == position[16] == position[17] == color:
        if node == 15 or node == 16 or node == 17:
            return True
    if position[17] == position[12] == position[8] == color:
        if node == 17 or node == 12 or node == 8:
            return True
    if position[1] == position[4] == position[7] == color:
        if node == 1 or node == 4 or node == 7:
            return True
    if position[9] == position[10] == position[11] == color:
        if node == 9 or node == 10 or node == 11:
            return True
    if position[22] == position[19] == position[16] == color:
        if node == 22 or node == 19 or node == 16:
            return True
    if position[12] == position[13] == position[14] == color:
        if node == 12 or node == 13 or node == 14:
            return True

    return False


def _where_can_go(position: list, node_id: int, player: int) -> dict:
    """
    Args:
        position (list): The state of the game.
        node_id (int): Id of the node from where to go.
        player (int): PLAYER1 or PLAYER2; for deciding if the player can jump.

    Returns:
        dict: Contains the id of the nodes as the key and the node itself (0, 1 or 2) as the value.

    """
    if player == 1 and not _can_jump(position, 1) or player == 2 and not _can_jump(position, 2):
        if node_id == 0:
            return {1: position[1], 9: position[9]}
        elif node_id == 1:
            return {0: position[0], 2: position[2], 4: position[4]}
        elif node_id == 2:
            return {1: position[1], 14: position[14]}
        elif node_id == 3:
            return {4: position[4], 10: position[10]}
        elif node_id == 4:
            return {1: position[1], 3: position[3], 5: position[5], 7: position[7]}
        elif node_id == 5:
            return {4: position[4], 13: position[13]}
        elif node_id == 6:
            return {7: position[7], 11: position[11]}
        elif node_id == 7:
            return {4: position[4], 6: position[6], 8: position[8]}
        elif node_id == 8:
            return {7: position[7], 12: position[12]}
        elif node_id == 9:
            return {0: position[0], 10: position[10], 21: position[21]}
        elif node_id == 10:
            return {3: position[3], 9: position[9], 11: position[11], 18: position[18]}
        elif node_id == 11:
            return {6: position[6], 10: position[10], 15: position[15]}
        elif node_id == 12:
            return {8: position[8], 13: position[13], 17: position[17]}
        elif node_id == 13:
            return {5: position[5], 12: position[12], 14: position[14], 20: position[20]}
        elif node_id == 14:
            return {2: position[2], 13: position[13], 23: position[23]}
        elif node_id == 15:
            return {11: position[11], 16: position[16]}
        elif node_id == 16:
            return {15: position[15], 17: position[17], 19: position[19]}
        elif node_id == 17:
            return {12: position[12], 16: position[16]}
        elif node_id == 18:
            return {10: position[10], 19: position[19]}
        elif node_id == 19:
            return {16: position[16], 18: position[18], 20: position[20], 22: position[22]}
        elif node_id == 20:
            return {13: position[13], 19: position[19]}
        elif node_id == 21:
            return {9: position[9], 22: position[22]}
        elif node_id == 22:
            return {19: position[19], 21: position[21], 23: position[23]}
        else:
            return {14: position[14], 22: position[22]}
    else:
        nodes = {i: node for i, node in enumerate(position)}
        del nodes[node_id]
        return nodes


def _get_nodes_pieces_to_take(position: list, color: int) -> list:
    """
    Args:
        position (list): The state of the game.
        color (int): The color of the pieces to take.

    Returns:
        list: The id of the nodes.

    """
    windmill_nodes = []
    if position[0] == position[1] == position[2] == color:
        windmill_nodes.append(0)
        windmill_nodes.append(1)
        windmill_nodes.append(2)
    if position[0] == position[9] == position[21] == color:
        windmill_nodes.append(0)
        windmill_nodes.append(9)
        windmill_nodes.append(21)
    if position[21] == position[22] == position[23] == color:
        windmill_nodes.append(21)
        windmill_nodes.append(22)
        windmill_nodes.append(23)
    if position[23] == position[14] == position[2] == color:
        windmill_nodes.append(23)
        windmill_nodes.append(14)
        windmill_nodes.append(2)
    if position[3] == position[4] == position[5] == color:
        windmill_nodes.append(3)
        windmill_nodes.append(4)
        windmill_nodes.append(5)
    if position[3] == position[10] == position[18] == color:
        windmill_nodes.append(3)
        windmill_nodes.append(10)
        windmill_nodes.append(18)
    if position[18] == position[19] == position[20] == color:
        windmill_nodes.append(18)
        windmill_nodes.append(19)
        windmill_nodes.append(20)
    if position[20] == position[13] == position[5] == color:
        windmill_nodes.append(20)
        windmill_nodes.append(13)
        windmill_nodes.append(5)
    if position[6] == position[7] == position[8] == color:
        windmill_nodes.append(6)
        windmill_nodes.append(7)
        windmill_nodes.append(8)
    if position[6] == position[11] == position[15] == color:
        windmill_nodes.append(6)
        windmill_nodes.append(11)
        windmill_nodes.append(15)
    if position[15] == position[16] == position[17] == color:
        windmill_nodes.append(15)
        windmill_nodes.append(16)
        windmill_nodes.append(17)
    if position[17] == position[12] == position[8] == color:
        windmill_nodes.append(17)
        windmill_nodes.append(12)
        windmill_nodes.append(8)
    if position[1] == position[4] == position[7] == color:
        windmill_nodes.append(1)
        windmill_nodes.append(4)
        windmill_nodes.append(7)
    if position[9] == position[10] == position[11] == color:
        windmill_nodes.append(9)
        windmill_nodes.append(10)
        windmill_nodes.append(11)
    if position[22] == position[19] == position[16] == color:
        windmill_nodes.append(22)
        windmill_nodes.append(19)
        windmill_nodes.append(16)
    if position[12] == position[13] == position[14] == color:
        windmill_nodes.append(12)
        windmill_nodes.append(13)
        windmill_nodes.append(14)

    nodes = []
    for i, node in enumerate(position):
        if node == color and i not in windmill_nodes:
            nodes.append(i)

    # If there are no nodes, then they all must be in windmills, so return them all.
    if not nodes:
        return [i for i, node in enumerate(position) if node == color]

    return nodes


def _get_number_of_windmills(position: list) -> tuple:
    white_mills = 0
    black_mills = 0

    if position[0] == position[1] == position[2]:
        if position[0] == WHITE:
            white_mills += 1
        elif position[0] == BLACK:
            black_mills += 1
    if position[0] == position[9] == position[21]:
        if position[0] == WHITE:
            white_mills += 1
        elif position[0] == BLACK:
            black_mills += 1
    if position[21] == position[22] == position[23]:
        if position[21] == WHITE:
            white_mills += 1
        elif position[21] == BLACK:
            black_mills += 1
    if position[23] == position[14] == position[2]:
        if position[23] == WHITE:
            white_mills += 1
        elif position[23] == BLACK:
            black_mills += 1
    if position[3] == position[4] == position[5]:
        if position[3] == WHITE:
            white_mills += 1
        elif position[3] == BLACK:
            black_mills += 1
    if position[3] == position[10] == position[18]:
        if position[3] == WHITE:
            white_mills += 1
        elif position[3] == BLACK:
            black_mills += 1
    if position[18] == position[19] == position[20]:
        if position[18] == WHITE:
            white_mills += 1
        elif position[18] == BLACK:
            black_mills += 1
    if position[20] == position[13] == position[5]:
        if position[20] == WHITE:
            white_mills += 1
        elif position[20] == BLACK:
            black_mills += 1
    if position[6] == position[7] == position[8]:
        if position[6] == WHITE:
            white_mills += 1
        elif position[6] == BLACK:
            black_mills += 1
    if position[6] == position[11] == position[15]:
        if position[6] == WHITE:
            white_mills += 1
        elif position[6] == BLACK:
            black_mills += 1
    if position[15] == position[16] == position[17]:
        if position[15] == WHITE:
            white_mills += 1
        elif position[15] == BLACK:
            black_mills += 1
    if position[17] == position[12] == position[8]:
        if position[17] == WHITE:
            white_mills += 1
        elif position[17] == BLACK:
            black_mills += 1
    if position[1] == position[4] == position[7]:
        if position[1] == WHITE:
            white_mills += 1
        elif position[1] == BLACK:
            black_mills += 1
    if position[9] == position[10] == position[11]:
        if position[9] == WHITE:
            white_mills += 1
        elif position[9] == BLACK:
            black_mills += 1
    if position[22] == position[19] == position[16]:
        if position[22] == WHITE:
            white_mills += 1
        elif position[22] == BLACK:
            black_mills += 1
    if position[12] == position[13] == position[14]:
        if position[12] == WHITE:
            white_mills += 1
        elif position[12] == BLACK:
            black_mills += 1

    return white_mills, black_mills


def _is_game_over(position: list) -> bool:  # TODO check if player is blocked; better make a "check player" method
    black_pieces = 0
    white_pieces = 0
    for node in position:
        if node == WHITE:
            white_pieces += 1
        elif node == BLACK:
            black_pieces += 1

    if white_pieces < 3 or black_pieces < 3:  # Test if player has no more pieces
        return True

    for i in NODE_INDICES:  # Test if player has any moves to make
        if position[i] == WHITE:
            white_can_go = _where_can_go(position, i, 1)
            if not all(map(lambda node: node != NO_PIECE, white_can_go.values())):
                return False
        elif position[i] == BLACK:
            black_can_go = _where_can_go(position, i, 2)
            if not all(map(lambda node: node != NO_PIECE, black_can_go.values())):
                return False

    return True


def _can_jump(position: list, player: int) -> bool:
    if player == 1:
        white_pieces = 0
        for node in position:
            if node == WHITE:
                white_pieces += 1
        if white_pieces == 3:
            return True
    else:
        black_pieces = 0
        for node in position:
            if node == BLACK:
                black_pieces += 1
        if black_pieces == 3:
            return True

    return False
