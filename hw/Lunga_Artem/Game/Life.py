import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel
from PyQt5.QtWidgets import QSlider, QApplication, QCheckBox, QLineEdit
from PyQt5.QtCore import QBasicTimer, Qt

BORDERS = 25
SIDE_WIDTH = 250
SIDE = 2 * BORDERS + SIDE_WIDTH
FIELD_TOP = 30
FIELD_BUTTON = 15
BUTTON_WIDTH = 80
BUTTON_LENGTH = 40
DISTANCE = 10
SIZE_CELL = 15
NUMBER_CELL_WIDTH = 40
NUMBER_CELL_LENGTH = 40
SIZE_TEXT = 15

START_BUTTON = "border-radius: 0.5em; background-color: #b6bebe"
CLEAR_BUTTON = "border-radius: 0.5em; background-color: #b6bebe"
CLOSE_BUTTON = "border-radius: 0.5em; background-color: #b6bebe"
GRID_BUTTON = "border-radius: 0.5em; background-color: #b6bebe"
INPUT = "background-color: white; border: 0; border-radius: 0.5em; color: black; font-size: 15px; font-weight: 600;"
NO_CLICKED_CELL_FIRST = "background-color:"
CLICKED_CELL_FIRST = "background-color:"
GRID_DESIGN = ";border: 0.5px solid #f7f7f7"
NO_GRID_DESIGN = ";border: 0px"
CELL_COLOR = "#772226"
COLLOR_WITHOUT_CELL = "#c8cbcb"
COLOR_NOW = CELL_COLOR
NO_CLICKED_CELL = NO_CLICKED_CELL_FIRST + COLLOR_WITHOUT_CELL + GRID_DESIGN
CLICKED_CELL = CLICKED_CELL_FIRST + CELL_COLOR + GRID_DESIGN
WIN = "background-color: #dfe2e2; border: 0; font-family: Arial; font-size: "+ str(SIZE_TEXT) +"px;" \
            "font-weight: 600; color: black;"

class game_life(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initialization()

    def initialization(self):
        self.setStyleSheet(WIN)
        self.setFixedSize(NUMBER_CELL_WIDTH * SIZE_CELL + SIDE + BORDERS,
                          NUMBER_CELL_LENGTH * SIZE_CELL + 2 * FIELD_TOP)

        self.generations_count = 0
        self.main_count = 0
        self.speed = 85
        
        self.buttons = list()
        self.is_grid = True
        self.is_cycle = True

        self.timer = QBasicTimer()

        self.button_start = QPushButton("Start", self)
        self.button_start.clicked.connect(self.start_game)
        self.button_start.setStyleSheet(START_BUTTON)

        self.button_clear = QPushButton("Clear", self)
        self.button_clear.clicked.connect(self.clear_field)
        self.button_clear.setStyleSheet(CLEAR_BUTTON)


        self.button_close = QPushButton("Quit", self)
        self.button_close.clicked.connect(sys.exit)
        self.button_close.setStyleSheet(CLOSE_BUTTON)

        self.label_length = QLabel("Length:", self)
        self.label_width = QLabel("Width:", self)

        self.input_length = QLineEdit(self)
        self.input_length.setStyleSheet(INPUT)
        self.input_width = QLineEdit(self)
        self.input_width.setStyleSheet(INPUT)

        self.button_size = QPushButton("Ok", self)
        self.button_size.clicked.connect(self.field_resize)
        self.button_size.setStyleSheet(START_BUTTON)

        self.label_change = QLabel("Change color:", self)

        self.input_change = QLineEdit(self)
        self.input_change.setStyleSheet(INPUT)

        self.button_change = QPushButton("Change", self)
        self.button_change.clicked.connect(self.color_status)
        self.button_change.setStyleSheet(START_BUTTON)

        self.label_speed = QLabel("Speed:", self)
        
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.valueChanged[int].connect(self.change_speed)
        self.slider.setValue(50)
        
        self.checkbox_cycle = QCheckBox("Cycle: on", self)
        self.checkbox_cycle.toggle()
        self.checkbox_cycle.stateChanged.connect(self.change_cycle)

        self.button_hide_grid = QPushButton("Hide grid", self)
        self.button_hide_grid.clicked.connect(self.grid)
        self.button_hide_grid.setStyleSheet(GRID_BUTTON)

        self.size_button()

        for i in range(NUMBER_CELL_LENGTH):
            self.buttons.append(list())

            for j in range(NUMBER_CELL_WIDTH):
                button = QPushButton("", self)
                button.setStyleSheet(NO_CLICKED_CELL)
                button.clicked.connect(self.button_pressed)
                button.status = False
                button.setGeometry(BORDERS + j * SIZE_CELL,
                                   FIELD_TOP + i * SIZE_CELL, SIZE_CELL,
                                   SIZE_CELL)

                self.buttons[i].append(button)

        self.statusBar()
        self.setGeometry(75, 75, NUMBER_CELL_WIDTH * SIZE_CELL + SIDE + BORDERS,
                         NUMBER_CELL_LENGTH * SIZE_CELL + 2 * FIELD_TOP)
        self.setWindowTitle("Conway's Game of Life")
        self.show()

    def change_cycle(self):
        if self.is_cycle:
            self.checkbox_cycle.setText("Cycle: off")
        else:
            self.checkbox_cycle.setText("Cycle: on")
        self.is_cycle = not self.is_cycle

    def size_button(self):
        point = BORDERS * 2 + NUMBER_CELL_WIDTH * SIZE_CELL

        self.button_start.setGeometry(point, FIELD_TOP, BUTTON_WIDTH,
                                      BUTTON_LENGTH)
        self.button_clear.setGeometry(point + BUTTON_WIDTH + DISTANCE, 
                                      FIELD_TOP, BUTTON_WIDTH, BUTTON_LENGTH)
        self.button_close.setGeometry(point + 2 * (BUTTON_WIDTH + DISTANCE),
                                      FIELD_TOP, BUTTON_WIDTH, BUTTON_LENGTH)
        
        self.label_length.setGeometry(
            point, FIELD_TOP + BUTTON_LENGTH + (FIELD_TOP - SIZE_TEXT) // 2,
            (SIDE_WIDTH - 2 * FIELD_BUTTON) // 3, SIZE_TEXT)
        self.label_width.setGeometry(
            point + BUTTON_WIDTH + DISTANCE,
            FIELD_TOP + BUTTON_LENGTH + (FIELD_TOP - SIZE_TEXT) // 2,
            (SIDE_WIDTH - 2 * FIELD_BUTTON) // 3, SIZE_TEXT)
        self.input_length.setGeometry(point,2 * FIELD_TOP + BUTTON_LENGTH,
                                      BUTTON_WIDTH, BUTTON_LENGTH)
        self.input_width.setGeometry(point + BUTTON_WIDTH + DISTANCE,
                                     2 * FIELD_TOP + BUTTON_LENGTH,
                                     BUTTON_WIDTH, BUTTON_LENGTH)

        self.button_size.setGeometry(point + 2 * (BUTTON_WIDTH + DISTANCE),
                                     2 * FIELD_TOP + BUTTON_LENGTH,
                                     BUTTON_WIDTH, BUTTON_LENGTH)
        
        self.label_change.setGeometry(
            point, 2 * FIELD_TOP + 2 * BUTTON_LENGTH +
            (FIELD_TOP - SIZE_TEXT) // 2, SIDE_WIDTH, SIZE_TEXT)
        self.input_change.setGeometry(
            point, 3 * FIELD_TOP + 2 * BUTTON_LENGTH, 2 * BUTTON_WIDTH 
            + DISTANCE, BUTTON_LENGTH)
        
        self.button_change.setGeometry(point + 2 * (BUTTON_WIDTH + DISTANCE),
                                       3 * FIELD_TOP + 2 * BUTTON_LENGTH,
                                       BUTTON_WIDTH, BUTTON_LENGTH)

        self.label_speed.setGeometry(
            point,3 * BUTTON_LENGTH + 3 * FIELD_TOP +
            (FIELD_TOP - SIZE_TEXT) // 2, SIDE_WIDTH, SIZE_TEXT)

        self.slider.setGeometry(
            point,4 * FIELD_TOP + 3 * BUTTON_LENGTH, 
            3 * BUTTON_WIDTH + 2 * DISTANCE, BUTTON_LENGTH)

        self.checkbox_cycle.setGeometry(
            point,4 * FIELD_TOP + 4 * BUTTON_LENGTH + FIELD_BUTTON,
            SIDE_WIDTH, FIELD_TOP)
        
        self.button_hide_grid.setGeometry(
            point + BUTTON_WIDTH + 4 * DISTANCE, 4 * FIELD_TOP + 
            4 * BUTTON_LENGTH + FIELD_BUTTON,
            2 * (BUTTON_WIDTH - DISTANCE), BUTTON_LENGTH)

    def change_speed(self, val):
        if val > 60:
            self.speed = -2 * val + 200
        else:
            if val == 0:
                self.speed = 1000
            else:
                self.speed = 1200 // int(val**0.5) - 85
        
        if self.timer.isActive():
            self.timer.start(self.speed, self)

    def clear_field(self):
        for i in range(NUMBER_CELL_LENGTH):
            for j in range(NUMBER_CELL_WIDTH):
                self.buttons[i][j].status = False
                self.buttons[i][j].setStyleSheet(NO_CLICKED_CELL)
        self.main_count = 0

    def timerEvent(self, e):
        self.game()
        if self.main_count <= 0:
            self.timer.stop()

    def grid(self):
        global CLICKED_CELL
        global NO_CLICKED_CELL
        if self.button_hide_grid.text() == "Hide grid":
            CLICKED_CELL = CLICKED_CELL_FIRST + COLOR_NOW + NO_GRID_DESIGN
            NO_CLICKED_CELL = NO_CLICKED_CELL_FIRST + COLLOR_WITHOUT_CELL + NO_GRID_DESIGN
            self.is_grid = False
            self.button_hide_grid.setText("Show grid")
            for i in range(NUMBER_CELL_LENGTH):
                for j in range(NUMBER_CELL_WIDTH):
                    if self.buttons[i][j].status:
                        self.buttons[i][j].setStyleSheet(CLICKED_CELL)
                    else:
                        self.buttons[i][j].setStyleSheet(NO_CLICKED_CELL)
        else:
            self.is_grid = True
            CLICKED_CELL = CLICKED_CELL_FIRST + COLOR_NOW + GRID_DESIGN
            NO_CLICKED_CELL = NO_CLICKED_CELL_FIRST + COLLOR_WITHOUT_CELL + GRID_DESIGN
            self.button_hide_grid.setText("Hide grid")
            for i in range(NUMBER_CELL_LENGTH):
                for j in range(NUMBER_CELL_WIDTH):
                    if self.buttons[i][j].status:
                        self.buttons[i][j].setStyleSheet(CLICKED_CELL)
                    else:
                        self.buttons[i][j].setStyleSheet(NO_CLICKED_CELL)

    def color_status(self):
        string = str(self.input_change.text())
        global COLOR_NOW
        global CLICKED_CELL
        if string == "":
            COLOR_NOW = CELL_COLOR
            if self.is_grid:
                CLICKED_CELL = CLICKED_CELL_FIRST + CELL_COLOR + GRID_DESIGN
            else:
                CLICKED_CELL = CLICKED_CELL_FIRST + CELL_COLOR + NO_GRID_DESIGN
        else:
            COLOR_NOW = str(string)
            if self.is_grid:
                CLICKED_CELL = CLICKED_CELL_FIRST + COLOR_NOW + GRID_DESIGN
            else:
                CLICKED_CELL = CLICKED_CELL_FIRST + COLOR_NOW + NO_GRID_DESIGN
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                if self.buttons[i][j].status == True:
                    self.buttons[i][j].setStyleSheet(CLICKED_CELL)

    def field_resize(self):
        self.main_count = 0
        self.generations_count = 0
        global BUTTON_LENGTH

        new_length = int(self.input_length.text())
        new_width = int(self.input_width.text())
        if new_length < 25:
            self.input_length.setText("25")
            return
        if new_width < 25:
            self.input_width.setText("25")    
            return
        if new_length > 60:
            self.input_length.setText("60")
            return
        if new_width > 60:
            self.input_width.setText("60")    
            return
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                self.buttons[i][j].deleteLater()
        global NUMBER_CELL_LENGTH
        NUMBER_CELL_LENGTH = new_length
        global NUMBER_CELL_WIDTH
        NUMBER_CELL_WIDTH = new_width
        self.buttons.clear()
        for i in range(new_length):
            self.buttons.append(list())
            for j in range(new_width):
                temp = QPushButton("", self)
                temp.setStyleSheet(NO_CLICKED_CELL)
                temp.clicked.connect(self.button_pressed)
                temp.status = False
                temp.setGeometry(BORDERS + j * SIZE_CELL,FIELD_TOP + i * 
                                 SIZE_CELL, SIZE_CELL,SIZE_CELL)
                temp.show()

                self.buttons[i].append(temp)
                
        if NUMBER_CELL_LENGTH * SIZE_CELL < (6 * BUTTON_LENGTH + 5 * FIELD_BUTTON):
            BUTTON_LENGTH = (NUMBER_CELL_LENGTH * SIZE_CELL - 5 * FIELD_BUTTON) // 6
        self.setGeometry(75, 75, NUMBER_CELL_WIDTH * SIZE_CELL + SIDE + BORDERS,
                         NUMBER_CELL_LENGTH * SIZE_CELL + 2 * FIELD_TOP)

        self.size_button()
        self.setFixedSize(NUMBER_CELL_WIDTH * SIZE_CELL + SIDE + BORDERS,
                          NUMBER_CELL_LENGTH * SIZE_CELL + 2 * FIELD_TOP)

    def button_pressed(self):

        ship = self.sender()
        if ship.status == False:
            ship.status = True
            ship.setStyleSheet(CLICKED_CELL)
            self.main_count += 1
        else:
            ship.status = False
            ship.setStyleSheet(NO_CLICKED_CELL)
            self.main_count -= 1

    def start_game(self):
        self.generations_count = 0
        self.it_changed = False
        if self.timer.isActive():
            self.timer.stop()
            self.button_start.setText('Start')
        else:
            self.timer.start(self.speed, self)
            self.button_start.setText('Stop')

    def game(self):
        self.it_changed = False

        generations_now = list()
        for i in range(NUMBER_CELL_LENGTH):
            generations_now.append(list())
            for j in range(NUMBER_CELL_WIDTH):
                generations_now[i].append(self.counting(i, j))

        for i in range(NUMBER_CELL_LENGTH):
            for j in range(NUMBER_CELL_WIDTH):
                if generations_now[i][j] == 3 and not self.buttons[i][j].status:
                    self.buttons[i][j].status = True
                    self.buttons[i][j].setStyleSheet(CLICKED_CELL)
                    self.main_count += 1
                    self.it_changed = True
                elif generations_now[i][j] not in (2, 3) and self.buttons[i][j].status:
                    self.buttons[i][j].status = False
                    self.buttons[i][j].setStyleSheet(NO_CLICKED_CELL)
                    self.main_count -= 1
                    self.it_changed = True
                self.buttons[i][j].show()

        self.generations_count += 1
        self.statusBar().showMessage("     Generations : {}".format(
            self.generations_count))

        if self.main_count <= 0 or not self.it_changed:
            self.button_start.setText("Start")
            self.timer.stop()

    def counting(self, i, j):
        if self.is_cycle:
            count = 0
            if i == 0:
                next_i = 1
                previous_i = NUMBER_CELL_LENGTH - 1
            elif i == NUMBER_CELL_LENGTH - 1:
                previous_i = NUMBER_CELL_LENGTH - 2
                next_i = 0
            else:
                previous_i = i - 1
                next_i = i + 1

            if j == 0:
                next_j = 1
                previous_j = NUMBER_CELL_WIDTH - 1
            elif j == NUMBER_CELL_WIDTH - 1:
                previous_j = NUMBER_CELL_WIDTH - 2
                next_j = 0
            else:
                next_j = j + 1
                previous_j = j - 1
                
            if self.buttons[previous_i][previous_j].status:
                count += 1
            if self.buttons[previous_i][j].status:
                count += 1
            if self.buttons[previous_i][next_j].status:
                count += 1
            if self.buttons[i][previous_j].status:
                count += 1
            if self.buttons[i][next_j].status:
                count += 1
            if self.buttons[next_i][previous_j].status:
                count += 1
            if self.buttons[next_i][j].status:
                count += 1
            if self.buttons[next_i][next_j].status:
                count += 1
            return count
        
        else:
            count = 0
            if i > 0:
                if j > 0:
                    if self.buttons[i - 1][j - 1].status:
                        count += 1
                if j < NUMBER_CELL_WIDTH - 1:
                    if self.buttons[i - 1][j + 1].status:
                        count += 1
                if self.buttons[i - 1][j].status:
                    count += 1
            if i < NUMBER_CELL_LENGTH - 1:
                if j > 0:
                    if self.buttons[i + 1][j - 1].status:
                        count += 1
                if j < NUMBER_CELL_WIDTH - 1:
                    if self.buttons[i + 1][j + 1].status:
                        count += 1
                if self.buttons[i + 1][j].status:
                    count += 1
            if j > 0:
                if self.buttons[i][j - 1].status:
                    count += 1
            if j < NUMBER_CELL_WIDTH - 1:
                if self.buttons[i][j + 1].status:
                    count += 1
            return count


if __name__ == '__main__':

    app = QApplication(sys.argv)
    play = game_life()
    sys.exit(app.exec_())