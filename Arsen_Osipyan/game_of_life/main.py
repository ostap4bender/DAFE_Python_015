import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLineEdit, QCheckBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
import random

import styles as css


MARGIN = 20
EL_MARGIN = 10
EL_WIDTH = 160
EL_HEIGHT = 35
EL_FORM_WIDTH = int((EL_WIDTH - 2 * EL_MARGIN)/3)
SIDEBAR_WIDTH = 2 * MARGIN + EL_WIDTH
TEXT_H = 18

# Default: BURN(3,) / SURVIVE(2, 3)
# Interest: BURN(5,6,7,8) / SURVIVE(4, 5, 6, 7, 8) draw line
# Interest: BURN(1,) / SURVIVE(0, 1, 2, 3, 4, 5, 6, 7, 8)
# Interest: BURN(3,) / SURVIVE(1, 2, 3, 4, 5, 6, 7, 8)
# Interest: BURN(1, 2, 3, 4) / SURVIVE(6, 7, 8) one cell in the center
BURN = (1, 2, 3, 4)
SURVIVE = (6, 7, 8)


class GameOfLife(QMainWindow):

    def __init__(self):
        super().__init__()

        self.height = 0         # [cells]
        self.width = 0          # [cells]
        self.generations = 0    # number of generations
        self.counter = 0        # counter of alive cells
        self.table = list()     # table of cells
        self.cache = list()     # cleared version
        self.looped = False     # loop mode or finite mode
        self.random = False     # random generation
        self.random_rarity = 2  # if self.random = True

        # Constants
        self.cell_size = 10     # [px]
        self.max_height = 80    # [cells]
        self.max_width = 80     # [cells]
        self.min_height = 24    # [cells]
        self.min_width = 24     # [cells]

        self.initUI()

    def initUI(self):
        # Status bar
        self.status = self.statusBar()
        self.update_status()

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.simulate)

        # Buttons
        self.btn_start = QPushButton("start", self)
        self.btn_start.clicked.connect(self.start_clicked)

        self.btn_clear = QPushButton("clear", self)
        self.btn_clear.clicked.connect(self.clear_clicked)

        self.btn_confirm = QPushButton("ok", self)
        self.btn_confirm.clicked.connect(self.resize_table)

        self.btn_close = QPushButton("quit", self)
        self.btn_close.clicked.connect(self.exit)

        # Form
        self.input_h = QLineEdit(self)
        self.input_w = QLineEdit(self)

        # Checkbox
        self.check_looped = QCheckBox("looped table", self)
        self.check_looped.stateChanged.connect(self.set_looped)

        self.check_random = QCheckBox("random", self)
        self.check_random.stateChanged.connect(self.set_random)

        # Table
        self.create_table(self.max_width, self.max_height)

        # Geometry
        self.set_geometry()

        # Window parameters
        self.setWindowTitle('Game Of Life')

        # Styles applying
        self.setWindowIcon(QIcon("./gol_icon.png"))
        self.setStyleSheet(css.WINDOW_CSS)

        self.btn_start.setStyleSheet(css.START_CSS)
        self.btn_clear.setStyleSheet(css.CLEAR_CSS)
        self.btn_close.setStyleSheet(css.CLOSE_CSS)
        self.btn_confirm.setStyleSheet(css.CONFIRM_CSS)

        self.input_h.setStyleSheet(css.INPUT_CSS)
        self.input_w.setStyleSheet(css.INPUT_CSS)

        self.check_looped.setStyleSheet(css.CHECKBOX_CSS)
        self.check_random.setStyleSheet(css.CHECKBOX_CSS)

        self.status.setStyleSheet(css.STATUS_CSS)

        # Show UI
        self.show()

    def set_geometry(self):
        # Window
        self.setGeometry(
            100, 100,
            self.cell_size * self.width + SIDEBAR_WIDTH + 2 * MARGIN,
            self.cell_size * self.height + 2 * MARGIN
        )
        self.setFixedSize(
            self.cell_size * self.width + SIDEBAR_WIDTH + 2 * MARGIN,
            self.cell_size * self.height + 2 * MARGIN
        )

        # Sidebar
        self.btn_start.setGeometry(
            3 * MARGIN + self.cell_size * self.width,
            MARGIN,
            EL_WIDTH, EL_HEIGHT
        )
        self.btn_clear.setGeometry(
            3 * MARGIN + self.cell_size * self.width,
            MARGIN + EL_HEIGHT + EL_MARGIN,
            EL_WIDTH, EL_HEIGHT
        )
        self.btn_close.setGeometry(
            3 * MARGIN + self.cell_size * self.width,
            self.cell_size * self.height + MARGIN - EL_HEIGHT,
            EL_WIDTH, EL_HEIGHT
        )
        self.btn_confirm.setGeometry(
            3 * MARGIN + self.cell_size * self.width + 2 * EL_MARGIN + 2 * EL_FORM_WIDTH,
            MARGIN + 2 * EL_HEIGHT + 2 * EL_MARGIN,
            EL_FORM_WIDTH, EL_HEIGHT
        )
        self.input_w.setGeometry(
            3 * MARGIN + self.cell_size * self.width,
            MARGIN + 2 * EL_HEIGHT + 2 * EL_MARGIN,
            EL_FORM_WIDTH, EL_HEIGHT
        )
        self.input_h.setGeometry(
            3 * MARGIN + self.cell_size * self.width + EL_MARGIN + EL_FORM_WIDTH,
            MARGIN + 2 * EL_HEIGHT + 2 * EL_MARGIN,
            EL_FORM_WIDTH, EL_HEIGHT
        )
        self.check_looped.setGeometry(
            3 * MARGIN + self.cell_size * self.width,
            MARGIN + 3 * EL_HEIGHT + 3 * EL_MARGIN,
            EL_WIDTH - 2*EL_MARGIN, TEXT_H
        )
        self.check_random.setGeometry(
            3 * MARGIN + self.cell_size * self.width,
            MARGIN + 3 * EL_HEIGHT + 4 * EL_MARGIN + TEXT_H,
            EL_WIDTH - 2*EL_MARGIN, TEXT_H
        )

    def button_clicked(self):
        if not self.sender().status:
            self.sender().status = True
            self.sender().setStyleSheet(css.ALIVE_CSS)
            self.counter += 1
        else:
            self.sender().status = False
            self.sender().setStyleSheet(css.DEAD_CSS)
            self.counter -= 1

    def start_clicked(self):
        if self.btn_start.text() == "start":
            self.timer.start(100)
            self.btn_start.setText("stop")
            self.btn_clear.setText("clear")
        elif self.btn_start.text() == "stop":
            self.pause()

    def simulate(self):
        cur_gen = []
        for i in range(self.height):
            cur_gen.append(list())
            for j in range(self.width):
                cur_gen[i].append(self.count(i, j))

        for i in range(self.height):
            for j in range(self.width):
                if cur_gen[i][j] in BURN and not self.table[i][j].status:
                    self.table[i][j].status = True
                    self.table[i][j].setStyleSheet(css.ALIVE_CSS)
                    self.counter += 1
                elif cur_gen[i][j] not in SURVIVE and self.table[i][j].status:
                    self.table[i][j].status = False
                    self.table[i][j].setStyleSheet(css.DEAD_CSS)
                    self.counter -= 1
                self.table[i][j].show()

        self.generations += 1
        self.update_status()
        if self.counter == 0:
            # We can use self.pause() if we can
            # If we want to exit from simulation,
            # we should use self.clear_table()
            # If we want to pause table and not
            # finish simulation - use self.pause()
            self.clear_table()

    def clear_clicked(self):
        if self.btn_clear.text() == "clear":
            self.clear_table()
            self.btn_clear.setText("recover")
        elif self.btn_clear.text() == "recover":
            self.recover_table()
            self.btn_clear.setText("clear")

    def clear_table(self):
        self.cache.clear()

        self.cache.append((self.generations, self.counter))
        self.generations = 0
        self.counter = 0

        self.cache.append(list())
        for i in range(self.height):
            self.cache[1].append(list())
            for j in range(self.width):
                self.cache[1][i].append(self.table[i][j].status)
                self.table[i][j].status = False
                self.table[i][j].setStyleSheet(css.DEAD_CSS)
                self.table[i][j].show()

        self.pause()
        self.update_status()

    def recover_table(self):
        if self.cache:
            self.generations, self.counter = self.cache[0]
            self.update_status()

            for i in range(len(self.cache[1])):
                for j in range(len(self.cache[1][0])):
                    self.table[i][j].status = self.cache[1][i][j]
                    if self.table[i][j].status:
                        self.table[i][j].setStyleSheet(css.ALIVE_CSS)
                    else:
                        self.table[i][j].setStyleSheet(css.DEAD_CSS)
                    self.table[i][j].show()

    def pause(self):
        self.timer.stop()
        self.btn_start.setText("start")

    def resize_table(self):
        if self.btn_start.text() == "stop":
            self.pause()
        self.cache.clear()
        self.btn_clear.setText("clear")

        try:
            if self.input_h.text():
                new_h = max(min(self.max_height, int(self.input_h.text())), self.min_height)
            else:
                new_h = self.height
        except BaseException:
            new_h = self.height

        try:
            if self.input_w.text():
                new_w = max(min(self.max_width, int(self.input_w.text())), self.min_width)
            else:
                new_w = self.width
        except BaseException:
            new_w = self.width

        self.create_table(new_w, new_h)
        self.update_status()
        self.set_geometry()

    def create_table(self, w, h):
        self.counter = 0
        self.generations = 0

        for i in range(self.height):
            for j in range(self.width):
                self.table[i][j].deleteLater()
        self.table.clear()

        for i in range(h):
            self.table.append(list())
            for j in range(w):
                tmp = QPushButton("", self)
                tmp.clicked.connect(self.button_clicked)
                tmp.setGeometry(
                    MARGIN + j * self.cell_size, MARGIN + i * self.cell_size,
                    self.cell_size, self.cell_size
                )
                if self.random:
                    tmp.status = not bool(random.randint(0, self.random_rarity-1))
                    if tmp.status:
                        tmp.setStyleSheet(css.ALIVE_CSS)
                    else:
                        tmp.setStyleSheet(css.DEAD_CSS)
                else:
                    tmp.status = False
                    tmp.setStyleSheet(css.DEAD_CSS)
                self.table[i].append(tmp)
                self.table[i][-1].show()

        self.height = h
        self.width = w

    def update_status(self):
        self.status.showMessage("Generations: {}\tAlive: {}".format(self.generations, self.counter))

    def exit(self):
        self.close()

    def set_looped(self):
        self.looped = not self.looped

    def set_random(self):
        self.random = not self.random

    def count(self, i, j):
        count = 0
        if self.looped:
            if self.table[(i-1) % self.height][(j-1) % self.width].status:
                count += 1
            if self.table[i][(j-1) % self.width].status:
                count += 1
            if self.table[(i+1) % self.height][(j-1) % self.width].status:
                count += 1
            if self.table[(i-1) % self.height][(j+1) % self.width].status:
                count += 1
            if self.table[i][(j+1) % self.width].status:
                count += 1
            if self.table[(i+1) % self.height][(j+1) % self.width].status:
                count += 1
            if self.table[(i-1) % self.height][j].status:
                count += 1
            if self.table[(i+1) % self.height][j].status:
                count += 1
        else:
            if i > 0:
                if j > 0:
                    if self.table[i - 1][j - 1].status:
                        count += 1
                if j < self.width - 1:
                    if self.table[i - 1][j + 1].status:
                        count += 1
                if self.table[i - 1][j].status:
                    count += 1
            if i < self.height - 1:
                if j > 0:
                    if self.table[i + 1][j - 1].status:
                        count += 1
                if j < self.width - 1:
                    if self.table[i + 1][j + 1].status:
                        count += 1
                if self.table[i + 1][j].status:
                    count += 1
            if j > 0:
                if self.table[i][j - 1].status:
                    count += 1
            if j < self.width - 1:
                if self.table[i][j + 1].status:
                    count += 1
        return count


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameOfLife()
    sys.exit(app.exec_())
