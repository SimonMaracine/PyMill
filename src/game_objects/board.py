import pygame
from src.display import WIDTH, HEIGHT
from src.game_objects.piece import Piece
from src.game_objects.node import Node
from src.constants import *
from src.fonts import board_font


class Board:
    """Game board object."""

    def __init__(self):
        self.width = HEIGHT - 60
        self.x = (WIDTH - self.width) // 2
        self.y = (HEIGHT - self.width) // 2
        self.DIV = self.width // 6
        self.nodes = (
            Node(self.x, self.y, (0, 1, 1, 0)),
            Node(self.x + self.DIV * 3, self.y, (0, 1, 1, 1)),
            Node(self.x + self.DIV * 6, self.y, (0, 1, 0, 1)),  # line
            Node(self.x + self.DIV, self.y + self.DIV, (0, 1, 1, 0)),
            Node(self.x + self.DIV * 3, self.y + self.DIV, (1, 1, 1, 1)),
            Node(self.x + self.DIV * 5, self.y + self.DIV, (0, 1, 0, 1)),  # line
            Node(self.x + self.DIV * 2, self.y + self.DIV * 2, (0, 1, 1, 0)),
            Node(self.x + self.DIV * 3, self.y + self.DIV * 2, (1, 0, 1, 1)),
            Node(self.x + self.DIV * 4, self.y + self.DIV * 2, (0, 1, 0, 1)),  # line
            Node(self.x, self.y + self.DIV * 3, (1, 1, 1, 0)),
            Node(self.x + self.DIV, self.y + self.DIV * 3, (1, 1, 1, 1)),
            Node(self.x + self.DIV * 2, self.y + self.DIV * 3, (1, 1, 0, 1)),  # line
            Node(self.x + self.DIV * 4, self.y + self.DIV * 3, (1, 1, 1, 0)),
            Node(self.x + self.DIV * 5, self.y + self.DIV * 3, (1, 1, 1, 1)),
            Node(self.x + self.DIV * 6, self.y + self.DIV * 3, (1, 1, 0, 1)),  # line
            Node(self.x + self.DIV * 2, self.y + self.DIV * 4, (1, 0, 1, 0)),
            Node(self.x + self.DIV * 3, self.y + self.DIV * 4, (0, 1, 1, 1)),
            Node(self.x + self.DIV * 4, self.y + self.DIV * 4, (1, 0, 0, 1)),  # line
            Node(self.x + self.DIV, self.y + self.DIV * 5, (1, 0, 1, 0)),
            Node(self.x + self.DIV * 3, self.y + self.DIV * 5, (1, 1, 1, 1)),
            Node(self.x + self.DIV * 5, self.y + self.DIV * 5, (1, 0, 0, 1)),  # line
            Node(self.x, self.y + self.DIV * 6, (1, 0, 1, 0)),
            Node(self.x + self.DIV * 3, self.y + self.DIV * 6, (1, 0, 1, 1)),
            Node(self.x + self.DIV * 6, self.y + self.DIV * 6, (1, 0, 0, 1))  # line
        )
        for node in self.nodes:  # Correct the position of each node.
            node.x += 1
            node.y += 1
        self.turn = PLAYER1
        self.white_pieces = 9
        self.black_pieces = 9
        self.phase = PHASE1
        self.picked_up_piece = None  # has picked up a piece
        self.node_taken_piece = None
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
        self.game_over = False
        self.turns_without_windmills = 0
        self.winner = tuple
        # self.phase2_now()

    def render(self, surface: pygame.Surface):
        self.show_board(surface)
        for node in self.nodes:
            node.render(surface)
            if node.piece:
                node.piece.render(surface)
                if node.remove_thingy and self.turn_color() != node.piece.color:
                    node.render_remove_thingy(surface)
        if self.phase == PHASE1:
            self.show_player_pieces(surface, board_font)
        self.show_player_indicator(surface, board_font)

    def update(self, mouse: tuple, mouse_pressed: tuple):
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        for node in self.nodes:
            node.update(mouse_x, mouse_y, self.must_remove_piece)
            if node.piece is not None:
                node.piece.update(mouse_x, mouse_y)

    def put_new_piece(self):
        for node in self.nodes:
            if node.highlight and not node.piece:
                if self.turn == PLAYER1:
                    new_piece = Piece(node.x, node.y, WHITE)
                    node.add_piece(new_piece)
                    self.white_pieces -= 1
                    if not self.check_windmills(WHITE, node):
                        self.switch_turn()
                    else:
                        self.must_remove_piece = True
                        print("Remove a piece!")
                else:
                    new_piece = Piece(node.x, node.y, BLACK)
                    node.add_piece(new_piece)
                    self.black_pieces -= 1
                    if not self.check_windmills(BLACK, node):
                        self.switch_turn()
                    else:
                        self.must_remove_piece = True
                        print("Remove a piece!")
                break
        if (self.white_pieces + self.black_pieces) == 0:
            self.phase = PHASE2
            print("PHASE2")

    def pick_up_piece(self):
        for node in self.nodes:
            if node.highlight and node.piece and not self.picked_up_piece:
                if node.piece.pick_up(self.turn):
                    self.change_node_color(node, (0, 255, 0), (255, 0, 0))
                    self.node_taken_piece = node
                    self.picked_up_piece = node.piece
                break

    def remove_opponent_piece(self):
        """Removes a piece from opponent."""
        for node in self.nodes:
            if self.turn == PLAYER1:
                if node.highlight and node.piece and node.piece.color == BLACK:
                    if not self.check_windmills(BLACK, node) or \
                            self.number_pieces_in_windmills(BLACK) == self.count_pieces(BLACK):
                        node.take_piece()
                        self.must_remove_piece = False
                        if self.check_player_pieces(BLACK):
                            self.game_over = True  # game is over
                        self.switch_turn()
                    else:
                        print("You cannot take piece from windmill!")
            else:
                if node.highlight and node.piece and node.piece.color == WHITE:
                    if not self.check_windmills(WHITE, node) or \
                            self.number_pieces_in_windmills(WHITE) == self.count_pieces(WHITE):
                        node.take_piece()
                        self.must_remove_piece = False
                        if self.check_player_pieces(WHITE):
                            self.game_over = True  # game is over
                        self.switch_turn()
                    else:
                        print("You cannot take piece from windmill!")
        self.node_pressed = False

    def put_down_piece(self) -> bool:
        """Puts down a picked up piece.

        Returns:
            bool: True if the turn was changed, False otherwise.

        """
        changed_turn = False
        if self.picked_up_piece:
            for node in self.where_can_go(self.node_taken_piece):
                if node.highlight and not node.piece:
                    node.add_piece(self.picked_up_piece)
                    print(node.piece)
                    self.change_node_color(self.node_taken_piece, (0, 0, 0), (0, 0, 0))
                    self.node_taken_piece.piece.release(node)
                    self.node_taken_piece.take_piece()
                    self.node_taken_piece = None
                    self.picked_up_piece = None
                    if not self.check_windmills(WHITE if self.turn == PLAYER1 else BLACK, node):
                        self.switch_turn()
                        changed_turn = True
                    else:
                        self.must_remove_piece = True
                        print("Remove a piece!")

        # Release piece if player released the left button.
        if self.picked_up_piece:
            self.change_node_color(self.node_taken_piece, (0, 0, 0), (0, 0, 0))
            self.picked_up_piece.release(self.node_taken_piece)
            self.picked_up_piece = None

        if self.check_player_pieces(WHITE if self.turn == PLAYER1 else BLACK):  # inverse WHITE and BLACK because turn
            if not self.must_remove_piece:                                      # was already switched
                self.game_over = True  # game is over
        return changed_turn

    def clicked_on_node(self) -> bool:
        for node in self.nodes:
            if node.highlight:
                return True
        return False

    def show_board(self, surface):
        # Drawing three rectangles...
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.width), 2)
        pygame.draw.rect(surface, (0, 0, 0), (self.x + self.DIV, self.y + self.DIV,
                                              self.width - self.DIV * 2, self.width - self.DIV * 2), 2)
        pygame.draw.rect(surface, (0, 0, 0), (self.x + self.DIV * 2, self.y + self.DIV * 2,
                                              self.width - self.DIV * 4, self.width - self.DIV * 4), 2)
        # ...and four middle lines.
        pygame.draw.line(surface, (0, 0, 0), (self.x + self.DIV * 3, self.y),
                         (self.x + self.DIV * 3, self.y + self.DIV * 2), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x, self.y + self.DIV * 3),
                         (self.x + self.DIV * 2, self.y + self.DIV * 3), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x + self.DIV * 3, self.y + self.DIV * 6),
                         (self.x + self.DIV * 3, self.y + self.DIV * 4), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x + self.DIV * 6, self.y + self.DIV * 3),
                         (self.x + self.DIV * 4, self.y + self.DIV * 3), 2)

    def show_player_pieces(self, surface, font):
        player1_text = font.render("x {}".format(self.white_pieces), True, (0, 0, 0))
        player2_text = font.render("x {}".format(self.black_pieces), True, (0, 0, 0))
        surface.blit(player1_text, (20, HEIGHT//2 - 30))
        surface.blit(player2_text, (WIDTH - 20 - player2_text.get_width(), HEIGHT // 2 - 30))

    def show_player_indicator(self, surface, font):
        text = font.render("Player: {}".format(self.turn), True, (0, 0, 0))
        surface.blit(text, (5, 60))

    def switch_turn(self):
        if self.turn == PLAYER1:
            self.turn = PLAYER2
        else:
            self.turn = PLAYER1

    @staticmethod
    def check_nodes(w_mill: tuple, color: tuple) -> bool:
        """Checks if all nodes within a group of nodes have pieces of the same color.

        Args:
            w_mill (tuple): The group of nodes to check (a possible windmill).
            color (tuple): The color that the pieces all need to be.

        Returns:
            bool: True if the nodes within the windmill actually form a windmill, False otherwise.

        """
        nodes = []
        for n in w_mill:
            if n.piece and n.piece.color == color:
                nodes.append(True)
            else:
                nodes.append(False)
        if all(nodes):
            return True
        else:
            return False

    def check_windmills(self, color: tuple, node: Node) -> bool:
        """Checks if there is a windmill formed and if node is any of the windmill's nodes.

        Args:
            color (tuple): The color of the pieces it checks.
            node (Node): The node to check if is any of windmill's nodes.

        Returns:
            bool: True if there is a windmill and if node is in there, False otherwise.

        """
        for i, windmill in enumerate(self.windmills):
            if self.check_nodes(windmill, color) and any(map(lambda n: n is node, windmill)):
                print("{} windmill: {}".format(color, i))
                self.turns_without_windmills = 0
                return True
        return False

    def count_pieces(self, color: tuple) -> int:
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
        print(pieces)
        return pieces

    def check_player_pieces(self, color: tuple) -> bool:
        """Checks the number of pieces of a player and returns when the game is over.

        If the player has 3 pieces remaining, his/her pieces can go anywhere and if 2 pieces remaining, he/she loses.

        Args:
            color (tuple): The color of the pieces to check.

        Returns:
            bool: True if the game is over, False otherwise.

        """
        player = PLAYER1 if color == WHITE else PLAYER2
        pieces_left = self.count_pieces(color)

        if self.phase == PHASE2:
            if pieces_left == 3:
                self.can_jump[player] = True
            else:
                self.can_jump[player] = False

            if pieces_left == 2:
                win = "White won!" if player == PLAYER2 else "Black won!"
                print(win)
                print("Game is over.")
                self.winner = WHITE if player == PLAYER2 else BLACK
                return True

        pieces_to_check = (self.black_pieces < 2) if player is PLAYER2 else (self.white_pieces < 2)
        if pieces_to_check:
            if self.is_opponent_blocked(player):
                win = "White won!" if player is PLAYER2 else "Black won!"
                print(win)
                print("Game is over.")
                self.winner = WHITE if player == PLAYER2 else BLACK
                return True

        return False

    def where_can_go(self, node: Node) -> tuple:
        """Decides where a piece can go based on the dictionary self.can_jump.

        Args:
            node (Node): The node from where the piece wants to go.

        Returns:
            tuple: The nodes where the piece can go.

        """
        if node is None:
            raise TypeError("Node shouldn't be None...")

        if self.turn == PLAYER1 and not self.can_jump[PLAYER1] or self.turn == PLAYER2 and not self.can_jump[PLAYER2]:
            return node.search_neighbors(self.nodes, self.DIV)
        else:
            new_nodes = list(self.nodes)
            new_nodes.remove(node)
            return tuple(new_nodes)

    def number_pieces_in_windmills(self, color: tuple) -> int:
        """Counts the number of pieces that are inside of every windmill.

        Args:
            color (tuple): The color of the pieces to count.

        Returns:
            int: The number of pieces that are inside windmills.

        """
        pieces_inside_windmills = set()
        for windmill in self.windmills:
            if self.check_nodes(windmill, color):
                for node in windmill:
                    pieces_inside_windmills.add(node)
        return len(pieces_inside_windmills)

    def change_node_color(self, node: Node, color1: tuple, color2: tuple):
        """Changes color of other nodes based on where the piece can go.

        Args:
            node (Node): The node where the piece currently sits.
            color1 (tuple): The color to change the nodes where the piece can go.
            color2 (tuple): The color to change the nodes where the piece cannot go.

        """
        for n in self.where_can_go(node):
            n.change_color(color1)

        nodes_copy = list(self.nodes)
        for i in self.nodes:
            for j in self.where_can_go(node):
                if i is j:
                    nodes_copy.remove(i)
        nodes_copy.remove(node)

        for n in nodes_copy:
            n.change_color(color2)

    def is_opponent_blocked(self, player: int) -> bool:
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

        print("Player " + str(player))
        player_nodes = [node for node in self.nodes if node.piece and node.piece.color == color]
        num_of_player_nodes = len(player_nodes)

        for node in player_nodes:
            where_can_go = self.where_can_go(node)
            num_of_nodes_can_go = len(where_can_go)
            # print(where_can_go)
            for n in where_can_go:
                if n.piece:
                    num_of_nodes_can_go -= 1

            if not num_of_nodes_can_go:
                num_of_player_nodes -= 1

        if not num_of_player_nodes and self.count_pieces(color) > 3 \
                and self.white_pieces == 0 if color == WHITE else self.black_pieces == 0:
            print("Player {} is blocked!".format(player))
            return True
        else:
            return False

    def turn_color(self):
        if self.turn == 1:
            return WHITE
        else:
            return BLACK

    def phase2_now(self):
        """Automatically puts all pieces. Only for testing purposes."""
        w = True
        for node in self.nodes:
            if not node.piece and (self.white_pieces + self.black_pieces) > 0:
                if w:
                    new_piece = Piece(node.x, node.y, WHITE)
                    node.add_piece(new_piece)
                    self.switch_turn()
                    self.white_pieces -= 1
                    w = not w
                else:
                    new_piece = Piece(node.x, node.y, BLACK)
                    node.add_piece(new_piece)
                    self.switch_turn()
                    self.black_pieces -= 1
                    w = not w
