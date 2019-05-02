import pygame
from src.display import WIDTH, HEIGHT
from src.piece import Piece
from src.node import Node
from src.constants import *


class Table:
    def __init__(self):
        self.width = HEIGHT - 40
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
        self.font = pygame.font.SysFont("calibri", 30, True)
        self.faze = FAZE1
        self.picked_up_piece = None  # has picked up a piece
        self.node_taken_piece = None
        # self.faze2_now()

    def render(self, surface):
        # Drawing three rectangles...
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.width), 2)
        pygame.draw.rect(surface, (0, 0, 0), (self.x + self.DIV, self.y + self.DIV,
                                              self.width - self.DIV * 2, self.width - self.DIV * 2), 2)
        pygame.draw.rect(surface, (0, 0, 0), (self.x + self.DIV * 2, self.y + self.DIV * 2,
                                              self.width - self.DIV * 4, self.width - self.DIV * 4), 2)
        # ... and four middle lines.
        pygame.draw.line(surface, (0, 0, 0), (self.x + self.DIV * 3, self.y),
                         (self.x + self.DIV * 3, self.y + self.DIV * 2), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x, self.y + self.DIV * 3),
                         (self.x + self.DIV * 2, self.y + self.DIV * 3), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x + self.DIV * 3, self.y + self.DIV * 6),
                         (self.x + self.DIV * 3, self.y + self.DIV * 4), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x + self.DIV * 6, self.y + self.DIV * 3),
                         (self.x + self.DIV * 4, self.y + self.DIV * 3), 2)

        for node in self.nodes:
            node.render(surface)
            if node.piece:
                node.piece.render(surface)

        self.show_player_pieces(surface)
        self.show_player_indicator(surface)

    def update(self, mouse: tuple, mouse_pressed: tuple):
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        for node in self.nodes:
            node.update(mouse_x, mouse_y)
            if node.piece:
                node.piece.update(mouse_x, mouse_y)

        if self.faze == FAZE2:
            if mouse_pressed[0]:
                for node in self.nodes:
                    if node.highlight and node.piece and not self.picked_up_piece:
                        if node.piece.pick_up(self.turn):
                            for n in node.search_neighbors(self.nodes, self.DIV):
                                n.change_color((0, 255, 0))
                            self.node_taken_piece = node
                            self.picked_up_piece = node.piece
                        break
            else:
                if self.picked_up_piece:
                    for node in self.node_taken_piece.search_neighbors(self.nodes, self.DIV):
                        if node.highlight and not node.piece:
                            node.add_piece(self.picked_up_piece)
                            for n in self.node_taken_piece.search_neighbors(self.nodes, self.DIV):
                                n.change_color((0, 0, 0))
                            self.node_taken_piece.piece.release(node)
                            self.node_taken_piece.take_piece()
                            self.node_taken_piece = None
                            self.picked_up_piece = None
                            self.switch_turn()
                    if self.picked_up_piece:
                        for n in self.node_taken_piece.search_neighbors(self.nodes, self.DIV):
                            n.change_color((0, 0, 0))
                        self.picked_up_piece.release(self.node_taken_piece)
                        self.picked_up_piece = None

    def put_new_piece(self):
        for node in self.nodes:
            if node.highlight and not node.piece:
                if self.turn == PLAYER1 and self.white_pieces > 0:
                    new_piece = Piece(node.x, node.y, WHITE)
                    node.add_piece(new_piece)
                    self.white_pieces -= 1
                    self.switch_turn()
                elif self.turn == PLAYER2 and self.black_pieces > 0:
                    new_piece = Piece(node.x, node.y, BLACK)
                    node.add_piece(new_piece)
                    self.black_pieces -= 1
                    self.switch_turn()
                break
        if (self.white_pieces + self.black_pieces) == 0:
            self.faze = FAZE2
            print("FAZE2")

    def show_player_pieces(self, surface):
        player1_text = self.font.render("x {}".format(self.white_pieces), True, (0, 0, 0))
        player2_text = self.font.render("x {}".format(self.black_pieces), True, (0, 0, 0))
        surface.blit(player1_text, (20, HEIGHT//2 - 30))
        surface.blit(player2_text, (WIDTH - 20 - player2_text.get_width(), HEIGHT // 2 - 30))

    def show_player_indicator(self, surface):
        text = self.font.render("Player: {}".format(self.turn), True, (0, 0, 0))
        surface.blit(text, (5, 60))

    def switch_turn(self):
        if self.turn == PLAYER1:
            self.turn = PLAYER2
        else:
            self.turn = PLAYER1

    def check_windmills(self):
        pass

    def faze2_now(self):  # automatically put all pieces; developer only
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
