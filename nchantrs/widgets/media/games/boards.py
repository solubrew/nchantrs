# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
from typing import Any

"""
---
<(META)>:
    docid:
    name:
    description: >
    version: 0.0.0.0.0.0
    authority: filesystem
    security: seclvl2
    <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.widgets import NchantdWidget

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NchantdGameBoard(NchantdWidget):
    """"""

    board_width = 10
    board_height = 22
    score_changed = Signal(int)
    level_changed = Signal(int)
    lines_removed_changed = Signal(int)

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

        self.timer = QBasicTimer()
        self.nextPieceLabel = None
        self._is_waiting_after_line = False
        self._cur_piece = TetrixPiece()
        self._next_piece = TetrixPiece()
        self._cur_x = 0
        self._cur_y = 0
        self._num_lines_removed = 0
        self._num_pieces_dropped = 0
        self.score = 0
        self.level = 0
        self.board = None

        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setFocusPolicy(Qt.StrongFocus)
        self._is_started = False
        self._is_paused = False
        self.clear_board()

        self._next_piece.set_random_shape()
        logma.info(f"NchantdGameBoard initialized")


    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def shape_at(self, x, y) -> Any:
        return self.board[(y * TetrixBoard.board_width) + x]

    def set_shape_at(self, x, y, shape) -> None:
        self.board[(y * TetrixBoard.board_width) + x] = shape

    def timeout_time(self) -> int:
        return 1000 / (1 + self.level)

    def square_width(self) -> Any:
        return self.contentsRect().width() / TetrixBoard.board_width

    def square_height(self) -> Any:
        return self.contentsRect().height() / TetrixBoard.board_height

    def set_next_piece_label(self, label) -> None:
        self.nextPieceLabel = label

    def sizeHint(self) -> Any:
        return QSize(
            TetrixBoard.board_width * 15 + self.frameWidth() * 2, TetrixBoard.board_height * 15 + self.frameWidth() * 2
        )

    def minimum_size_hint(self) -> Any:
        return QSize(
            TetrixBoard.board_width * 5 + self.frameWidth() * 2, TetrixBoard.board_height * 5 + self.frameWidth() * 2
        )

    @Slot()
    def start(self) -> None:
        if self._is_paused:
            return

        self._is_started = True
        self._is_waiting_after_line = False
        self._num_lines_removed = 0
        self._num_pieces_dropped = 0
        self.score = 0
        self.level = 1
        self.clear_board()

        self.lines_removed_changed.emit(self._num_lines_removed)
        self.score_changed.emit(self.score)
        self.level_changed.emit(self.level)

        self.new_piece()
        self.timer.start(self.timeout_time(), self)

    @Slot()
    def pause(self) -> None:
        if not self._is_started:
            return

        self._is_paused = not self._is_paused
        if self._is_paused:
            self.timer.stop()
        else:
            self.timer.start(self.timeout_time(), self)

        self.update()

    def paintEvent(self, event) -> None:
        super(TetrixBoard, self).paintEvent(event)

        with QPainter(self) as painter:
            rect = self.contentsRect()

            if self._is_paused:
                painter.drawText(rect, Qt.AlignCenter, "Pause")
                return

            board_top = rect.bottom() - TetrixBoard.board_height * self.square_height()

            for i in range(TetrixBoard.board_height):
                for j in range(TetrixBoard.board_width):
                    shape = self.shape_at(j, TetrixBoard.board_height - i - 1)
                    if shape != Piece.NoShape:
                        self.draw_square(
                            painter, rect.left() + j * self.square_width(), board_top + i * self.square_height(), shape
                        )

            if self._cur_piece.shape() != Piece.NoShape:
                for i in range(4):
                    x = self._cur_x + self._cur_piece.x(i)
                    y = self._cur_y - self._cur_piece.y(i)
                    self.draw_square(
                        painter,
                        rect.left() + x * self.square_width(),
                        board_top + (TetrixBoard.board_height - y - 1) * self.square_height(),
                        self._cur_piece.shape(),
                    )

    def keyPressEvent(self, event) -> None:
        if not self._is_started or self._is_paused or self._cur_piece.shape() == Piece.NoShape:
            super(TetrixBoard, self).keyPressEvent(event)
            return

        key = event.key()
        if key == Qt.Key_Left:
            self.try_move(self._cur_piece, self._cur_x - 1, self._cur_y)
        elif key == Qt.Key_Right:
            self.try_move(self._cur_piece, self._cur_x + 1, self._cur_y)
        elif key == Qt.Key_Down:
            self.try_move(self._cur_piece.rotated_right(), self._cur_x, self._cur_y)
        elif key == Qt.Key_Up:
            self.try_move(self._cur_piece.rotated_left(), self._cur_x, self._cur_y)
        elif key == Qt.Key_Space:
            self.drop_down()
        elif key == Qt.Key_D:
            self.one_line_down()
        else:
            super(TetrixBoard, self).keyPressEvent(event)

    def timerEvent(self, event) -> None:
        if event.timerId() == self.timer.timerId():
            if self._is_waiting_after_line:
                self._is_waiting_after_line = False
                self.new_piece()
                self.timer.start(self.timeout_time(), self)
            else:
                self.one_line_down()
        else:
            super(TetrixBoard, self).timerEvent(event)

    def clear_board(self) -> None:
        self.board = [Piece.NoShape for _ in range(TetrixBoard.board_height * TetrixBoard.board_width)]

    def drop_down(self) -> None:
        drop_height = 0
        new_y = self._cur_y
        while new_y > 0:
            if not self.try_move(self._cur_piece, self._cur_x, new_y - 1):
                break
            new_y -= 1
            drop_height += 1

        self.piece_dropped(drop_height)

    def one_line_down(self) -> None:
        if not self.try_move(self._cur_piece, self._cur_x, self._cur_y - 1):
            self.piece_dropped(0)

    def piece_dropped(self, dropHeight) -> None:
        for i in range(4):
            x = self._cur_x + self._cur_piece.x(i)
            y = self._cur_y - self._cur_piece.y(i)
            self.set_shape_at(x, y, self._cur_piece.shape())

        self._num_pieces_dropped += 1
        if self._num_pieces_dropped % 25 == 0:
            self.level += 1
            self.timer.start(self.timeout_time(), self)
            self.level_changed.emit(self.level)

        self.score += dropHeight + 7
        self.score_changed.emit(self.score)
        self.remove_full_lines()

        if not self._is_waiting_after_line:
            self.new_piece()

    def remove_full_lines(self) -> None:
        num_full_lines = 0

        for i in range(TetrixBoard.board_height - 1, -1, -1):
            line_is_full = True

            for j in range(TetrixBoard.board_width):
                if self.shape_at(j, i) == Piece.NoShape:
                    line_is_full = False
                    break

            if line_is_full:
                num_full_lines += 1
                for k in range(i, TetrixBoard.board_height - 1):
                    for j in range(TetrixBoard.board_width):
                        self.set_shape_at(j, k, self.shape_at(j, k + 1))

                for j in range(TetrixBoard.board_width):
                    self.set_shape_at(j, TetrixBoard.board_height - 1, Piece.NoShape)

        if num_full_lines > 0:
            self._num_lines_removed += num_full_lines
            self.score += 10 * num_full_lines
            self.lines_removed_changed.emit(self._num_lines_removed)
            self.score_changed.emit(self.score)

            self.timer.start(500, self)
            self._is_waiting_after_line = True
            self._cur_piece.set_shape(Piece.NoShape)
            self.update()

    def new_piece(self) -> None:
        self._cur_piece = self._next_piece
        self._next_piece.set_random_shape()
        self.show_next_piece()
        self._cur_x = TetrixBoard.board_width // 2 + 1
        self._cur_y = TetrixBoard.board_height - 1 + self._cur_piece.min_y()

        if not self.try_move(self._cur_piece, self._cur_x, self._cur_y):
            self._cur_piece.set_shape(Piece.NoShape)
            self.timer.stop()
            self._is_started = False

    def show_next_piece(self) -> None:
        if self.nextPieceLabel is not None:
            return

        dx = self._next_piece.max_x() - self._next_piece.min_x() + 1
        dy = self._next_piece.max_y() - self._next_piece.min_y() + 1

        pixmap = QPixmap(dx * self.square_width(), dy * self.square_height())
        with QPainter(pixmap) as painter:
            painter.fillRect(pixmap.rect(), self.nextPieceLabel.palette().background())

        for i in range(4):
            x = self._next_piece.x(i) - self._next_piece.min_x()
            y = self._next_piece.y(i) - self._next_piece.min_y()
            self.draw_square(painter, x * self.square_width(), y * self.square_height(), self._next_piece.shape())

        self.nextPieceLabel.setPixmap(pixmap)

    def try_move(self, newPiece, newX, newY) -> bool:
        for i in range(4):
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)
            if x < 0 or x >= TetrixBoard.board_width or y < 0 or y >= TetrixBoard.board_height:
                return False
            if self.shape_at(x, y) != Piece.NoShape:
                return False

        self._cur_piece = newPiece
        self._cur_x = newX
        self._cur_y = newY
        self.update()
        return True

    def draw_square(self, painter, x, y, shape) -> None:
        color_table = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC, 0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(color_table[shape])
        painter.fillRect(x + 1, y + 1, self.square_width() - 2, self.square_height() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.square_height() - 1, x, y)
        painter.drawLine(x, y, x + self.square_width() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.square_height() - 1, x + self.square_width() - 1, y + self.square_height() - 1)
        painter.drawLine(x + self.square_width() - 1, y + self.square_height() - 1, x + self.square_width() - 1, y + 1)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
