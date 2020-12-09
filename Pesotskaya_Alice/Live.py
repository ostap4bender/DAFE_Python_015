
'''
*Game of Life*

Игру «Жизнь» изобрел математик Джон Хортон Конуэй в 1970 году.

Правила игры следующие:
-«Жизнь» разыгрывается на зацикленном клеточном поле
-У каждой клетки 8 соседних клеток
-Каждая клетка может быть живой или мёртвой
-Клетка с двумя или тремя соседями выживает в следующем поколении, иначе погибает от одиночества или перенаселённости
-Мёртвая клетка с тремя соседями в следующем поколении становится живой

Чтобы начать игру нужно:
-Выбрать цвет живых клеток
-Указать ширину, высоту поля и размер клеток в нём
-Установить необходимые параметры, нажав кнопку "Select parameters"
-Начать симуляцию кнопкой "Start"

Во время симуляции кнопка "Start" изменится на "Stop", с её помощью можно остновить симуляцию в любой момент.
Чтобы выйти из игры, нажмите "Quit"
'''

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QBasicTimer

# неизменяемый размер окна
width_of_window = 800
height_of_window = 800

indent = 30

# диапазон размеров на поле
max_width_field = 600
max_height_field = 700
min_width_field = 100
min_height_field = 100
min_cell_size = 10
max_cell_size = 50

# стили кнопок
deactivate_button = "background-color: black"
activate_button = "background-color: pink"

font = "Arial"

class GameOfLife(QWidget):
    def __init__(self, speed = 60):
        super().__init__()

        self.timer = QBasicTimer()
        self.speed = speed

        self.field = []
        self.activate_buttons = 0

        self.initUI()

    def initUI(self):
        self.resize(width_of_window, height_of_window)
        self.setWindowTitle("Game of Life")

        self.button_start = QPushButton("Start", self)
        self.button_start.setFont(QFont(font, 14))
        self.button_start.setStyleSheet("background-color: white")
        self.button_start.move(max_width_field + 2 * indent, indent)
        self.button_start.clicked.connect(self.initGame)

        self.lbl1 = QLabel("Select color: ", self)
        self.lbl1.setFont(QFont(font, 14))
        self.lbl1.move(max_width_field + 2 * indent, 3 * indent)

        self.green = QRadioButton("Green", self)
        self.green.setFont(QFont(font, 14))
        self.green.move(max_width_field + 2 * indent, 4 * indent)
        self.green.clicked.connect(self.changeColor)

        self.blue = QRadioButton("Blue", self)
        self.blue.setFont(QFont(font, 14))
        self.blue.move(max_width_field + 2 * indent, 5 * indent)
        self.blue.clicked.connect(self.changeColor)

        self.yellow = QRadioButton("Yellow", self)
        self.yellow.setFont(QFont(font, 14))
        self.yellow.move(max_width_field + 2 * indent, 6 * indent)
        self.yellow.clicked.connect(self.changeColor)

        self.red = QRadioButton("Red", self)
        self.red.setFont(QFont(font, 14))
        self.red.move(max_width_field + 2 * indent, 7 * indent)
        self.red.clicked.connect(self.changeColor)

        self.lbl_w = QLabel("Width:", self)
        self.lbl_w.setFont(QFont(font, 14))
        self.lbl_w.move(max_width_field + 2 * indent, 9 * indent)
        self.input_w = QSpinBox(self)
        self.input_w.move(max_width_field + 2 * indent, 10 * indent)
        self.input_w.resize(80, 50)
        self.input_w.setFont(QFont(font, 14))
        self.input_w.setMinimum(min_width_field)
        self.input_w.setMaximum(max_width_field)

        self.lbl_h = QLabel("Height:", self)
        self.lbl_h.setFont(QFont(font, 14))
        self.lbl_h.move(max_width_field + 2 * indent, 12 * indent)
        self.input_h = QSpinBox(self)
        self.input_h.move(max_width_field + 2 * indent, 13 * indent)
        self.input_h.resize(80, 50)
        self.input_h.setFont(QFont(font, 14))
        self.input_h.setMinimum(min_height_field)
        self.input_h.setMaximum(max_height_field)

        self.lbl_c = QLabel("Cells size:", self)
        self.lbl_c.setFont(QFont(font, 14))
        self.lbl_c.move(max_width_field + 2 * indent, 15 * indent)
        self.input_c = QSpinBox(self)
        self.input_c.move(max_width_field + 2 * indent, 16 * indent)
        self.input_c.resize(80, 50)
        self.input_c.setFont(QFont(font, 14))
        self.input_c.setMinimum(min_cell_size)
        self.input_c.setMaximum(max_cell_size)

        self.button_size = QPushButton("Select\n parameters", self)
        self.button_size.setFont(QFont(font, 14))
        self.button_size.resize(130, 60)
        self.button_size.move(max_width_field + 2 * indent, 18 * indent)
        self.button_size.clicked.connect(self.selectSize)

        self.button_quit = QPushButton("Quit", self)
        self.button_quit.setFont(QFont(font, 14))
        self.button_quit.setStyleSheet("background-color: red")
        self.button_quit.move(max_width_field + 3 * indent, 22 * indent)
        self.button_quit.clicked.connect(self.close)

        self.show()

    def changeColor(self):
        global activate_button
        if self.green.isChecked():
            activate_button = "background-color: green"
        elif self.blue.isChecked():
            activate_button = "background-color: blue"
        elif self.red.isChecked():
            activate_button = "background-color: red"
        else:
            activate_button = "background-color: yellow"

    def selectSize(self):
        self.width = self.input_w.value()
        self.height = self.input_h.value()
        self.cell_size = self.input_c.value()
        self.drawButtons()

    def drawButtons(self):
        if not self.field == []:
            for i in self.field:
                for j in i:
                    j.hide()
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.field = []
        for x in range(0, self.width, self.cell_size):
            line = []
            for y in range(0, self.height, self.cell_size):
                button = QPushButton(self)
                button.setStyleSheet(deactivate_button)
                button.clicked.connect(self.Clicked)
                button.move(x+indent, y+indent)
                button.resize(self.cell_size, self.cell_size)
                button.status = False
                button.show()

                line.append(button)

            self.field.append(line)

    def Clicked(self):
        button = self.sender()
        if button.status:
            button.status = False
            button.setStyleSheet(deactivate_button)
            self.activate_buttons -= 1
        else:
            button.status = True
            button.setStyleSheet(activate_button)
            self.activate_buttons += 1

    def timerEvent(self, event):
        self.startGame()
        if self.activate_buttons <= 0:
            self.timer.stop()

    def startGame(self):
        self.changed = False

        generation = []
        for i in range(self.cell_width):
            line = []
            for j in range(self.cell_height):
                line.append(self.neibours(i, j))
            generation.append(line)

        for i in range(self.cell_width):
            for j in range(self.cell_height):
                if not self.field[i][j].status and generation[i][j] == 3:
                    self.field[i][j].status = True
                    self.field[i][j].setStyleSheet(activate_button)
                    self.activate_buttons += 1
                    self.changed = True
                elif self.field[i][j].status and (generation[i][j] != 3 and generation[i][j] != 2):
                    self.field[i][j].status = False
                    self.field[i][j].setStyleSheet(deactivate_button)
                    self.activate_buttons -= 1
                    self.changed = True
                self.field[i][j].show()

        if self.activate_buttons <= 0 and not self.changed:
            self.timer.stop()

    def neibours(self, i, j):
        c = 0
        if i == 0:
            next_i = 1
            prev_i = self.cell_width-1
        elif i == self.cell_width - 1:
            next_i = 0
            prev_i = self.cell_width-2
        else:
            next_i = i+1
            prev_i = i-1

        if j == 0:
            next_j = 1
            prev_j = self.cell_height-1
        elif j == self.cell_height - 1:
            next_j = 0
            prev_j = self.cell_height-2
        else:
            next_j = j + 1
            prev_j = j - 1

        if self.field[prev_i][prev_j].status:
            c += 1
        if self.field[prev_i][j].status:
            c += 1
        if self.field[prev_i][next_j].status:
            c += 1
        if self.field[i][prev_j].status:
            c += 1
        if self.field[i][next_j].status:
            c += 1
        if self.field[next_i][prev_j].status:
            c += 1
        if self.field[next_i][j].status:
            c += 1
        if self.field[next_i][next_j].status:
            c += 1

        return c

    def initGame(self):
        self.changed = False
        if self.timer.isActive():
            self.timer.stop()
            self.button_start.setText("Start")
        else:
            self.timer.start(self.speed, self)
            self.button_start.setText("Stop")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameOfLife()
    sys.exit(app.exec_())

