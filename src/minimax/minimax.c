#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdio.h>
#include <assert.h>
#include <limits.h>
#include "helpers.h"

#define NO_PIECE 0
#define WHITE 1
#define BLACK 2

#define WEIGHT_MILL 20
#define WEIGHT_PIECE 24
#define WEIGHT_FREE_MOVE 1

int _best_node_id_to_take = -1;
int computation_count = 0;


int ai_place_piece_at(int* position) {
	int best_evaluation = INT_MAX;
	int best_node_id = -1;

	for (int i = 0; i < 24; i++) {
		if (position[i] == NO_PIECE) {
			position[i] = BLACK;
			int evaluation;
			if (_check_is_windmill_formed(position, BLACK, i)) {
				int best_eval_piece_to_take = INT_MAX;
				List pieces_to_take = _get_nodes_pieces_to_take(position, WHITE);
				for (int j = 0; j < pieces_to_take.count; j++) {
					int j_ = pieces_to_take.items[j];
					position[j_] = NO_PIECE;
					evaluation = _minimax_phase1(position, 3, INT_MIN, INT_MAX, 1);
					position[j_] = WHITE;
					if (evaluation < best_eval_piece_to_take) {
						_best_node_id_to_take = j_;
						best_eval_piece_to_take = evaluation;
					}
					if (evaluation < best_evaluation) {
						best_node_id = i;
						best_evaluation = evaluation;
					}
				}
			} else {
				evaluation = _minimax_phase1(position, 3, INT_MIN, INT_MAX, 1);
				if (evaluation < best_evaluation) {
					best_node_id = i;
					best_evaluation = evaluation;
				}
			}
			position[i] = NO_PIECE;
			printf("Checked spot %d, evaluation is %d\n", i, evaluation);
		}
	}
	printf("Nr. of computations is %d\n", computation_count);
	computation_count = 0;

	assert(best_node_id != -1);
	return best_node_id;
}


int ai_remove_piece() {
	assert(_best_node_id_to_take != -1);
	int id = _best_node_id_to_take;
	_best_node_id_to_take = -1;
	return id;
}


Tuple ai_move_piece(int* position) {
	int best_evaluation = INT_MAX;
	int best_nodes_id_src = -1;
	int best_nodes_id_dest = -1;

	for (int i = 0; i < 24; i++) {
		if (position[i] == BLACK) {
			Dict where_can_go = _where_can_go(position, i, 2);
			for (int j = 0; j < where_can_go.count; j++) {
				int j_ = where_can_go.keys[j];
				if (position[j_] == NO_PIECE) {
					position[j_] = BLACK;
					position[i] = NO_PIECE;
					int evaluation;
					if (_check_is_windmill_formed(position, BLACK, j_)) {
						int best_eval_piece_to_take = INT_MAX;
						List pieces_to_take = _get_nodes_pieces_to_take(position, WHITE);
						for (int k = 0; k < pieces_to_take.count; k++) {
							int k_ = pieces_to_take.items[k];
							position[k_] = NO_PIECE;
							evaluation = _minimax_phase2(position, 3, INT_MIN, INT_MAX, 1);
							position[k_] = WHITE;
							if (evaluation < best_eval_piece_to_take) {
								_best_node_id_to_take = k_;
								best_eval_piece_to_take = evaluation;
							}
							if (evaluation < best_evaluation) {
								best_nodes_id_src = i;
								best_nodes_id_dest = j_;
								best_evaluation = evaluation;
							}
						}
					} else {
						evaluation = _minimax_phase2(position, 3, INT_MIN, INT_MAX, 1);
						if (evaluation < best_evaluation) {
							best_nodes_id_src = i;
							best_nodes_id_dest = j_;
							best_evaluation = evaluation;
						}
					}
					position[i] = BLACK;
					position[j_] = NO_PIECE;
					printf("Checked spot %d for piece node %d, evaluation is %d\n", j_, i, evaluation);
				}
			}
		}
	}
	printf("Nr. of computations is %d\n", computation_count);
	computation_count = 0;

	assert(best_node_id_src != -1 || best_node_id_dest != -1);
	Tuple t;
	t.a = best_node_id_src;
	t.b = best_node_id_dest;
	return t;
}


int _get_evaluation_of_position_phase1(int* position) {
	computation_count++;

	int evaluation = 0;

	for (int i = 0; i < 24; i++) {
		if (position[i] == WHITE)
			evaluation += WEIGHT_PIECE;
		else if (position[i] == BLACK)
			evaluation -= WEIGHT_PIECE;
	}

	Tuple white_and_black_mills = _get_number_of_windmills(position);

	for (int i = 0; i < white_and_black_mills.a; i++)
		evaluation += WEIGHT_MILL;
	for (int i = 0; i < white_and_black_mills.b; i++)
		evaluation -= WEIGHT_MILL;

	for (int i = 0; i < 24; i++) {
		if (position[i] == WHITE) {
			Dict positions = _where_can_go(position, i, 1);

			for (int j = 0; j < positions.count; j++) {
				if (positions.values[j] == NO_PIECE)
					evaluation += WEIGHT_FREE_MOVE;
			}
		} else if (position[i] == BLACK) {
			Dict positions = _where_can_go(position, i, 2);

			for (int j = 0; j < positions.count; j++) {
				if (positions.values[j] == NO_PIECE)
					evaluation -= WEIGHT_FREE_MOVE;
			}
		}
	}

	return evaluation;
}


int _get_evaluation_of_position_phase2(int* position) {
	computation_count++;

	int white_pieces = 0;
	int black_pieces = 0;
	for (int i = 0; i < 24; i++) {
		if (position[i] == WHITE)
			white_pieces++;
		else if (position[i] == BLACK)
			black_pieces++;
	}
	if (white_pieces == 2)
		return INT_MIN;
	else if (black_pieces == 2)
		return INT_MAX;

	int evaluation = 0;

	for (int i = 0; i < 24; i++) {
		if (position[i] == WHITE)
			evaluation += WEIGHT_PIECE;
		else if (position[i] == BLACK)
			evaluation -= WEIGHT_PIECE;
	}

	Tuple white_and_black_mills = _get_number_of_windmills(position);

	for (int i = 0; i < white_and_black_mills.a; i++)
		evaluation += WEIGHT_MILL;
	for (int i = 0; i < white_and_black_mills.b; i++)
		evaluation -= WEIGHT_MILL;

	for (int i = 0; i < 24; i++) {
		if (position[i] == WHITE) {
			Dict positions = _where_can_go(position, i, 1);

			for (int j = 0; j < positions.count; j++) {
				if (positions.values[j] == NO_PIECE)
					evaluation += WEIGHT_FREE_MOVE;
			}
		} else if (position[i] == BLACK) {
			Dict positions = _where_can_go(position, i, 2);

			for (int j = 0; j < positions.count; j++) {
				if (positions.values[j] == NO_PIECE)
					evaluation -= WEIGHT_FREE_MOVE;
			}
		}
	}

	return evaluation;
}


int _minimax_phase1(int* position, int depth, int alpha, int beta, int maximizing_player) {
	if (depth == 0)
		return _get_evaluation_of_position_phase1(position);

	if (maximizing_player) {
		int max_eval = INT_MIN;
		for (int i = 0; i < 24; i++) {
			if (position[i] == NO_PIECE) {
				position[i] = WHITE;
				if (_check_is_windmill_formed(position, WHITE, i)) {
					List pieces_to_take = _get_nodes_pieces_to_take(position, BLACK);
					for (int j = 0; j < pieces_to_take.count; j++) {
						int j_ = pieces_to_take.items[j];
						position[j_] = NO_PIECE;
						int eval = _minimax_phase1(position, depth - 1, alpha, beta, 0);
						position[j_] = BLACK;
						max_eval = MAX(max_eval, eval);
						int new_alpha = MAX(alpha, eval);
						if (beta <= new_alpha) {
							position[i] = NO_PIECE;
							return max_eval;
						}
					}
				} else {
					int eval = _minimax_phase1(position, depth - 1, alpha, beta, 0);
					max_eval = MAX(max_eval, eval);
					int new_alpha = MAX(alpha, eval);
					if (beta <= new_alpha) {
						position[i] = NO_PIECE;
						return max_eval;
					}
				}
				position[i] = NO_PIECE;
			}
		}
		return max_eval;
	} else {
		int min_eval = INT_MAX;
		for (int i = 0; i < 24; i++) {
			if (position[i] == NO_PIECE) {
				position[i] = BLACK;
				if (_check_is_windmill_formed(position, BLACK, i)) {
					List pieces_to_take = _get_nodes_pieces_to_take(position, WHITE);
					for (int j = 0; j < pieces_to_take.count; j++) {
						int j_ = pieces_to_take.items[j];
						position[j_] = NO_PIECE;
						int eval = _minimax_phase1(position, depth - 1, alpha, beta, 1);
						position[j_] = WHITE;
						min_eval = MIN(min_eval, eval);
						int new_beta = MIN(beta, eval);
						if (new_beta <= alpha) {
							position[i] = NO_PIECE;
							return min_eval;
						}
					}
				} else {
					int eval = _minimax_phase1(position, depth - 1, alpha, beta, 1);
					min_eval = MIN(min_eval, eval);
					int new_beta = MIN(beta, eval);
					if (new_beta <= alpha) {
						position[i] = NO_PIECE;
						return min_eval;
					}
				}
				position[i] = NO_PIECE;
			}
		}
		return min_eval;
	}
}


int _minimax_phase2(int* position, int depth, int alpha, int beta, int maximizing_player) {
	if (depth == 0 || _is_game_over(position))
		return _get_evaluation_of_position_phase2(position);

	if (maximizing_player) {
		int max_eval = INT_MIN;
		for (int i = 0; i < 24; i++) {
			if (position[i] == WHITE) {
				Dict where_can_go = _where_can_go(position, i, 1);
				for (int j = 0; j < where_can_go.count; j++) {
					int j_ = where_can_go.keys[j];
					if (position[j_] == NO_PIECE) {
						position[j_] = WHITE;
						position[i] = NO_PIECE;
						if (_check_is_windmill_formed(position, WHITE, i)) {
							List pieces_to_take = _get_nodes_pieces_to_take(position, BLACK);
							for (int k = 0; k < pieces_to_take.count; k++) {
								int k_ = pieces_to_take.items[k];
								position[k_] = NO_PIECE;
								int eval = _minimax_phase2(position, depth - 1, alpha, beta, 0);
								position[k_] = BLACK;
								max_eval = MAX(max_eval, eval);
								int new_alpha = MAX(alpha, eval);
								if (beta <= new_alpha) {
									position[i] = WHITE;
									position[j_] = NO_PIECE;
									return max_eval;
								}
							}
						} else {
							int eval = _minimax_phase2(position, depth - 1, alpha, beta, 0);
							max_eval = MAX(max_eval, eval);
							int new_alpha = MAX(alpha, eval);
							if (beta <= new_alpha) {
								position[i] = WHITE;
								position[j_] = NO_PIECE;
								return max_eval
							}
						}
						position[i] = WHITE;
						position[j_] = NO_PIECE;
					}
				}
			}
		}
		return max_eval;
	} else {
		int min_eval = INT_MAX;
		for (int i = 0; i < 24; i++) {
			if (position[i] == BLACK) {
				Dict where_can_go = _where_can_go(position, i, 2);
				for (int j = 0; j < where_can_go.count; j++) {
					int j_ = where_can_go.keys[j];
					if (position[j_] == NO_PIECE) {
						position[j_] = BLACK;
						position[i] = NO_PIECE;
						if (_check_is_windmill_formed(position, BLACK, i)) {
							List pieces_to_take = _get_nodes_pieces_to_take(position, WHITE);
							for (int k = 0; k < pieces_to_take.count; k++) {
								int k_ = pieces_to_take.items[k];
								position[k_] = NO_PIECE;
								int eval = _minimax_phase2(position, depth - 1, alpha, beta, 1);
								position[k_] = WHITE;
								min_eval = MIN(min_eval, eval);
								int new_beta = MIN(beta, eval);
								if (new_beta <= alpha) {
									position[i] = BLACK;
									position[j_] = NO_PIECE;
									return min_eval;
								}
							}
						} else {
							int eval = _minimax_phase2(position, depth - 1, alpha, beta, 1);
							min_eval = MIN(min_eval, eval);
							int new_beta = MIN(beta, eval);
							if (new_beta <= alpha) {
								position[i] = BLACK;
								position[j_] = NO_PIECE;
								return min_eval;
							}
						}
						position[i] = BLACK;
						position[j_] = NO_PIECE;
					}
				}
			}
		}
		return min_eval;
	}
}


int _check_is_windmill_formed(int* position, int color, int node) {
	if (position[0] == color && position[1] == color && position[2] == color)
		if (node == 0 || node == 1 || node == 2)
			return 1;
	if (position[0] == color && position[9] == color && position[21] == color)
		if (node == 0 || node == 9 || node == 21)
			return 1;
	if (position[21] == color && position[22] == color && position[23] == color)
		if (node == 21 || node == 22 || node == 23)
			return 1;
	if (position[23] == color && position[14] == color && position[2] == color)
		if (node == 23 || node == 14 || node == 2)
			return 1;
	if (position[3] == color && position[4] == color && position[5] == color)
		if (node == 3 || node == 4 || node == 5)
			return 1;
	if (position[3] == color && position[10] == color && position[18] == color)
		if (node == 3 || node == 10 || node == 18)
			return 1;
	if (position[18] == color && position[19] == color && position[20] == color)
		if (node == 18 || node == 19 || node == 20)
			return 1;
	if (position[20] == color && position[13] == color && position[5] == color)
		if (node == 20 || node == 13 || node == 5)
			return 1;
	if (position[6] == color && position[7] == color && position[8] == color)
		if (node == 6 || node == 7 || node == 8)
			return 1;
	if (position[6] == color && position[11] == color && position[15] == color)
		if (node == 6 || node == 11 || node == 15)
			return 1;
	if (position[15] == color && position[16] == color && position[17] == color)
		if (node == 15 || node == 16 || node == 17)
			return 1;
	if (position[17] == color && position[12] == color && position[8] == color)
		if (node == 17 || node == 12 || node == 8)
			return 1;
	if (position[1] == color && position[4] == color && position[7] == color)
		if (node == 1 || node == 4 || node == 7)
			return 1;
	if (position[9] == color && position[10] == color && position[11] == color)
		if (node == 9 || node == 10 || node == 11)
			return 1;
	if (position[22] == color && position[19] == color && position[16] == color)
		if (node == 22 || node == 19 || node == 16)
			return 1;
	if (position[12] == color && position[13] == color && position[14] == color)
		if (node == 12 || node == 13 || node == 14)
			return 1;

    return 0;
}


Dict _where_can_go(int* position, int node_id, int player) {
	if (player == 1 && !_can_jump(position, 1) || player == 2 && !_can_jump(position, 2)) {
		Dict d;
		Dict_initialize(&d);

		if (node_id == 0) {
			Dict_put_pair(&d, 1, position[1]);
			Dict_put_pair(&d, 9, position[9]);
			return d;
		} else if (node_id == 1) {
			Dict_put_pair(&d, 0, position[0]);
			Dict_put_pair(&d, 2, position[2]);
			Dict_put_pair(&d, 4, position[4]);
			return d;
		} else if (node_id == 2) {
			Dict_put_pair(&d, 1, position[1]);
			Dict_put_pair(&d, 14, position[14]);
			return d;
		} else if (node_id == 3) {
			Dict_put_pair(&d, 4, position[4]);
			Dict_put_pair(&d, 10, position[10]);
			return d;
		} else if (node_id == 4) {
			Dict_put_pair(&d, 1, position[1]);
			Dict_put_pair(&d, 3, position[3]);
			Dict_put_pair(&d, 5, position[5]);
			Dict_put_pair(&d, 7, position[7]);
			return d;
		} else if (node_id == 5) {
			Dict_put_pair(&d, 4, position[4]);
			Dict_put_pair(&d, 13, position[13]);
			return d;
		} else if (node_id == 6) {
			Dict_put_pair(&d, 7, position[7]);
			Dict_put_pair(&d, 11, position[11]);
			return d;
		} else if (node_id == 7) {
			Dict_put_pair(&d, 4, position[4]);
			Dict_put_pair(&d, 6, position[6]);
			Dict_put_pair(&d, 8, position[8]);
			return d;
		} else if (node_id == 8) {
			Dict_put_pair(&d, 7, position[7]);
			Dict_put_pair(&d, 12, position[12]);
			return d;
		} else if (node_id == 9) {
			Dict_put_pair(&d, 0, position[0]);
			Dict_put_pair(&d, 10, position[10]);
			Dict_put_pair(&d, 21, position[21]);
			return d;
		} else if (node_id == 10) {
			Dict_put_pair(&d, 3, position[3]);
			Dict_put_pair(&d, 9, position[9]);
			Dict_put_pair(&d, 11, position[11]);
			Dict_put_pair(&d, 18, position[18]);
			return d;
		} else if (node_id == 11) {
			Dict_put_pair(&d, 6, position[6]);
			Dict_put_pair(&d, 10, position[10]);
			Dict_put_pair(&d, 15, position[15]);
			return d;
		} else if (node_id == 12) {
			Dict_put_pair(&d, 8, position[8]);
			Dict_put_pair(&d, 13, position[13]);
			Dict_put_pair(&d, 17, position[17]);
			return d;
		} else if (node_id == 13) {
			Dict_put_pair(&d, 5, position[5]);
			Dict_put_pair(&d, 12, position[12]);
			Dict_put_pair(&d, 14, position[14]);
			Dict_put_pair(&d, 20, position[20]);
			return d;
		} else if (node_id == 14) {
			Dict_put_pair(&d, 2, position[2]);
			Dict_put_pair(&d, 13, position[13]);
			Dict_put_pair(&d, 23, position[23]);
			return d;
		} else if (node_id == 15) {
			Dict_put_pair(&d, 11, position[11]);
			Dict_put_pair(&d, 16, position[16]);
			return d;
		} else if (node_id == 16) {
			Dict_put_pair(&d, 15, position[15]);
			Dict_put_pair(&d, 17, position[17]);
			Dict_put_pair(&d, 19, position[19]);
			return d;
		} else if (node_id == 17) {
			Dict_put_pair(&d, 12, position[12]);
			Dict_put_pair(&d, 16, position[16]);
			return d;
		} else if (node_id == 18) {
			Dict_put_pair(&d, 10, position[10]);
			Dict_put_pair(&d, 19, position[19]);
			return d;
		} else if (node_id == 19) {
			Dict_put_pair(&d, 16, position[16]);
			Dict_put_pair(&d, 18, position[20]);
			Dict_put_pair(&d, 20, position[20]);
			Dict_put_pair(&d, 22, position[22]);
			return d;
		} else if (node_id == 20) {
			Dict_put_pair(&d, 13, position[13]);
			Dict_put_pair(&d, 19, position[19]);
			return d;
		} else if (node_id == 21) {
			Dict_put_pair(&d, 9, position[9]);
			Dict_put_pair(&d, 22, position[22]);
			return d;
		} else if (node_id == 22) {
			Dict_put_pair(&d, 19, position[19]);
			Dict_put_pair(&d, 21, position[21]);
			Dict_put_pair(&d, 23, position[23]);
			return d;
		} else {
			Dict_put_pair(&d, 14, position[14]);
			Dict_put_pair(&d, 22, position[22]);
			return d;
		}
	} else {
		Dict nodes;
		Dict_initialize(&nodes);

		for (int i = 0; i < 24; i++)
			Dict_put_pair(&nodes, i, nodes[i]);

		Dict_del_pair(&nodes, node_id);
		return nodes;
	}
}


List _get_nodes_pieces_to_take(int* position, int color) {
	List windmill_nodes;
	List_initialize(&windmill_nodes);

	if (position[0] == color && position[1] == color && position[2] == color) {
		List_append(&windmill_nodes, 0);
		List_append(&windmill_nodes, 1);
		List_append(&windmill_nodes, 2);
	}
	if (position[0] == color && position[9] == color && position[21] == color) {
		List_append(&windmill_nodes, 0);
		List_append(&windmill_nodes, 9);
		List_append(&windmill_nodes, 21);
	}
	if (position[21] == color && position[22] == color && position[23] == color) {
		List_append(&windmill_nodes, 21);
		List_append(&windmill_nodes, 22);
		List_append(&windmill_nodes, 23);
	}
	if (position[23] == color && position[14] == color && position[2] == color) {
		List_append(&windmill_nodes, 23);
		List_append(&windmill_nodes, 14);
		List_append(&windmill_nodes, 2);
	}
	if (position[3] == color && position[4] == color && position[5] == color) {
		List_append(&windmill_nodes, 3);
		List_append(&windmill_nodes, 4);
		List_append(&windmill_nodes, 5);
	}
	if (position[3] == color && position[10] == color && position[18] == color) {
		List_append(&windmill_nodes, 3);
		List_append(&windmill_nodes, 10);
		List_append(&windmill_nodes, 18);
	}
	if (position[18] == color && position[19] == color && position[20] == color) {
		List_append(&windmill_nodes, 18);
		List_append(&windmill_nodes, 19);
		List_append(&windmill_nodes, 20);
	}
	if (position[20] == color && position[13] == color && position[5] == color) {
		List_append(&windmill_nodes, 20);
		List_append(&windmill_nodes, 13);
		List_append(&windmill_nodes, 5);
	}
	if (position[6] == color && position[7] == color && position[8] == color) {
		List_append(&windmill_nodes, 6);
		List_append(&windmill_nodes, 7);
		List_append(&windmill_nodes, 8);
	}
	if (position[6] == color && position[11] == color && position[15] == color) {
		List_append(&windmill_nodes, 6);
		List_append(&windmill_nodes, 11);
		List_append(&windmill_nodes, 15);
	}
	if (position[15] == color && position[16] == color && position[17] == color) {
		List_append(&windmill_nodes, 15);
		List_append(&windmill_nodes, 16);
		List_append(&windmill_nodes, 17);
	}
	if (position[17] == color && position[12] == color && position[8] == color) {
		List_append(&windmill_nodes, 17);
		List_append(&windmill_nodes, 12);
		List_append(&windmill_nodes, 8);
	}
	if (position[1] == color && position[4] == color && position[7] == color) {
		List_append(&windmill_nodes, 1);
		List_append(&windmill_nodes, 4);
		List_append(&windmill_nodes, 7);
	}
	if (position[9] == color && position[10] == color && position[11] == color) {
		List_append(&windmill_nodes, 9);
		List_append(&windmill_nodes, 10);
		List_append(&windmill_nodes, 11);
	}
	if (position[22] == color && position[19] == color && position[16] == color) {
		List_append(&windmill_nodes, 22);
		List_append(&windmill_nodes, 19);
		List_append(&windmill_nodes, 16);
	}
	if (position[12] == color && position[13] == color && position[14] == color) {
		List_append(&windmill_nodes, 12);
		List_append(&windmill_nodes, 13);
		List_append(&windmill_nodes, 14);
	}

	List nodes;
	List_initialize(&nodes);

	for (int i = 0; i < 24; i++) {
		if (position[i] == color && !List_item_in_list(&nodes, i))
			List_append(&nodes, i);
	}

	if (nodes.count == 0) {
		List all;
		List_initialize(&all);

		for (int i = 0; i < 24; i++) {
			if (position[i] == color)
				List_append(&all, i);
		}

		return all;
	}

	return nodes;
}


Tuple _get_number_of_windmills(int* position) {
    int white_mills = 0;
    int black_mills = 0;

    if (position[0] == position[1] && position[1] == position[2]) {
        if (position[0] == WHITE)
            white_mills++;
        else if (position[0] == BLACK)
            black_mills++;
    }
    if (position[0] == position[9] && position[9] == position[21]) {
        if (position[0] == WHITE)
            white_mills++;
        else if (position[0] == BLACK)
            black_mills++;
    }
    if (position[21] == position[22] && position[22] == position[23]) {
        if (position[21] == WHITE)
            white_mills++;
        else if (position[21] == BLACK)
            black_mills++;
    }
    if (position[23] == position[14] && position[14] == position[2]) {
        if (position[23] == WHITE)
            white_mills++;
        else if (position[23] == BLACK)
            black_mills++;
    }
    if (position[3] == position[4] && position[4] == position[5]) {
        if (position[3] == WHITE)
            white_mills++;
        else if (position[3] == BLACK)
            black_mills++;
    }
    if (position[3] == position[10] && position[10] == position[18]) {
        if (position[3] == WHITE)
            white_mills++;
        else if (position[3] == BLACK)
            black_mills++;
    }
    if (position[18] == position[19] && position[19] == position[20]) {
        if(position[18] == WHITE)
            white_mills++;
        else if (position[18] == BLACK)
            black_mills++;
    }
    if (position[20] == position[13] && position[13] == position[5]) {
        if (position[20] == WHITE)
            white_mills++;
        else if (position[20] == BLACK)
            black_mills++;
    }
    if (position[6] == position[7] && position[7] == position[8]) {
        if (position[6] == WHITE)
            white_mills++;
        else if (position[6] == BLACK)
            black_mills++;
    }
    if (position[6] == position[11] && position[11] == position[15]) {
        if (position[6] == WHITE)
            white_mills++;
        else if (position[6] == BLACK)
            black_mills++;
    }
    if (position[15] == position[16] && position[16] == position[17]) {
        if (position[15] == WHITE)
            white_mills++;
        else if (position[15] == BLACK)
            black_mills++;
    }
    if (position[17] == position[12] && position[12] == position[8]) {
        if (position[17] == WHITE)
            white_mills++;
        else if (position[17] == BLACK)
            black_mills++;
    }
    if (position[1] == position[4] && position[4] == position[7]) {
        if (position[1] == WHITE)
            white_mills++;
        else if (position[1] == BLACK)
            black_mills++;
    }
    if (position[9] == position[10] && position[10] == position[11]) {
        if (position[9] == WHITE)
            white_mills++;
        else if (position[9] == BLACK)
            black_mills++;
    }
    if (position[22] == position[19] && position[19] == position[16]) {
        if (position[22] == WHITE)
            white_mills++;
        else if (position[22] == BLACK)
            black_mills++;
    }
    if (position[12] == position[13] && position[13] == position[14]) {
        if (position[12] == WHITE)
            white_mills++;
        else if (position[12] == BLACK)
            black_mills++;
    }

    Tuple mills = {white_mills, black_mills};

    return mills;
}


int _is_game_over(int* position) {
	int black_pieces = 0;
	int white_pieces = 0;
	for (int i = 0; i < 24; i++) {
		if (node == WHITE)
			white_pieces++;
		else if (node == BLACK)
			black_pieces++;
	}

	if (white_pieces < 3 || black_pieces < 3)
		return 1;

	for (int i = 0; i < 24; i++) {
		if (position[i] == WHITE) {
			Dict white_can_go = _where_can_go(position, i, 1);

			for (int i = 0; i < white_can_go.count; i++) {
				if (white_can_go.values[i] == NO_PIECE)
					return 0;
			}
		} else if (position[i] == BLACK) {
			Dict black_can_go = _where_can_go(position, i, 2);

			for (int i = 0; i < black_can_go.count; i++) {
				if (black_can_go.values[i] == NO_PIECE)
					return 0;
			}
		}
	}

	return 1;
}


int _can_jump(int* position, int player) {
	if (player == 1) {
		int white_pieces = 0;

		for (int i = 0; i < 24; i++) {
			if (position[i] == WHITE)
				white_pieces++;
		}

		if (white_pieces == 3)
			return 1;
	} else {
		int black_pieces = 0;

		for (int i = 0; i < 24; i++) {
			if (position[i] == BLACK)
				black_pieces++;
		}

		if (black_pieces == 3)
			return 1;
	}

	return 0;
}


static PyObject* py_ai_place_piece_at(PyObject* self, PyObject* position) {
	PyObject* position_list;
	int position[24];

	for (int i = 0; i < 24; i++) {
		PyObject* item = PyList_GetItem(position_list, i);  // Borowed reference
		long item_as_number = PyLong_AsLong(item);

		if (item_as_number < 0 && PyErr_Occurred()) {  // Might not be needed
			Py_DECREF(position_list);
			return NULL;
		}

		position[i] = (int) item_as_number;
	}

	int node = ai_place_piece_at(position);

	return PyLong_FromLong((long) node);
}


static PyObject* py_ai_remove_piece(PyObject* self) {
	int node = ai_remove_piece();

	return PyLong_FromLong((long) node);
}


static PyObject* py_ai_move_piece(PyObject* self, PyObject* position) {
	PyObject* position_list;
	PyObject* nodes_tuple;
	int position[24];

	for (int i = 0; i < 24; i++) {
		PyObject* item = PyList_GetItem(position_list, i);  // Borowed reference
		long item_as_number = PyLong_AsLong(item);

		if (item_as_number < 0 && PyErr_Occurred()) {  // Might not be needed
			Py_DECREF(position_list);
			return NULL;
		}

		position[i] = (int) item_as_number;
	}

	Tuple nodes = ai_move_piece(position);

	nodes_tuple = PyTuple_New(2);
	if (nodes_tuple == NULL) {  // Might not be needed
		Py_DECREF(position_list);
		PyErr_SetString(PyExc_RunTimeError, "Could not create tuple");
		return NULL;
	}

	PyTuple_SetItem(nodes_tuple, 0, PyLong_FromLong((long) nodes.a));
	PyTuple_SetItem(nodes_tuple, 1, PyLong_FromLong((long) nodes.b));

	return nodes_tuple;
}


static PyMethodDef minimax_methods[] = {
	{"ai_place_piece_at", (PyCFunction) py_ai_place_piece_at, METH_O, ""},
	{"ai_remove_piece", (PyCFunction) py_ai_remove_piece, METH_NOARGS, ""},
	{"ai_move_piece", (PyCFunction) py_ai_move_piece, METH_O, ""},
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef minimax_module = {
    PyModuleDef_HEAD_INIT,
	.m_name = "minimax",
	.m_doc = "",
	.m_size = -1,
	.m_methods = minimax_methods
};

PyMODINIT_FUNC PyInit_minimax() {
	PyObject* m;

	m = PyModule_Create(&minimax_module);
	if (m == NULL)
		return NULL;

	return m;
}
