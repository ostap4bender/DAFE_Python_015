import sys, random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


w, h = 3, 3
w_w, w_h = 1700, 1000
to_color = [[0 for i in range(100)] for j in range (100)]
nears = [[0 for i in range(100)] for j in range (100)]

colors = ['#add8e6', '#ff0000', 'green']

def clean():
    for i in range (4):
        for j in range(4):
            nears[i][j]=0
            to_color[i][j] = 0


def is_alive(i, j, w, h):
    s = 0
    #if (i > 0):
    s += to_color[(h + i-1)%h][j]
    s += to_color[(h + i-1)%h][(j+1)%w]
        #if j > 0:
    s+=to_color[(h + i-1)%h][(w+j-1)%w]
    s+=to_color[i][(w+j-1)%w]
    s+=to_color[(i+1)%h][(w+j-1)%w]
    # else:
    #     if j>0:
    #         s += to_color[i][j - 1]
    #         s += to_color[i + 1][ j - 1]
    s += to_color[(i+1)%h][ (j +1)%w]
    s += to_color[i][(j + 1)%w]
    s += to_color[(i + 1)%h][j]
    return s

def evolve():
    key = False
    for i in range (99):
        for j in range (99):
            if (nears[i][j] == 3):
                if (to_color[i][j] == 0):key = True
                to_color[i][j] = 1
                continue
            if (nears[i][j] != 2):
                if (to_color[i][j] != 0):key = True
                to_color[i][j] = 0
    return key





def Color_(s):
    return 'QPushButton {background-color:' + s + '}'
def get_col(s):
    return s.palette().button().color().name()


class Board(QWidget):
    b_list = [[0 for i in range(100)]for j in range (100)]
    def __init__(self,parent, wi, hi):
        self.w, self.h = wi, hi
        super().__init__(parent)
        self.col = colors[1]
        self.setContentsMargins(100, 50, 100, 100)
        self.initBoard()

    def initBoard(self):
        self.clearMask()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        positions = [(i, j) for i in range(self.h) for j in range(self.w)]
        for i, j in positions:
            self.b_list[i][j] = QPushButton()
            self.b_list[i][j].setStyleSheet(Color_(colors[0]))
            sz = min(int(w_w/self.w), int(w_h/self.h))
            self.b_list[i][j].setFixedSize(sz, sz)
            self.b_list[i][j].clicked.connect(self.on_click)  # соединение сигнала и слота (сигнал clicked и слот on_click)
            self.grid.addWidget(self.b_list[i][j], i, j)

        self.show()


    def on_click(self):
        sender = self.sender()
        if get_col(sender) == colors[0]:
            self.col = colors[1]
        else:
            self.col = colors[0]
        sender.setStyleSheet(Color_(self.col))

    def clean_colors(self):
        for i in range(self.h):
            for j in range(self.w):
                self.b_list[i][j].setStyleSheet(Color_(colors[0]))

    def renew_colors(self, key = 0):
        for i in range(self.h):
            for j in range(self.w):
                if(get_col(self.b_list[i][j]) != colors[1 - key]):
                    self.b_list[i][j].setStyleSheet(Color_(colors[key]))

    def process(self):
        for i in range(self.h):
            for j in range(self.w):
                if (get_col(self.b_list[i][j]) == colors[1]):
                    to_color[i][j] = 1
                else:
                    to_color[i][j] = 0
        for i in range(self.h):
            for j in range(self.w):
                nears[i][j] = is_alive(i, j, self.w, self.h)
        key = evolve()
        for i in range(self.h):
            for j in range(self.w):
                if to_color[i][j]:
                    self.b_list[i][j].setStyleSheet(Color_(colors[1]))
                else:
                    self.b_list[i][j].setStyleSheet(Color_(colors[0]))
        return key







class LifeGame(QMainWindow):
    def __init__(self ,w = 12, h = 12):
        super(LifeGame, self).__init__()
        self.w, self.h = w, h
        self.initUI()

    def initUI(self):
        self.tboard = Board(self, self.w, self.h)
        self.statusBar().showMessage(str(self.w) +' ' + str(self.h))
        self.setCentralWidget(self.tboard)
        self.resize(w_w, w_h)
        self.setWindowTitle('LifeGame')

        self.P_button = QPushButton('Step', self)
        self.E_button = QPushButton('Start', self)
        self.S_button = QPushButton('Dialog', self)
        self.C_button = QPushButton('Clean', self)
        self.Co_button = QPushButton('BackColor', self)
        self.Co2_button = QPushButton('LiveColor', self)

        self.Co_button.move(0, 340)
        self.Co_button.clicked.connect(self.colorDialog)
        self.Co_button.setMinimumSize(110, 70)
        self.Co_button.setStyleSheet(Color_("orange"))

        self.Co2_button.move(0, 420)
        self.Co2_button.clicked.connect(self.colorDialog)
        self.Co2_button.setMinimumSize(110, 70)
        self.Co2_button.setStyleSheet(Color_("orange"))

        self.S_button.move(0, 180)
        self.S_button.clicked.connect(self.sizeDialog)
        self.S_button.setMinimumSize(110, 70)
        self.S_button.setStyleSheet(Color_("orange"))

        StepAction = QAction(self)
        StepAction.setShortcut('Ctrl')
        StepAction.triggered.connect(self.process)
        self.addAction(StepAction)

        self.C_button.move(0, 260)
        self.C_button.clicked.connect(self.clean)
        self.C_button.setMinimumSize(110, 70)
        self.C_button.setStyleSheet(Color_("orange"))

        self.P_button.setStyleSheet(Color_("orange"))
        self.P_button.setMinimumSize(110, 70)
        self.E_button.setStyleSheet(Color_("orange"))
        self.E_button.setMinimumSize(110, 70)
        self.P_button.move(0, 20)
        self.E_button.move(0, 100)
        self.P_button.clicked.connect(self.process)
        self.E_button.clicked.connect(self.era)
        self.timer = QBasicTimer()
        self.is_continue = True
        # self.timer.start(100, self)
        # hbox = QHBoxLayout()
        # hbox.addStretch(1)
        # hbox.addWidget(self.tboard)
        # hbox.addWidget(self.P_button)
        #self.P_button.move(int(w_w/10), w_h)

        self.show()



    def process(self):
        self.is_continue = self.tboard.process()

    def sizeDialog(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Input new size, spllited by space')
        if ok:
            # global w, self.h
            self.w, self.h= map(int, text.split())
            self.tboard.hide()
            self.tboard = Board(self, self.w, self.h)
            clean()
            self.hide()
            self.__init__(self.w, self.h)

    def colorDialog(self):
        col = QColorDialog.getColor()
        key = 1
        if self.sender() == self.Co_button:
            key = 0
        if col.isValid():
            colors[key] = col.name()

        self.tboard.renew_colors(key)

    def clean(self):
        self.tboard.clean_colors()
        clean()

    def era(self):
        if self.timer.isActive():
            self.timer.stop()
            self.E_button.setText('Start')
        else:
            self.timer.start(100, self)
            self.E_button.setText('Stop')

    def timerEvent(self, e):
        if not self.is_continue:
              self.timer.stop()
              self.E_button.setText('Start')
              self.is_continue = True
              return
        #
        # self.step = self.step + 1
        self.process()



if __name__ == '__main__':
    app = QApplication([])
    life = LifeGame()
    sys.exit(app.exec_())