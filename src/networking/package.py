from dataclasses import dataclass

from src.game_objects.board import Board
from src.helpers import Boolean


@dataclass
class Package:
    started: Boolean
    board: Board
    change_turn: Boolean
