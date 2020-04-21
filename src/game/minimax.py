from math import inf
from timeit import default_timer
from copy import copy

from src.constants import *

# Assume maximizing player is WHITE and minimizing player is BLACK.
# For now the AI is always BLACK.

values = {
    "mill": 8,
    "piece": 9,
    "free_move": 1
}

best_node_id_to_take = -1
computation_count = 0


def ai_place_piece_at(position: list) -> int:
    """
    Args:
        position (list): The state of the game.

    Returns:
        int: The id of the node on which to put the piece.

    """
    global computation_count, best_node_id_to_take
    best_evaluation = inf  # BLACK searches for the lowest evaluation!!!
    best_node_id = -1

    start = default_timer()
    for i, node in enumerate(position[0:23]):
        if node == 0:  # If there is no piece
            position[i] = 2  # Put a BLACK piece
            if _check_is_windmill_formed(position, 2, i):
                best_eval_piece_to_take = inf
                for j, node_ in enumerate(_get_nodes_pieces_to_take(position, 1)):
                    position[j] = 0
                    evaluation = minimax_phase1(position, 3, -inf, inf, True)
                    position[j] = 1
                    if evaluation < best_eval_piece_to_take:
                        best_node_id_to_take = j
                        best_eval_piece_to_take = evaluation
                    if evaluation < best_evaluation:
                        best_node_id = i
                        best_evaluation = evaluation
            else:
                evaluation = minimax_phase1(position, 3, -inf, inf, True)  # It's maximizing player now, because we just put
                if evaluation < best_evaluation:                           # a black piece
                    best_node_id = i
                    best_evaluation = evaluation
            position[i] = 0  # Undo the placement
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
    global best_node_id_to_take
    assert best_node_id_to_take != -1
    id = best_node_id_to_take
    best_node_id_to_take = -1
    return id


def ai_move_piece(position: list) -> tuple:
    """
    Args:
        position (list): The state of the game.

    Returns:
        tuple: The id of the source and destinantion nodes.

    """
    global computation_count, best_node_id_to_take
    best_evaluation = inf
    best_node_id_src = -1
    best_node_id_dest = -1

    start = default_timer()
    for i, node in enumerate(position[0:23]):
        if node == 2:
            for node_, j in _where_can_go(position, i, 2).items():
                if node_ == 0:
                    position[j] = 2
                    position[i] = 0
                    if _check_is_windmill_formed(position, 2, j):
                        best_eval_piece_to_take = inf
                        for k, node__ in enumerate(_get_nodes_pieces_to_take(position, 1)):
                            position[k] = 0
                            evaluation = minimax_phase2(position, 3, -inf, inf, True)
                            position[k] = 1
                            if evaluation < best_eval_piece_to_take:
                                best_node_id_to_take = k
                                best_eval_piece_to_take = evaluation
                            if evaluation < best_evaluation:
                                best_node_id_src = i
                                best_node_id_dest = j
                                best_evaluation = evaluation
                    else:
                        evaluation = minimax_phase2(position, 3, -inf, inf, True)
                        if evaluation < best_evaluation:
                            best_node_id_src = i
                            best_node_id_dest = j
                            best_evaluation = evaluation
                    position[i] = 2  # Undo the taking
                    position[j] = 0
                    print(f"Checked spot {j} for piece node {i}, evaluation is {evaluation}")
    print(f"Took {default_timer() - start} seconds")
    print(f"Nr. of computations is {computation_count}")
    computation_count = 0

    assert best_node_id_src != -1 and best_node_id_dest != -1
    return best_node_id_src, best_node_id_dest


def get_evaluation_of_position(position: list) -> int:
    global computation_count
    computation_count += 1

    evaluation = 0

    for node in position[0:23]:
        if node == 1:  # Piece is WHITE
            evaluation += values["piece"]
        elif node == 2:  # Piece is BLACK
            evaluation -= values["piece"]

    white_mills, black_mills = _get_number_of_windmills(position)
    for _ in range(white_mills):
        evaluation += values["mill"]
    for _ in range(black_mills):
        evaluation -= values["mill"]

    for i, node in enumerate(position[0:23]):
        if node == 1:
            positions = _where_can_go(position, i, 1)
            for node_ in positions.keys():
                if node_ == 0:
                    evaluation += values["free_move"]
        elif node == 2:
            positions = _where_can_go(position, i, 2)
            for node_ in positions.keys():
                if node_ == 0:
                    evaluation -= values["free_move"]

    return evaluation


def minimax_phase1(position: list, depth: int, alpha: float, beta: float, maximizing_player: bool) -> int:
    if depth == 0:
        return get_evaluation_of_position(position)

    if maximizing_player:
        max_eval = -inf
        for i, node in enumerate(position[0:23]):
            if node == 0:
                position[i] = 1  # It's WHITE's turn
                if _check_is_windmill_formed(position, 1, i):
                    for j, node_ in enumerate(_get_nodes_pieces_to_take(position, 2)):
                        position[j] = 0
                        eval = minimax_phase1(position, depth - 1, alpha, beta, False)
                        position[j] = 2
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            position[i] = 0  # Remove the piece before breaking
                            return max_eval
                else:
                    eval = minimax_phase1(position, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    if beta <= alpha:
                        position[i] = 0  # Remove the piece before breaking
                        return max_eval
                position[i] = 0
        return max_eval
    else:
        min_eval = inf
        for i, node in enumerate(position[0:23]):
            if node == 0:
                position[i] = 2  # It's BLACK's turn
                if _check_is_windmill_formed(position, 2, i):
                    for j, node_ in enumerate(_get_nodes_pieces_to_take(position, WHITE)):
                        position[j] = 0
                        eval = minimax_phase1(position, depth - 1, alpha, beta, True)
                        position[j] = 1
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            position[i] = 0  # Remove the piece before breaking
                            return min_eval
                else:
                    eval = minimax_phase1(position, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        position[i] = 0  # Remove the piece before breaking
                        return min_eval
                position[i] = 0
        return min_eval


def minimax_phase2(position: list, depth: int, alpha: float, beta: float, maximizing_player: bool) -> int:
    if depth == 0 or _is_game_over(position):
        return get_evaluation_of_position(position)

    if maximizing_player:
        max_eval = -inf
        for i, node in enumerate(position[0:23]):
            if node == 1:
                for node_, j in _where_can_go(position, i, 1).items():
                    if node_ == 0:
                        position[j] = 1
                        position[i] = 0
                        if _check_is_windmill_formed(position, 1, i):
                            for k, node__ in enumerate(_get_nodes_pieces_to_take(position, BLACK)):
                                position[k] = 0
                                eval = minimax_phase2(position, depth - 1, alpha, beta, True)
                                position[k] = 2
                                max_eval = max(max_eval, eval)
                                alpha = max(alpha, eval)
                                if beta <= alpha:
                                    position[i] = 1  # Do the thing before breaking
                                    position[j] = 0
                                    return max_eval
                        else:
                            eval = minimax_phase2(position, depth - 1, alpha, beta, False)
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                position[i] = 1  # Do the thing before breaking
                                position[j] = 0
                                return max_eval
                        position[i] = 1
                        position[j] = 0
        return max_eval
    else:
        min_eval = inf
        for i, node in enumerate(position[0:23]):
            if node == 2:
                for node_, j in _where_can_go(position, i, 2).items():
                    if node_ == 0:
                        position[j] = 2
                        position[i] = 0
                        if _check_is_windmill_formed(position, 2, i):
                            for k, node__ in enumerate(_get_nodes_pieces_to_take(position, WHITE)):
                                position[k] = 0
                                eval = minimax_phase2(position, depth - 1, alpha, beta, True)
                                position[k] = 1
                                min_eval = min(min_eval, eval)
                                beta = min(beta, eval)
                                if beta <= alpha:
                                    position[i] = 2  # Do the thing before breaking
                                    position[j] = 0
                                    return min_eval
                        else:
                            eval = minimax_phase2(position, depth - 1, alpha, beta, True)
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                position[i] = 2  # Do the thing before breaking
                                position[j] = 0
                                return min_eval
                        position[i] = 2
                        position[j] = 0
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


def _where_can_go(position: list, node: int, player: int) -> dict:
    if player == 1 and not position[-2] or player == 2 and not position[-1]:  # TODO the can_jump variables must be set
        if node == 0:
            return {position[1]: 1, position[9]: 9}  # The key is the node and the value is the id, which is weird
        elif node == 1:
            return {position[0]: 0, position[2]: 2, position[4]: 4}
        elif node == 2:
            return {position[1]: 1, position[14]: 14}
        elif node == 3:
            return {position[4]: 4, position[10]: 10}
        elif node == 4:
            return {position[1]: 1, position[3]: 3, position[5]: 5, position[7]: 7}
        elif node == 5:
            return {position[4]: 4, position[13]: 13}
        elif node == 6:
            return {position[7]: 7, position[11]: 11}
        elif node == 7:
            return {position[4]: 4, position[6]: 6, position[8]: 8}
        elif node == 8:
            return {position[7]: 7, position[12]: 12}
        elif node == 9:
            return {position[0]: 0, position[10]: 10, position[21]: 21}
        elif node == 10:
            return {position[3]: 3, position[9]: 9, position[11]: 11, position[18]: 18}
        elif node == 11:
            return {position[6]: 6, position[10]: 10, position[15]: 15}
        elif node == 12:
            return {position[8]: 8, position[13]: 13, position[17]: 17}
        elif node == 13:
            return {position[5]: 5, position[12]: 12, position[14]: 14, position[20]: 20}
        elif node == 14:
            return {position[2]: 2, position[13]: 13, position[23]: 23}
        elif node == 15:
            return {position[11]: 11, position[16]: 16}
        elif node == 16:
            return {position[15]: 15, position[17]: 17, position[19]: 19}
        elif node == 17:
            return {position[12]: 12, position[16]: 16}
        elif node == 18:
            return {position[10]: 10, position[19]: 19}
        elif node == 19:
            return {position[16]: 16, position[18]: 18, position[20]: 20, position[22]: 22}
        elif node == 20:
            return {position[13]: 13, position[19]: 19}
        elif node == 21:
            return {position[9]: 9, position[22]: 22}
        elif node == 22:
            return {position[19]: 19, position[21]: 21, position[23]: 23}
        else:
            return {position[14]: 14, position[22]: 22}
    else:
        nodes = copy(position[0:23])
        del nodes[node]
        return {node: i for i, node in enumerate(nodes)}


def _get_nodes_pieces_to_take(position: list, color: int) -> list:
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
    for i, node in enumerate(position[0:23]):
        if node == color and i not in windmill_nodes:
            nodes.append(i)

    # If there are no nodes, then they all must be in windmills, so return them all.
    if not nodes:
        return [node for node in position[0:23] if node == color]

    return nodes


def _get_number_of_windmills(position: list) -> tuple:
    white_mills = 0
    black_mills = 0

    if position[0] == position[1] == position[2]:
        if position[0] == 1:
            white_mills += 1
        elif position[0] == 2:
            black_mills += 1
    if position[0] == position[9] == position[21]:
        if position[0] == 1:
            white_mills += 1
        elif position[0] == 2:
            black_mills += 1
    if position[21] == position[22] == position[23]:
        if position[21] == 1:
            white_mills += 1
        elif position[21] == 2:
            black_mills += 1
    if position[23] == position[14] == position[2]:
        if position[23] == 1:
            white_mills += 1
        elif position[23] == 2:
            black_mills += 1
    if position[3] == position[4] == position[5]:
        if position[3] == 1:
            white_mills += 1
        elif position[3] == 2:
            black_mills += 1
    if position[3] == position[10] == position[18]:
        if position[3] == 1:
            white_mills += 1
        elif position[3] == 2:
            black_mills += 1
    if position[18] == position[19] == position[20]:
        if position[18] == 1:
            white_mills += 1
        elif position[18] == 2:
            black_mills += 1
    if position[20] == position[13] == position[5]:
        if position[20] == 1:
            white_mills += 1
        elif position[20] == 2:
            black_mills += 1
    if position[6] == position[7] == position[8]:
        if position[6] == 1:
            white_mills += 1
        elif position[6] == 2:
            black_mills += 1
    if position[6] == position[11] == position[15]:
        if position[6] == 1:
            white_mills += 1
        elif position[6] == 2:
            black_mills += 1
    if position[15] == position[16] == position[17]:
        if position[15] == 1:
            white_mills += 1
        elif position[15] == 2:
            black_mills += 1
    if position[17] == position[12] == position[8]:
        if position[17] == 1:
            white_mills += 1
        elif position[17] == 2:
            black_mills += 1
    if position[1] == position[4] == position[7]:
        if position[1] == 1:
            white_mills += 1
        elif position[1] == 2:
            black_mills += 1
    if position[9] == position[10] == position[11]:
        if position[9] == 1:
            white_mills += 1
        elif position[9] == 2:
            black_mills += 1
    if position[22] == position[19] == position[16]:
        if position[22] == 1:
            white_mills += 1
        elif position[22] == 2:
            black_mills += 1
    if position[12] == position[13] == position[14]:
        if position[12] == 1:
            white_mills += 1
        elif position[12] == 2:
            black_mills += 1

    return white_mills, black_mills


def _is_game_over(position: list) -> bool:  # TODO check if player is blocked; better make a "check player" method
    black_pieces = 0
    white_pieces = 0
    for node in position[0:23]:
        if node == 1:
            white_pieces += 1
        elif node == 2:
            black_pieces += 1

    if white_pieces < 3 or black_pieces < 3:
        return True
    else:
        return False
