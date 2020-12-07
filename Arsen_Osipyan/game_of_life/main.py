import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLineEdit
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

import styles as ss


class GameOfLife(QMainWindow):

    def __init__(self):
        super().__init__()

        self.cell_size = 20    # [px]

        self.generations = 0   # number of generations
        self.main_counter = 0  # counter of alive cells
        self.table = list()    # table of cells

        self.max_height = 40   # [cells]
        self.max_width = 80    # [cells]
        self.min_height = 10   # [cells]
        self.min_width = 10    # [cells]
        self.height = 20       # [cells]
        self.width = 40        # [cells]

        self.initUI()

    def initUI(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.simulate)

        # Start button
        self.btn_start = QPushButton("start", self)
        self.btn_start.setGeometry(ss.MARGIN_LR * 3 + self.width * self.cell_size, ss.MARGIN_TB,
                                   ss.BTN_WIDTH, ss.BTN_HEIGHT)
        self.btn_start.clicked.connect(self.start_simulate)

        # Close button
        self.btn_close = QPushButton("quit", self)
        self.btn_close.setGeometry(ss.MARGIN_LR * 3 + self.width * self.cell_size,
                                   self.height * self.cell_size + ss.MARGIN_TB - ss.BTN_HEIGHT,
                                   ss.BTN_WIDTH, ss.BTN_HEIGHT)
        self.btn_close.clicked.connect(self.exit)

        # Size form
        self.input_h = QLineEdit(self)
        self.input_w = QLineEdit(self)
        self.input_w.setGeometry(
            ss.MARGIN_LR * 3 + self.width * self.cell_size,
            ss.MARGIN_TB + ss.MARGIN_BTN + ss.BTN_HEIGHT,
            int((ss.BTN_WIDTH - 2 * ss.MARGIN_BTN) / 3), ss.BTN_HEIGHT)
        self.input_h.setGeometry(
            ss.MARGIN_LR * 3 + self.width * self.cell_size + int((ss.BTN_WIDTH + ss.MARGIN_BTN) / 3),
            ss.MARGIN_TB + ss.MARGIN_BTN + ss.BTN_HEIGHT,
            int((ss.BTN_WIDTH - 2 * ss.MARGIN_BTN) / 3), ss.BTN_HEIGHT)

        # Size confirm button
        self.btn_confirm = QPushButton("ok", self)
        self.btn_confirm.setGeometry(
            ss.MARGIN_LR * 3 + self.width * self.cell_size + 2 * int((ss.BTN_WIDTH + ss.MARGIN_BTN) / 3),
            ss.MARGIN_TB + ss.MARGIN_BTN + ss.BTN_HEIGHT,
            int((ss.BTN_WIDTH - 2 * ss.MARGIN_BTN) / 3), ss.BTN_HEIGHT)
        self.btn_confirm.clicked.connect(self.resize)

        # Table
        for i in range(self.height):
            self.table.append(list())
            for j in range(self.width):
                btn = QPushButton("", self)
                btn.setStyleSheet(ss.NON_ACTIVE_STYLE)
                btn.clicked.connect(self.button_clicked)
                btn.status = False
                btn.setGeometry(ss.MARGIN_LR + j * self.cell_size, ss.MARGIN_TB + i * self.cell_size,
                                self.cell_size, self.cell_size)
                self.table[i].append(btn)

        # Window parameters
        self.status = self.statusBar()
        self.setGeometry(100, 100, self.width * self.cell_size + ss.SIDEBAR_WIDTH + 2 * ss.MARGIN_LR,
                         self.height * self.cell_size + 2 * ss.MARGIN_TB)
        self.setFixedSize(self.width * self.cell_size + ss.SIDEBAR_WIDTH + 2 * ss.MARGIN_LR,
                          self.height * self.cell_size + 2 * ss.MARGIN_TB)
        self.setWindowTitle('Game Of Life')
        self.setWindowIcon(QIcon("gol_icon.png"))
        self.setStyleSheet(ss.WINDOW_STYLE)

        # Styles applying
        self.btn_start.setStyleSheet(ss.BTN_START_STYLE)
        self.btn_close.setStyleSheet(ss.BTN_CLOSE_STYLE)
        self.btn_confirm.setStyleSheet(ss.BTN_OK_STYLE)
        self.input_h.setStyleSheet(ss.INPUT_STYLE)
        self.input_w.setStyleSheet(ss.INPUT_STYLE)
        self.status.setStyleSheet(ss.STATUS_STYLE)

        self.show()

    def resize_sidebar(self):
        self.btn_close.setGeometry(
            ss.MARGIN_LR * 3 + self.width * self.cell_size,
            self.height * self.cell_size + ss.MARGIN_TB - ss.BTN_HEIGHT,
            ss.BTN_WIDTH, ss.BTN_HEIGHT)
        self.btn_start.setGeometry(
            ss.MARGIN_LR * 3 + self.width * self.cell_size, ss.MARGIN_TB,
            ss.BTN_WIDTH, ss.BTN_HEIGHT)

        self.input_w.setGeometry(
            ss.MARGIN_LR * 3 + self.width * self.cell_size,
            ss.MARGIN_TB + ss.MARGIN_BTN + ss.BTN_HEIGHT,
            int((ss.BTN_WIDTH - 2 * ss.MARGIN_BTN) / 3), ss.BTN_HEIGHT)
        self.input_h.setGeometry(
            ss.MARGIN_LR * 3 + self.width * self.cell_size + int((ss.BTN_WIDTH + ss.MARGIN_BTN) / 3),
            ss.MARGIN_TB + ss.MARGIN_BTN + ss.BTN_HEIGHT,
            int((ss.BTN_WIDTH - 2 * ss.MARGIN_BTN) / 3), ss.BTN_HEIGHT)

        self.btn_confirm.setGeometry(
            ss.MARGIN_LR * 3 + self.width * self.cell_size + 2 * int((ss.BTN_WIDTH + ss.MARGIN_BTN) / 3),
            ss.MARGIN_TB + ss.MARGIN_BTN + ss.BTN_HEIGHT,
            int((ss.BTN_WIDTH - 2 * ss.MARGIN_BTN) / 3), ss.BTN_HEIGHT)

    def resize_table(self, w, h):
        for i in range(self.height):
            for j in range(self.width):
                self.table[i][j].deleteLater()
        self.table.clear()

        for i in range(h):
            self.table.append(list())
            for j in range(w):
                tmp = QPushButton("", self)
                tmp.setStyleSheet(ss.NON_ACTIVE_STYLE)
                tmp.clicked.connect(self.button_clicked)
                tmp.status = False
                tmp.setGeometry(ss.MARGIN_LR + j * self.cell_size, ss.MARGIN_TB + i * self.cell_size,
                                self.cell_size, self.cell_size)
                self.table[i].append(tmp)
                self.table[i][-1].show()

        self.height = h
        self.width = w

    def resize(self):
        if self.btn_start.text() == "stop":
            self.pause()

        if self.input_h.text():
            new_h = max(min(self.max_height, int(self.input_h.text())), self.min_height)
        else:
            new_h = self.height
        if self.input_w.text():
            new_w = max(min(self.max_width, int(self.input_w.text())), self.min_width)
        else:
            new_w = self.width

        self.resize_table(new_w, new_h)
        self.resize_sidebar()
        self.setGeometry(100, 100, self.width * self.cell_size + ss.SIDEBAR_WIDTH + 2 * ss.MARGIN_LR,
                         self.height * self.cell_size + 2 * ss.MARGIN_TB)
        self.setFixedSize(self.width * self.cell_size + ss.SIDEBAR_WIDTH + 2 * ss.MARGIN_LR,
                          self.height * self.cell_size + 2 * ss.MARGIN_TB)

    def button_clicked(self):
        if not self.sender().status:
            self.sender().status = True
            self.sender().setStyleSheet(ss.ACTIVE_STYLE)
            self.main_counter += 1
        else:
            self.sender().status = False
            self.sender().setStyleSheet(ss.NON_ACTIVE_STYLE)
            self.main_counter -= 1

    def start_simulate(self):
        if self.btn_start.text() == "start":
            self.timer.start(100)
            self.btn_start.setText("stop")
        elif self.btn_start.text() == "stop":
            self.pause()

    def pause(self):
        self.generations = 0
        self.main_counter = 0
        self.timer.stop()
        self.btn_start.setText("start")
        self.status.showMessage("")

    def simulate(self):
        cur_gen = []
        for i in range(self.height):
            cur_gen.append(list())
            for j in range(self.width):
                cur_gen[i].append(self.count(i, j))

        for i in range(self.height):
            for j in range(self.width):
                if cur_gen[i][j] == 3 and not self.table[i][j].status:
                    self.table[i][j].status = True
                    self.table[i][j].setStyleSheet(ss.ACTIVE_STYLE)
                    self.main_counter += 1
                elif cur_gen[i][j] not in (2, 3) and self.table[i][j].status:
                    self.table[i][j].status = False
                    self.table[i][j].setStyleSheet(ss.NON_ACTIVE_STYLE)
                    self.main_counter -= 1
                self.table[i][j].show()

        self.generations += 1
        self.status.showMessage("Generations: {}".format(self.generations))
        print(self.main_counter)
        if self.main_counter <= 0:
            self.pause()

    def count(self, i, j):
        count = 0
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

    def exit(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameOfLife()
    sys.exit(app.exec_())
