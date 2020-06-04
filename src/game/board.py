import tkinter as tk
from typing import Optional
from math import sqrt

from src.game.piece import Piece
from src.game.node import Node
from src.constants import *
from src.log import get_logger

logger = get_logger(__name__)
logger.setLevel(10)

canvas_width = 700


class Vec2:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def set_mag(self, mag: float):
        assert self.x != 0 or self.y != 0
        length = sqrt(self.x ** 2 + self.y ** 2)
        self.x /= length
        self.y /= length
        self.x *= mag
        self.y *= mag

    def as_tuple(self) -> tuple:
        return self.x, self.y


class Board:
    """Game board object."""

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.DIV = 100
        self.PAD = 50

        self._draw_board()

        self.nodes = (
            Node(0 + self.PAD, 0 + self.PAD, canvas, 0),
            Node(self.DIV * 3 + self.PAD, 0 + self.PAD, canvas, 1),
            Node(self.DIV * 6 + self.PAD, 0 + self.PAD, canvas, 2),  # line
            Node(self.DIV + self.PAD, self.DIV + self.PAD, canvas, 3),
            Node(self.DIV * 3 + self.PAD, self.DIV + self.PAD, canvas, 4),
            Node(self.DIV * 5 + self.PAD, self.DIV + self.PAD, canvas, 5),  # line
            Node(self.DIV * 2 + self.PAD, self.DIV * 2 + self.PAD, canvas, 6),
            Node(self.DIV * 3 + self.PAD, self.DIV * 2 + self.PAD, canvas, 7),
            Node(self.DIV * 4 + self.PAD, self.DIV * 2 + self.PAD, canvas, 8),  # line
            Node(0 + self.PAD, self.DIV * 3 + self.PAD, canvas, 9),
            Node(self.DIV + self.PAD, self.DIV * 3 + self.PAD, canvas, 10),
            Node(self.DIV * 2 + self.PAD, self.DIV * 3 + self.PAD, canvas, 11),  # line
            Node(self.DIV * 4 + self.PAD, self.DIV * 3 + self.PAD, canvas, 12),
            Node(self.DIV * 5 + self.PAD, self.DIV * 3 + self.PAD, canvas, 13),
            Node(self.DIV * 6 + self.PAD, self.DIV * 3 + self.PAD, canvas, 14),  # line
            Node(self.DIV * 2 + self.PAD, self.DIV * 4 + self.PAD, canvas, 15),
            Node(self.DIV * 3 + self.PAD, self.DIV * 4 + self.PAD, canvas, 16),
            Node(self.DIV * 4 + self.PAD, self.DIV * 4 + self.PAD, canvas, 17),  # line
            Node(self.DIV + self.PAD, self.DIV * 5 + self.PAD, canvas, 18),
            Node(self.DIV * 3 + self.PAD, self.DIV * 5 + self.PAD, canvas, 19),
            Node(self.DIV * 5 + self.PAD, self.DIV * 5 + self.PAD, canvas, 20),  # line
            Node(0 + self.PAD, self.DIV * 6 + self.PAD, canvas, 21),
            Node(self.DIV * 3 + self.PAD, self.DIV * 6 + self.PAD, canvas, 22),
            Node(self.DIV * 6 + self.PAD, self.DIV * 6 + self.PAD, canvas, 23)  # line
        )

        self.phase = PHASE1
        self.turn = PLAYER1

        self.white_pieces = 9
        self.black_pieces = 9

        self.picked_up_piece: Optional[Piece] = None  # The piece that is currenly held
        self.node_taken_piece: Optional[Node] = None  # The node whose piece is currently picked up

        self.windmills = (
            (self.nodes[0], self.nodes[1], self.nodes[2]),
            (self.nodes[0], self.nodes[9], self.nodes[21]),
            (self.nodes[21], self.nodes[22], self.nodes[23]),
            (self.nodes[23], self.nodes[14], self.nodes[2]),
            (self.nodes[3], self.nodes[4], self.nodes[5]),
            (self.nodes[3], self.nodes[10], self.nodes[18]),
            (self.nodes[18], self.nodes[19], self.nodes[20]),
            (self.nodes[20], self.nodes[13], self.nodes[5]),
            (self.nodes[6], self.nodes[7], self.nodes[8]),
            (self.nodes[6], self.nodes[11], self.nodes[15]),
            (self.nodes[15], self.nodes[16], self.nodes[17]),
            (self.nodes[17], self.nodes[12], self.nodes[8]),
            (self.nodes[1], self.nodes[4], self.nodes[7]),
            (self.nodes[9], self.nodes[10], self.nodes[11]),
            (self.nodes[22], self.nodes[19], self.nodes[16]),
            (self.nodes[12], self.nodes[13], self.nodes[14])
        )

        self.must_remove_piece = False
        self.can_jump = {PLAYER1: False, PLAYER2: False}
        self.node_pressed = False  # if a node is clicked
        self.turns_without_windmills = 0

        self.MAX_TURNS_WO_MILLS = 100

        self.game_over = False
        self.winner = TIE  # Nobody is the winner

        self.history = {"ones": [], "twos": []}

    def update(self, mouse_x: int, mouse_y: int):
        for node in self.nodes:
            try:
                node.update(mouse_x, mouse_y, self.must_remove_piece, self._get_turn_color() != node.piece.color)
            except AttributeError:  # Dirty solution for when the node doesn't have a piece
                node.update(mouse_x, mouse_y, self.must_remove_piece, False)

            if node.piece is not None and node.piece.reached_position:
                node.piece.update(mouse_x, mouse_y)

    # def on_window_resize(self, width: int, height: int):
    #     global window_width, window_height
    #     window_width = width
    #     window_height = height
    #
    #     if height <= width:
    #         self.width = height - 160
    #     else:
    #         self.width = width - 160
    #
    #     self.x = round((width - self.width) / 2)
    #     self.y = round((height - self.width) / 2)
    #     self.DIV = round(self.width / 6)
    #
    #     self.nodes[0].set_position(self.x, self.y)
    #     self.nodes[1].set_position(self.x + self.DIV * 3, self.y)
    #     self.nodes[2].set_position(self.x + self.DIV * 6, self.y)
    #     self.nodes[3].set_position(self.x + self.DIV, self.y + self.DIV)
    #     self.nodes[4].set_position(self.x + self.DIV * 3, self.y + self.DIV)
    #     self.nodes[5].set_position(self.x + self.DIV * 5, self.y + self.DIV)
    #     self.nodes[6].set_position(self.x + self.DIV * 2, self.y + self.DIV * 2)
    #     self.nodes[7].set_position(self.x + self.DIV * 3, self.y + self.DIV * 2)
    #     self.nodes[8].set_position(self.x + self.DIV * 4, self.y + self.DIV * 2)
    #     self.nodes[9].set_position(self.x, self.y + self.DIV * 3)
    #     self.nodes[10].set_position(self.x + self.DIV, self.y + self.DIV * 3)
    #     self.nodes[11].set_position(self.x + self.DIV * 2, self.y + self.DIV * 3)
    #     self.nodes[12].set_position(self.x + self.DIV * 4, self.y + self.DIV * 3)
    #     self.nodes[13].set_position(self.x + self.DIV * 5, self.y + self.DIV * 3)
    #     self.nodes[14].set_position(self.x + self.DIV * 6, self.y + self.DIV * 3)
    #     self.nodes[15].set_position(self.x + self.DIV * 2, self.y + self.DIV * 4)
    #     self.nodes[16].set_position(self.x + self.DIV * 3, self.y + self.DIV * 4)
    #     self.nodes[17].set_position(self.x + self.DIV * 4, self.y + self.DIV * 4)
    #     self.nodes[18].set_position(self.x + self.DIV, self.y + self.DIV * 5)
    #     self.nodes[19].set_position(self.x + self.DIV * 3, self.y + self.DIV * 5)
    #     self.nodes[20].set_position(self.x + self.DIV * 5, self.y + self.DIV * 5)
    #     self.nodes[21].set_position(self.x, self.y + self.DIV * 6)
    #     self.nodes[22].set_position(self.x + self.DIV * 3, self.y + self.DIV * 6)
    #     self.nodes[23].set_position(self.x + self.DIV * 6, self.y + self.DIV * 6)
    #
    #     # Assuming that 600 is the default window height
    #     Node.dot_radius = round((window_height * Node.DEFAULT_DOT_RADIUS) / 600)
    #     Node.radius = round((window_height * Node.DEFAULT_RADIUS) / 600)
    #     Piece.radius = round((window_height * Piece.DEFAULT_RADIUS) / 600)
    #     self.line_thickness = round((window_height * 8) / 600)
    #     self.board_offset = round((window_height * 35) / 600)

    def put_new_piece(self) -> bool:
        """Puts a new piece on to the board.

        Returns:
            bool: True if the turn was changed, False otherwise. For pymill_network.

        """
        changed_turn = False
        for node in self.nodes:
            if node.highlight and not node.piece:
                if self.turn == PLAYER1:
                    new_piece = Piece(node.x, node.y, WHITE, self.canvas)
                    node.add_piece(new_piece)
                    self.white_pieces -= 1
                    if not self._check_is_windmill_formed(WHITE, node):
                        self._switch_turn()
                        changed_turn = True
                    else:
                        self.must_remove_piece = True
                        logger.debug("Remove a piece!")
                else:
                    new_piece = Piece(node.x, node.y, BLACK, self.canvas)
                    node.add_piece(new_piece)
                    self.black_pieces -= 1
                    if not self._check_is_windmill_formed(BLACK, node):
                        self._switch_turn()
                        changed_turn = True
                    else:
                        self.must_remove_piece = True
                        logger.debug("Remove a piece!")
                break
        if (self.white_pieces + self.black_pieces) == 0:
            self.phase = PHASE2
            logger.info("PHASE 2")
        return changed_turn

    def pick_up_piece(self):
        for node in self.nodes:
            if node.highlight and node.piece and self.picked_up_piece is None:
                if node.piece.pick_up(self.turn):
                    self.canvas.tag_raise(node.piece.oval)
                    self._change_nodes_color(node, "#00ff00", "#ff0000")
                    self.node_taken_piece = node
                    self.picked_up_piece = node.piece
                break

    def remove_opponent_piece(self) -> bool:
        """Removes a piece from opponent.

        Returns:
            bool: True if the player can actually remove the piece, False otherwise.

        """
        can_remove = False

        for node in self.nodes:
            if self.turn == PLAYER1:
                if node.highlight and node.piece and node.piece.color == BLACK:
                    if not self._check_is_windmill_formed(BLACK, node) or \
                            self._number_pieces_in_windmills(BLACK) == self._count_pieces_left_of_player(BLACK):
                        node.take_piece(True)
                        self.must_remove_piece = False
                        if self._check_player_pieces(BLACK):
                            self._game_over(tie=False, winner=PLAYER1 if self.turn == PLAYER1 else PLAYER2)
                        self._switch_turn()
                        self._clear_history()  # Clear the history, because it will never repeat itself
                        can_remove = True
                    else:
                        logger.info("You cannot take piece from windmill!")
            else:
                if node.highlight and node.piece and node.piece.color == WHITE:
                    if not self._check_is_windmill_formed(WHITE, node) or \
                            self._number_pieces_in_windmills(WHITE) == self._count_pieces_left_of_player(WHITE):
                        node.take_piece(True)
                        self.must_remove_piece = False
                        if self._check_player_pieces(WHITE):
                            self._game_over(tie=False, winner=PLAYER1 if self.turn == PLAYER1 else PLAYER2)
                        self._switch_turn()
                        self._clear_history()  # Clear the history, because it will never repeat itself
                        can_remove = True
                    else:
                        logger.info("You cannot take piece from windmill!")
        self.node_pressed = False
        return can_remove

    def put_down_piece(self) -> bool:
        """Puts down a picked up piece.

        Returns:
            bool: True if the turn was changed, False otherwise. For pymill_network.

        """
        changed_turn = False
        if self.picked_up_piece is not None:
            for node in self._where_can_go(self.node_taken_piece):
                if node.highlight and not node.piece:
                    node.add_piece(self.picked_up_piece)
                    logger.debug("Piece: {}".format(node.piece))
                    self._change_nodes_color(self.node_taken_piece, "#000000", "#000000")
                    self.node_taken_piece.piece.release(node)
                    self.node_taken_piece.take_piece()
                    self.node_taken_piece = None
                    self.picked_up_piece = None
                    if not self._check_is_windmill_formed(WHITE if self.turn == PLAYER1 else BLACK, node):
                        self._switch_turn()
                        self.turns_without_windmills += 1
                        changed_turn = True
                    else:
                        self.must_remove_piece = True
                        logger.info("Remove a piece!")

                    # Do all of this only if there was a piece put down on a node
                    if self._check_player_pieces(WHITE if self.turn == PLAYER1 else BLACK):  # inverse WHITE and BLACK,
                        if not self.must_remove_piece:                                       # because turn was already
                            self._game_over(tie=False, winner=PLAYER2 if self.turn == PLAYER1 else PLAYER1)  # switched

                    self._check_board_state()
                    self._check_turns_without_windmills()  # They call self._game_over by themself

        # Release piece if player released the left button.
        if self.picked_up_piece is not None:
            self._change_nodes_color(self.node_taken_piece, "#000000", "#000000")
            self.picked_up_piece.release(self.node_taken_piece)
            self.picked_up_piece = None

        return changed_turn

    def put_new_piece_alone(self, node_id: int, piece_color: tuple):
        """Puts a new piece on that node. For computer and networking versions of the game.

        Args:
            node_id: The node on which to put the new piece.
            piece_color: What type of piece to put.

        """
        assert 0 <= node_id <= 23
        assert self.phase == PHASE1

        logger.debug(f"Putting a piece on node {node_id}")
        node = self.nodes[node_id]

        assert node.piece is None
        piece = Piece(canvas_width // 2 - 100, -100, piece_color, self.canvas)

        piece.reached_position = False
        piece.target = (node.x, node.y)
        vel = Vec2(node.x - piece.x, node.y - piece.y)
        vel.set_mag(12)
        piece.velocity = vel.as_tuple()

        node.add_piece(piece)

        if piece_color == WHITE:
            self.white_pieces -= 1
        else:
            self.black_pieces -= 1
        if not self._check_is_windmill_formed(piece_color, node):
            self._switch_turn()
        else:
            self.must_remove_piece = True
            logger.debug("Remove a piece!")

        if self._check_player_pieces(WHITE if self.turn == PLAYER1 else BLACK):  # inverse WHITE and BLACK,
            if not self.must_remove_piece:                                       # because turn was already
                self._game_over(tie=False, winner=PLAYER2 if self.turn == PLAYER1 else PLAYER1)  # switched

        if (self.white_pieces + self.black_pieces) == 0:
            self.phase = PHASE2
            logger.info("PHASE 2")

    def change_piece_location(self, source_node_id: int, destination_node_id: int):
        """Takes a piece from a node and puts it somewhere else.

        Args:
            source_node_id: The node from which to take the piece.
            destination_node_id: The node on to which to put the piece.

        """
        assert 0 <= source_node_id <= 23 and 0 <= destination_node_id <= 23, f"{source_node_id}, {destination_node_id}"  # FIXME this failed unexpectedly
        assert self.phase == PHASE2
        assert source_node_id != destination_node_id

        logger.debug(f"Moving piece from node {source_node_id} to node {destination_node_id}")

        node = self.nodes[source_node_id]
        assert node.piece is not None
        piece = node.piece

        node.take_piece()  # TODO maybe with parameter True

        dest_node = self.nodes[destination_node_id]

        piece.reached_position = False
        piece.target = (dest_node.x, dest_node.y)
        vel = Vec2(dest_node.x - piece.x, dest_node.y - piece.y)
        vel.set_mag(12)
        piece.velocity = vel.as_tuple()

        assert dest_node.piece is None
        dest_node.add_piece(piece)

        if not self._check_is_windmill_formed(piece.color, dest_node):
            self._switch_turn()
            self.turns_without_windmills += 1
        else:
            self.must_remove_piece = True
            logger.debug("Remove a piece!")

        if self._check_player_pieces(WHITE if self.turn == PLAYER1 else BLACK):  # inverse WHITE and BLACK because turn
            if not self.must_remove_piece:                                       # was already switched
                self._game_over(tie=False, winner=PLAYER2 if self.turn == PLAYER1 else PLAYER1)

        self._check_board_state()
        self._check_turns_without_windmills()  # They call self._game_over by themself

    def remove_opponent_piece_alone(self, node_id: int):
        """Removes a piece from opponent. For computer and networking versions of the game.

        Warning: It doesn't check if the piece can actually be taken (i.e. it is inside a windmill).

        Args:
            node_id (int): The node from which to take the piece.

        """
        node = self.nodes[node_id]
        assert node.piece is not None

        piece = node.piece

        piece.reached_position = False
        piece.target = (canvas_width // 2 - 100, -100)
        vel = Vec2(canvas_width // 2 - 100 - piece.x, -100 - piece.y)
        vel.set_mag(12)
        piece.velocity = vel.as_tuple()

        node.take_piece_after()
        logger.info(f"Piece node {node.id} removed")

        self.must_remove_piece = False
        if self._check_player_pieces(BLACK if self.turn == PLAYER1 else WHITE):
            self._game_over(tie=False, winner=PLAYER1 if self.turn == PLAYER1 else PLAYER2)
        self._switch_turn()
        self._clear_history()  # Clear the history, because it will never repeat itself

    def get_current_state(self) -> list:
        """
        0 - no piece
        1 - WHITE piece
        2 - BLACK piece

        The state is just a list of numbers representing the pieces' positions.

        Returns:
            list: A representation of the current game state.

        """
        current_state = []
        for node in self.nodes:
            if node.piece is None:
                current_state.append(0)
            else:
                if node.piece.color == WHITE:
                    current_state.append(1)
                else:
                    current_state.append(2)

        return current_state

    def check_is_windmill_formed(self, color: tuple, node: Node) -> bool:
        """Same as the private version of this method, but optimized.

        Args:
            color (tuple): The color of the pieces to check.
            node (Node): The node to check if is any of windmill's nodes.

        Returns:
            bool: True if there is a windmill and if node is in there, False otherwise.

        """
        for windmill in self.windmills:
            if self._check_nodes_for_windmill(windmill, color) and any(map(lambda n: n is node, windmill)):
                return True
        return False

    def mouse_over_any_node(self) -> bool:
        for node in self.nodes:
            if node.highlight:
                return True
        return False

    def _draw_board(self):
        # self.canvas.create_rectangle(self.DIV, self.DIV, self.DIV * 7, self.DIV * 7, width=9)
        # self.canvas.create_rectangle(self.DIV * 2, self.DIV * 2, self.DIV * 6, self.DIV * 6, width=9)
        # self.canvas.create_rectangle(self.DIV * 3, self.DIV * 3, self.DIV * 5, self.DIV * 5, width=9)
        #
        # self.canvas.create_line(self.DIV, self.DIV * 4, self.DIV * 3, self.DIV * 4, width=9)
        # self.canvas.create_line(self.DIV * 5, self.DIV * 4, self.DIV * 7, self.DIV * 4, width=9)
        # self.canvas.create_line(self.DIV * 4, self.DIV, self.DIV * 4, self.DIV * 3, width=9)
        # self.canvas.create_line(self.DIV * 4, self.DIV * 5, self.DIV * 4, self.DIV * 7, width=9)

        self.canvas.create_rectangle(0 + self.PAD, 0 + self.PAD, self.DIV * 7 - self.PAD, self.DIV * 7 - self.PAD, width=9)
        self.canvas.create_rectangle(self.DIV + self.PAD, self.DIV + self.PAD, self.DIV * 6 - self.PAD,
                                     self.DIV * 6 - self.PAD, width=9)
        self.canvas.create_rectangle(self.DIV * 2 + self.PAD, self.DIV * 2 + self.PAD, self.DIV * 5 - self.PAD,
                                     self.DIV * 5 - self.PAD, width=9)

        self.canvas.create_line(0 + self.PAD, self.DIV * 3 + self.PAD, self.DIV * 2 + self.PAD, self.DIV * 3 + self.PAD,
                                width=9)
        self.canvas.create_line(self.DIV * 4 + self.PAD, self.DIV * 3 + self.PAD, self.DIV * 6 + self.PAD,
                                self.DIV * 3 + self.PAD, width=9)
        self.canvas.create_line(self.DIV * 3 + self.PAD, self.PAD, self.DIV * 3 + self.PAD, self.DIV * 2 + self.PAD, width=9)
        self.canvas.create_line(self.DIV * 3 + self.PAD, self.DIV * 4 + self.PAD, self.DIV * 3 + self.PAD,
                                self.DIV * 6 + self.PAD, width=9)

    def _switch_turn(self):
        if self.turn == PLAYER1:
            self.turn = PLAYER2
        else:
            self.turn = PLAYER1

    def _check_board_state(self):  # TODO doesn't work well; it is game over too early; problem is when this method is called
        """Get the current state of the board and check if it's game over. FIXME it was tie when it shouldn't be

        """
        current_state = tuple(self.get_current_state())

        for state in self.history["twos"]:
            if state == current_state:
                self._game_over(tie=True)
                return

        for state in self.history["ones"]:
            if state == current_state:
                self.history["ones"].remove(state)
                self.history["twos"].append(state)
                return

        self.history["ones"].append(current_state)

    def _check_turns_without_windmills(self):
        """Checks if the number of turns without windmills was exceeded.

        """
        if self.turns_without_windmills > self.MAX_TURNS_WO_MILLS:
            self._game_over(tie=True)
            logger.info("The amount of turns without windmills was exceeded")

    def _clear_history(self):
        self.history["ones"].clear()
        self.history["twos"].clear()

    def _game_over(self, tie: bool, winner: int = TIE):
        self.game_over = True
        if not tie:
            self.winner = winner
            logger.info(f"Player {self.winner} won!")
        else:
            logger.info("Tie!")

    @staticmethod
    def _check_nodes_for_windmill(w_mill: tuple, color: tuple) -> bool:
        """Checks if all nodes within a group of nodes have pieces of the same color.

        Args:
            w_mill (tuple): The group of nodes to check (a possible windmill).
            color (tuple): The color that the pieces all need to be.

        Returns:
            bool: True if the nodes within the windmill actually form a windmill, False otherwise.

        """
        return all(map(lambda n: n.piece is not None and n.piece.color == color, w_mill))

    def _check_is_windmill_formed(self, color: tuple, node: Node) -> bool:
        """Checks if there is a windmill formed and if node is any of the windmill's nodes.

        Args:
            color (tuple): The color of the pieces to check.
            node (Node): The node to check if is any of windmill's nodes.

        Returns:
            bool: True if there is a windmill and if node is in there, False otherwise.

        """
        for i, windmill in enumerate(self.windmills):
            if self._check_nodes_for_windmill(windmill, color) and any(map(lambda n: n is node, windmill)):
                logger.debug("{} windmill nr. {}".format("Black" if color == BLACK else "White", i))
                self.turns_without_windmills = 0
                return True
        return False

    def _count_pieces_left_of_player(self, color: tuple) -> int:
        """Counts the number of pieces a player has.

        Args:
            color (tuple): The color of the pieces it counts.

        Returns:
            int: The number of pieces a player has.

        """
        pieces = 0
        for node in self.nodes:
            if node.piece and node.piece.color == color:
                pieces += 1
        logger.debug(f"{'Player 1' if color == WHITE else 'Player 2'} pieces remaining: {pieces}")
        return pieces

    def _check_player_pieces(self, color: tuple) -> bool:
        """Checks the number of pieces of a player, checks if it's blocked and returns if the game is over.

        If the player has 3 pieces remaining, his/her pieces can go anywhere and if 2 pieces remaining, he/she loses.

        Args:
            color (tuple): The color of the pieces to check.

        Returns:
            bool: True if the game is over, False otherwise.

        """
        player = PLAYER1 if color == WHITE else PLAYER2
        pieces_left = self._count_pieces_left_of_player(color)

        if self.phase == PHASE2:
            if pieces_left == 3:
                self.can_jump[player] = True
            else:
                self.can_jump[player] = False

            if pieces_left == 2:
                return True

        pieces_to_check = (self.black_pieces < 2) if player is PLAYER2 else (self.white_pieces < 2)
        if pieces_to_check:
            if self._is_opponent_blocked(player):
                return True

        return False

    def _where_can_go(self, node: Node) -> tuple:
        """Decides where a piece can go based on the dictionary self.can_jump.

        It returns the neighbor nodes, if the player cannot jump; it doesn't check for pieces.

        Args:
            node (Node): The node from where the piece wants to go.

        Returns:
            tuple: The nodes where the piece can go.

        """
        assert node is not None, "Node shouldn't be None..."

        if self.turn == PLAYER1 and not self.can_jump[PLAYER1] or self.turn == PLAYER2 and not self.can_jump[PLAYER2]:
            return node.search_neighbors(self.nodes)
        else:
            new_nodes = list(self.nodes)
            new_nodes.remove(node)
            return tuple(new_nodes)

    def _number_pieces_in_windmills(self, color: tuple) -> int:
        """Counts the number of pieces that are inside of every windmill.

        Args:
            color (tuple): The color of the pieces to count.

        Returns:
            int: The number of pieces that are inside windmills.

        """
        pieces_inside_windmills = set()
        for windmill in self.windmills:
            if self._check_nodes_for_windmill(windmill, color):
                for node in windmill:
                    pieces_inside_windmills.add(node)
        return len(pieces_inside_windmills)

    def _change_nodes_color(self, node: Node, color1: str, color2: str):
        """Changes color of other nodes based on where the piece can go.

        Args:
            node (Node): The node where the piece currently sits.
            color1 (tuple): The color to change the nodes where the piece can go.
            color2 (tuple): The color to change the nodes where the piece cannot go.

        """
        for n in self._where_can_go(node):
            n.change_color(color1)

        nodes_copy = list(self.nodes)
        for i in self.nodes:
            for j in self._where_can_go(node):
                if i == j:
                    nodes_copy.remove(i)
        nodes_copy.remove(node)

        for n in nodes_copy:
            n.change_color(color2)

    def _is_opponent_blocked(self, player: int) -> bool:
        """Checks if a player has any legal moves to do.

        Args:
            player (int): The player whose pieces to check.

        Returns:
            bool: True if the player is blocked, False otherwise.

        """
        if player == PLAYER1:
            color = WHITE
        else:
            color = BLACK

        logger.debug(f"Player {player} is checked if it's blocked")
        player_nodes = [node for node in self.nodes if node.piece and node.piece.color == color]
        num_of_player_nodes = len(player_nodes)

        for node in player_nodes:
            where_can_go = self._where_can_go(node)
            num_of_nodes_can_go = len(where_can_go)
            for n in where_can_go:
                if n.piece:
                    num_of_nodes_can_go -= 1

            if not num_of_nodes_can_go:
                num_of_player_nodes -= 1

        logger.debug(f"num_of_player_nodes = {num_of_player_nodes}")

        if not num_of_player_nodes and self._count_pieces_left_of_player(color) > 3 \
                and (self.white_pieces == 0 if color == WHITE else self.black_pieces == 0):
            logger.info("Player {} is blocked!".format(player))
            return True
        else:
            return False

    def _get_turn_color(self):
        if self.turn == PLAYER1:
            return WHITE
        else:
            return BLACK
