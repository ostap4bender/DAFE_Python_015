import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QBasicTimer, Qt

deactive_btn = "background-color: peachpuff"

class Life(QWidget):
    def __init__(self, speed = 60):
        super().__init__()
        self.grid = []
        self.started = False
        self.active_btns = 0
        self.active_btn = "background-color: black"

        self.cell_width = 40
        self.cell_height = 40
       
        self.timer = QBasicTimer()
        self.speed = speed
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 850)
        self.setWindowTitle("Life game")
        self.setStyleSheet("background-color: black") 
  

        self.start_btn = QPushButton("Start", self)
        self.start_btn.resize(50,50)
        self.start_btn.setStyleSheet("background-color: cyan")
        self.start_btn.move(20,10)
        self.start_btn.clicked.connect(self.init_game)

        self.green_btn = QPushButton("Green", self)
        self.green_btn.resize(50,50)
        self.green_btn.setStyleSheet("background-color: green")
        self.green_btn.move(130,10)
        self.green_btn.clicked.connect(self.change_cl_green)

        self.yellow_btn = QPushButton("Yellow", self)
        self.yellow_btn.resize(50,50)
        self.yellow_btn.setStyleSheet("background-color: yellow")
        self.yellow_btn.move(190,10)
        self.yellow_btn.clicked.connect(self.change_cl_yellow)

        self.blue_btn = QPushButton("Blue", self)
        self.blue_btn.resize(50,50)
        self.blue_btn.setStyleSheet("background-color: blue")
        self.blue_btn.move(250,10)
        self.blue_btn.clicked.connect(self.change_cl_blue)

        self.slider = QSlider(Qt.Horizontal,self)
        self.slider.setRange(10, 100)
        self.slider.move(440,30)

        self.size_btn = QPushButton("Size", self)
        self.size_btn.resize(50,50)
        self.size_btn.setStyleSheet("background-color: cyan")
        self.size_btn.move(370,10)
        self.size_btn.clicked.connect(self.set_size)

        self.clean_btn = QPushButton("Clean", self)
        self.clean_btn.resize(50,50)
        self.clean_btn.setStyleSheet("background-color: cyan")
        self.clean_btn.move(700,10)
        self.clean_btn.clicked.connect(self.clean_win)

        self.quit_btn = QPushButton("Quit", self)
        self.quit_btn.resize(50,50)
        self.quit_btn.setStyleSheet("background-color: magenta")
        self.quit_btn.move(600,10)
        self.quit_btn.clicked.connect(self.quit_game)
          
        self.show()

    def change_cl_green(self):
        self.active_btn = "background-color: green"
    def change_cl_yellow(self):
        self.active_btn = "background-color: yellow"
    def change_cl_blue(self):
        self.active_btn = "background-color: blue"


    def clean_win(self):
        self.draw_grid()

    def set_size(self): # устанавливаем размер кнопок
        self.started = True
        self.cell_size = self.slider.value() # размер задается слайдером
        self.draw_grid()

    def draw_grid(self):
        if not self.grid == []:  # если поле не пустое, прячем его
            for i in self.grid:
                for j in i:
                    j.hide()

        self.cell_width = 700 // self.cell_size
        self.cell_height = 700 // self.cell_size
        self.grid = []
        for x in range(0, 700, self.cell_size):
            line = []
            for y in range(0, 700, self.cell_size):
                btn = QPushButton(self)
                btn.setStyleSheet(deactive_btn)
                btn.clicked.connect(self.clicked)
                btn.move(x+30, y+70)
                btn.resize(self.cell_size, self.cell_size)
                btn.status = False
                btn.show()

                line.append(btn)

            self.grid.append(line)

    def clicked(self):
        btn = self.sender()
        if btn.status:
            btn.status = False
            btn.setStyleSheet(deactive_btn)
            self.active_btns -= 1
        else:
            btn.status = True
            btn.setStyleSheet(self.active_btn)
            self.active_btns += 1

    def start_game(self):
        self.changed = False
        generation = []

        for i in range(self.cell_width):
            line = []
            for j in range(self.cell_height):
                line.append(self.near(i, j))
            generation.append(line)

        for i in range(self.cell_width):
            for j in range(self.cell_height):
                if not self.grid[i][j].status and generation[i][j] == 3:
                    self.grid[i][j].status = True
                    self.grid[i][j].setStyleSheet(self.active_btn)
                    self.active_btns += 1
                    self.changed = True
                elif self.grid[i][j].status and (generation[i][j] != 3 and generation[i][j] != 2):
                    self.grid[i][j].status = False
                    self.grid[i][j].setStyleSheet(deactive_btn)
                    self.active_btns -= 1
                    self.changed = True
                self.grid[i][j].show()

        if self.active_btns <= 0:
            self.timer.stop()

    def near(self, i, j):
            kolvo = 0        

            if self.grid[i-1][j-1].status:
                kolvo += 1
            if self.grid[i-1][j].status:
                kolvo += 1
            if self.grid[i-1][(j+1)%(self.cell_height)].status:
                kolvo += 1
            if self.grid[i][j-1].status:
                kolvo += 1
            if self.grid[i][(j+1)%self.cell_height].status:
                kolvo += 1
            if self.grid[(i+1)%self.cell_width][j-1].status:
                kolvo += 1
            if self.grid[(i+1)%self.cell_width][j].status:
                kolvo += 1
            if self.grid[(i+1)%self.cell_width][(j+1)%self.cell_height].status:
                kolvo += 1

            return kolvo

    def timerEvent(self, event):
        self.start_game()
        if self.active_btns <= 0:
            self.timer.stop()


    def init_game(self):
        if self.started:
            self.changed = False
            if self.timer.isActive():
                self.timer.stop()
                self.start_btn.setStyleSheet("background-color: cyan")
                self.start_btn.setText("Start")
            else:
                self.timer.start(self.speed, self)
                self.start_btn.setStyleSheet("background-color: red")
                self.start_btn.setText("Stop")
        else:
            pass
    def quit_game(self): # заканчиваем игру, прячем окно
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ob = Life()
    sys.exit(app.exec_())
