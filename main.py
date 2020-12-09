import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time


from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QFrame

colors = ['white', 'black', 'red', 'orange', 'yellow', 'green', 'blue', 'purple']
colors_ = {'white' : '#ffffff', 'black' : '#000000', 'red' : '#ff0000', 'orange' : '#ffa500',
           'yellow' : '#fff44f', 'green' : '#66ff00', 'blue' : '#0000ff', 'purple' : '#a020f0'}

class Field(QWidget):
    def __init__(self, parent, x_max, y_max, w, h):
        self.alive_c = 1
        self.dead_c = 0
        super().__init__(parent)
        self.w = w
        self.h = h
        self.x_max = x_max
        self.y_max = y_max
        self.alive = {}
        self.field = []
        self.setContentsMargins(100, 50, 100, 100)
        self.init_grid()

    def init_grid(self):
        self.clearMask()
        for x in range(self.x_max):
            tmp = []
            for y in range(self.y_max):
                btn = QPushButton()
                btn.setStyleSheet("background-color:" + colors[self.dead_c])
                btn.setObjectName(str(x) + ' '+ str(y))
                btn.setFixedSize(self.w/self.x_max, self.h/self.y_max)
                btn.clicked.connect(self.on_click)
                tmp.append(btn)
                self.alive[str(x) + ' ' + str(y)] = False
            self.field.append(tmp)
        self.grid = QGridLayout()
        for i in range(self.x_max):
            for j in range(self.y_max):
                self.grid.addWidget(self.field[i][j], i, j)
        self.setLayout(self.grid)
        self.show()

    def clean(self):
        for i in list(self.alive.keys()):
            self.alive[i] = False
        for x in range(self.x_max):
            for y in range(self.y_max):
                self.field[x][y].setStyleSheet("background-color:" + colors[self.dead_c])

    def reset(self):
        for x in range(self.x_max):
            for y in range(self.y_max):
                if self.alive[str(x) + ' ' + str(y)]:
                    self.field[x][y].setStyleSheet("background-color:" + colors[self.alive_c])
                else:
                    self.field[x][y].setStyleSheet("background-color:" + colors[self.dead_c])

    def get_alive_neighbors(self, cell, cells, a):
        x, y = (cell.split(' '))
        alive_neighbors = []
        neighbors = []
        for i in range(0, 3):
            for j in range(0, 3):
                if not i == j == 1:
                    neighbors.append(str(int(x) + i - 1) + ' ' + str(int(y) + j - 1))
        for nei in neighbors:
            if nei in cells:
                if a[nei]:
                    alive_neighbors.append(nei)
        return len(alive_neighbors)

    def calculate_new_era(self, a):
        cells = list(a.keys())
        b = {}
        for cell in cells:
            amount = self.get_alive_neighbors(cell, cells, a)
            if a[cell]:
                if amount == 2 or amount == 3:
                    b[cell] = True
                else:
                    b[cell] = False
            else:
                if amount == 3:
                    b[cell] = True
                else:
                    b[cell] = False
        return b

    def on_click(self):
        sender = self.sender()
        if sender.palette().button().color().name() == colors_[colors[self.dead_c]]:
            self.alive[sender.objectName()] = True
            self.col = "background-color:" + colors[self.alive_c]
        else:
            self.alive[sender.objectName()] = False
            self.col = "background-color:" + colors[self.dead_c]
        sender.setStyleSheet(self.col)

    def process(self):
        changed_alive = self.calculate_new_era(self.alive)
        key = False
        for i in self.alive.keys():
            if self.alive[i] != changed_alive[i]:
                key = True
        for x in range(self.x_max):
            for y in range(self.y_max):
                if changed_alive[str(x) + ' ' + str(y)]:
                    self.field[x][y].setStyleSheet("background-color:" + colors[self.alive_c])
                else:
                    self.field[x][y].setStyleSheet("background-color:" + colors[self.dead_c])
        self.alive = changed_alive
        return key


class MainWindow(QMainWindow):
    def __init__(self, x_max, y_max, w, h):
        super(MainWindow, self).__init__()
        self.w = w
        self.h = h
        self.x_max = x_max
        self.y_max = y_max
        self.init_ui()

    def init_ui(self):
        self.field = Field(self, self.x_max, self.y_max, self.w, self.h)
        self.statusBar().showMessage(str(self.x_max) + ' ' + str(self.y_max))
        self.setCentralWidget(self.field)
        self.resize(self.w, self.h)
        self.setWindowTitle('Game Life')

        self.process_button = QPushButton("Start", self)
        self.process_button.setStyleSheet("background-color:green")
        self.process_button.move(100, 0)
        self.process_button.setFixedSize(100, 50)
        self.process_button.clicked.connect(self.process)

        self.end_button = QPushButton("Quit", self)
        self.end_button.setStyleSheet("background-color:red")
        self.end_button.move(225, 0)
        self.end_button.setFixedSize(100, 50)
        self.end_button.clicked.connect(self.close)

        self.step_button = QPushButton("Step", self)
        self.step_button.setStyleSheet("background-color:blue")
        self.step_button.move(350, 0)
        self.step_button.setFixedSize(100, 50)
        self.step_button.clicked.connect(self.step)

        self.clean_button = QPushButton("Clean", self)
        self.clean_button.setStyleSheet("background-color:orange")
        self.clean_button.move(475, 0)
        self.clean_button.setFixedSize(100, 50)
        self.clean_button.clicked.connect(self.clean)

        self.timer = QBasicTimer()
        self.is_continue = True
        self.alive_color()
        self.dead_color()
        self.show()

    def clean(self):
        self.field.clean()

    def alive_color(self):
        self.alive_color = QComboBox(self)
        label = QLabel("Color of alive", self)
        label.move(0, 0)
        self.alive_color.addItem('black')
        self.alive_color.addItem('white')
        self.alive_color.addItems(colors[1:])
        self.alive_color.move(0, 50)
        self.alive_color.activated[str].connect(self.change_alive_color)

    def dead_color(self):
        self.dead_color = QComboBox(self)
        dlabel = QLabel("Color of dead", self)
        dlabel.move(0, 100)
        self.dead_color.addItems(colors)
        self.dead_color.move(0, 150)
        self.dead_color.activated[str].connect(self.change_dead_color)

    def change_alive_color(self, text):
        for i in range(len(colors)):
            if colors[i] == text:
                if i != self.field.dead_c:
                    self.field.alive_c = i
        self.field.reset()

    def change_dead_color(self, text):
        for i in range(len(colors)):
            if colors[i] == text:
                if i != self.field.alive_c:
                    self.field.dead_c = i
        self.field.reset()

    def step(self):
        self.is_continue = self.field.process()

    def process(self):
        if self.timer.isActive():
            self.timer.stop()
            self.process_button.setText('Start')
        else:
            self.timer.start(100, self)
            self.process_button.setText('Stop')

    def timerEvent(self, e):
        if not self.is_continue:
              self.timer.stop()
              self.process_button.setText('Start')
              self.is_continue = True
              return
        self.step()

if __name__ == '__main__':
    app = QApplication([])
    x_max = 20
    y_max = 20
    win = MainWindow(x_max, y_max, 600, 500)
    sys.exit(app.exec_())