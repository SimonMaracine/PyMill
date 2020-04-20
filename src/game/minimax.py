from math import inf
from timeit import default_timer

from src.constants import *
from src.game.piece import Piece
from src.game.board import Board

# Assume maximizing player is WHITE and minimizing player is BLACK.
# For now the AI is always BLACK.

values = {
    "mill": 8,
    "piece": 9,
    "free_move": 1
}

best_node_id_to_take = -1
computation_count = 0


def ai_place_piece_at(position: Board) -> int:
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
    for node in position.nodes:
        if node.piece is None:  # If there is no piece
            node.piece = Piece(node.x, node.y, BLACK)  # Put a BLACK piece
            if position.check_is_windmill_formed(BLACK, node):
                best_eval_piece_to_take = inf
                for node_ in _get_nodes_pieces_to_take(position, WHITE):
                    node_.piece = None
                    evaluation = minimax_phase1(position, 3, -inf, inf, True)
                    node_.piece = Piece(node_.x, node_.y, WHITE)
                    if evaluation < best_eval_piece_to_take:
                        best_node_id_to_take = node_.id
                        best_eval_piece_to_take = evaluation
                    if evaluation < best_evaluation:
                        best_node_id = node.id
                        best_evaluation = evaluation
            else:
                evaluation = minimax_phase1(position, 3, -inf, inf, True)  # It's maximizing player now, because we just put
                if evaluation < best_evaluation:                           # a black piece
                    best_node_id = node.id
                    best_evaluation = evaluation
            node.piece = None  # Undo the placement
            print(f"Checked spot {node.id}, evaluation is {evaluation}")
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


def ai_move_piece(position: Board) -> tuple:
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
    for node in position.nodes:
        if node.piece is not None and node.piece.color == BLACK:
            for node_ in position._where_can_go(node):
                if node_.piece is None:
                    node_.piece = Piece(node_.x, node_.y, BLACK)
                    node.piece = None
                    if position.check_is_windmill_formed(BLACK, node_):
                        best_eval_piece_to_take = inf
                        for node__ in _get_nodes_pieces_to_take(position, WHITE):
                            node__.piece = None
                            evaluation = minimax_phase2(position, 3, -inf, inf, True)
                            node__.piece = Piece(node__.x, node__.y, WHITE)
                            if evaluation < best_eval_piece_to_take:
                                best_node_id_to_take = node__.id
                                best_eval_piece_to_take = evaluation
                            if evaluation < best_evaluation:
                                best_node_id_src = node.id
                                best_node_id_dest = node_.id
                                best_evaluation = evaluation
                    else:
                        evaluation = minimax_phase2(position, 3, -inf, inf, True)
                        if evaluation < best_evaluation:
                            best_node_id_src = node.id
                            best_node_id_dest = node_.id
                            best_evaluation = evaluation
                    node.piece = Piece(node.x, node.y, BLACK)  # Undo the taking
                    node_.piece = None
                    print(f"Checked spot {node_.id} for piece node {node.id}, evaluation is {evaluation}")
    print(f"Took {default_timer() - start} seconds")
    print(f"Nr. of computations is {computation_count}")
    computation_count = 0

    assert best_node_id_src != -1 and best_node_id_dest != -1
    return best_node_id_src, best_node_id_dest


def get_evaluation_of_position(position: Board) -> int:
    global computation_count
    computation_count += 1

    evaluation = 0

    for node in position.nodes:
        if node.piece is not None:
            if node.piece.color == WHITE:  # Piece is WHITE
                evaluation += values["piece"]
            else:  # Piece is BLACK
                evaluation -= values["piece"]

    white_mills, black_mills = _get_number_of_windmills(position)
    for _ in range(white_mills):
        evaluation += values["mill"]
    for _ in range(black_mills):
        evaluation -= values["mill"]

    for node in position.nodes:
        if node.piece is not None:
            if node.piece.color == WHITE:
                positions = position._where_can_go(node)
                for node_ in positions:
                    if node_.piece is None:
                        evaluation += values["free_move"]
            else:
                positions = position._where_can_go(node)
                for node_ in positions:
                    if node_.piece is None:
                        evaluation -= values["free_move"]

    return evaluation


def minimax_phase1(position: Board, depth: int, alpha: float, beta: float, maximizing_player: bool) -> int:
    if depth == 0:
        return get_evaluation_of_position(position)

    if maximizing_player:
        max_eval = -inf
        for node in position.nodes:
            if node.piece is None:
                node.piece = Piece(node.x, node.y, WHITE)  # It's WHITE's turn
                if position.check_is_windmill_formed(WHITE, node):
                    for node_ in _get_nodes_pieces_to_take(position, BLACK):
                        node_.piece = None
                        eval = minimax_phase1(position, depth - 1, alpha, beta, False)
                        node_.piece = Piece(node_.x, node_.y, BLACK)
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            node.piece = None  # Remove the piece before breaking
                            return max_eval
                else:
                    eval = minimax_phase1(position, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    if beta <= alpha:
                        node.piece = None  # Remove the piece before breaking
                        return max_eval
                node.piece = None
        return max_eval
    else:
        min_eval = inf
        for node in position.nodes:
            if node.piece is None:
                node.piece = Piece(node.x, node.y, BLACK)  # It's BLACK's turn
                if position.check_is_windmill_formed(BLACK, node):
                    for node_ in _get_nodes_pieces_to_take(position, WHITE):
                        node_.piece = None
                        eval = minimax_phase1(position, depth - 1, alpha, beta, True)
                        node_.piece = Piece(node_.x, node_.y, WHITE)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            node.piece = None  # Remove the piece before breaking
                            return min_eval
                else:
                    eval = minimax_phase1(position, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        node.piece = None  # Remove the piece before breaking
                        return min_eval
                node.piece = None
        return min_eval


def minimax_phase2(position: Board, depth: int, alpha: float, beta: float, maximizing_player: bool) -> int:
    if depth == 0 or _is_game_over(position):
        return get_evaluation_of_position(position)

    if maximizing_player:
        max_eval = -inf
        for node in position.nodes:
            if node.piece is not None and node.piece.color == WHITE:
                for node_ in position._where_can_go(node):
                    if node_.piece is None:
                        node_.piece = Piece(node_.x, node_.y, WHITE)
                        node.piece = None
                        if position.check_is_windmill_formed(WHITE, node):
                            for node__ in _get_nodes_pieces_to_take(position, BLACK):
                                node__.piece = None
                                eval = minimax_phase2(position, depth - 1, alpha, beta, True)
                                node__.piece = Piece(node__.x, node__.y, BLACK)
                                max_eval = max(max_eval, eval)
                                alpha = max(alpha, eval)
                                if beta <= alpha:
                                    node.piece = Piece(node.x, node.y, WHITE)  # Do the thing before breaking
                                    node_.piece = None
                                    return max_eval
                        else:
                            eval = minimax_phase2(position, depth - 1, alpha, beta, False)
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                node.piece = Piece(node.x, node.y, WHITE)  # Do the thing before breaking
                                node_.piece = None
                                return max_eval
                        node.piece = Piece(node.x, node.y, WHITE)
                        node_.piece = None
        return max_eval
    else:
        min_eval = inf
        for node in position.nodes:
            if node.piece is not None and node.piece.color == BLACK:
                for node_ in position._where_can_go(node):
                    if node_.piece is None:
                        node_.piece = Piece(node_.x, node_.y, BLACK)
                        node.piece = None
                        if position.check_is_windmill_formed(BLACK, node):
                            for node__ in _get_nodes_pieces_to_take(position, WHITE):
                                node__.piece = None
                                eval = minimax_phase2(position, depth - 1, alpha, beta, True)
                                node__.piece = Piece(node__.x, node__.y, WHITE)
                                min_eval = min(min_eval, eval)
                                beta = min(beta, eval)
                                if beta <= alpha:
                                    node.piece = Piece(node.x, node.y, BLACK)  # Do the thing before breaking
                                    node_.piece = None
                                    return min_eval
                        else:
                            eval = minimax_phase2(position, depth - 1, alpha, beta, True)
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                node.piece = Piece(node.x, node.y, BLACK)  # Do the thing before breaking
                                node_.piece = None
                                return min_eval
                        node.piece = Piece(node.x, node.y, BLACK)
                        node_.piece = None
        return min_eval


def _get_nodes_pieces_to_take(position: Board, color: tuple) -> list:
    windmill_nodes = []
    for windmill in position.windmills:
        if position._check_nodes_for_windmill(windmill, color):
            windmill_nodes.append(windmill[0])
            windmill_nodes.append(windmill[1])
            windmill_nodes.append(windmill[2])

    nodes = []
    for node in position.nodes:
        if node.piece is not None and node.piece.color == color and node not in windmill_nodes:
            nodes.append(node)

    # If there are no nodes, then they all must be in windmills, so return them all.
    if not nodes:
        return [node for node in position.nodes if node.piece is not None and node.piece.color == color]

    return nodes


def _get_number_of_windmills(position: Board) -> tuple:
    white_mills = 0
    black_mills = 0

    for windmill in position.windmills:
        if all(map(lambda node: node.piece is not None and node.piece.color == WHITE, windmill)):
            white_mills += 1
        if all(map(lambda node: node.piece is not None and node.piece.color == BLACK, windmill)):
            black_mills += 1

    return white_mills, black_mills


def _is_game_over(position: Board) -> bool:
    black_pieces = 0
    white_pieces = 0
    for node in position.nodes:
        if node.piece is not None:
            if node.piece.color == WHITE:
                white_pieces += 1
            else:
                black_pieces += 1

    if white_pieces < 3 or black_pieces < 3:
        return True
    else:
        return False
