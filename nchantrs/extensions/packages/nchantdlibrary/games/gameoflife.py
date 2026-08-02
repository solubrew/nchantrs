from typing import Any
'\n---\n<(META)>:\n    docid:\n    name:\n    description: >\n    version: 0.0.0.0.0.0\n    authority: filesystem\n    security: seclvl2\n    <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.widgets.media.games.games import NchantdGameWidget
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdGameOfLife(NchantdGameWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdGameOfLife')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        logma.info(f'NchantdGameOfLife initialized')

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.run_game()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def run_game(self, board: list[list[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        neighbors = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
        rows = len(board)
        cols = len(board[0])
        copy_board = [[board[row][col] for col in range(cols)] for row in range(rows)]
        for row in range(rows):
            for col in range(cols):
                live_neighbors = 0
                for neighbor in neighbors:
                    r = row + neighbor[0]
                    c = col + neighbor[1]
                    if (r < rows and r >= 0) and (c < cols and c >= 0) and (copy_board[r][c] == 1):
                        live_neighbors += 1
                if copy_board[row][col] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                    board[row][col] = 0
                if copy_board[row][col] == 0 and live_neighbors == 3:
                    board[row][col] = 1