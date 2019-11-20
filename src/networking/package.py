from dataclasses import dataclass
from typing import Union

from src.game_objects.board import Board
from src.helpers import Boolean


@dataclass
class Package:
    started: Boolean
    board: Union[Board, None]
    change_turn: Boolean
