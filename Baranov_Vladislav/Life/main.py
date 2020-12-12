import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget
from Life import *
import random

class NewMatrix:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.Matrix = []
        self.create_Matrix()

    def create_Matrix(self):
        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append(0)
            self.Matrix.append(line)


class Life(QtWidgets.QMainWindow):
    def __init__(self):
        super(Life, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.timer = QBasicTimer()
        self.mousePosX = 0
        self.mousePosY = 0
        self.width = 10
        self.height = 10
        self.RGB = [0, 200, 0]

        self.Matrix = None
        self.upgrade_Matrix()

        self.init_UI()

    def init_UI(self):

        self.ui.pushButton_Accept.clicked.connect(self.change_parameters)
        self.ui.pushButton_Start.clicked.connect(self.start)
        self.ui.pushButton_Stop.clicked.connect(self.stop)
        self.ui.pushButton_ChangeColor.clicked.connect(self.change_color)

    def change_color(self):
        line = self.ui.lineEdit_Color.text()
        i = 0
        while(i < len(line)):
            if line[i] == ',':
                line = line[0: i] + ' ' + line[i + 1:]

            elif line[i] == '(' or line[i] == ')':
                line = line[0: i] + line[i + 1:]
                i -= 1
            i += 1

        new_RGB = list(map(int, line.split()))
        if len(new_RGB) == 3 and 0 <= new_RGB[0] <= 255 and 0 <= new_RGB[1] <= 255 and 0 <= new_RGB[2] <= 255:
            self.RGB = new_RGB

    def start(self):
        self.timer.start(100, self)

    def stop(self):
        self.timer.stop()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        self.draw_field(qp)

        qp.end()

    def timerEvent(self, event):
        if self.timer.timerId() == event.timerId():
            self.calculate()
            self.update()

    def calculate(self):
        new_matrix = NewMatrix(self.width, self.height)

        for i in range(self.height):
            for j in range(self.width):
                new_matrix.Matrix[i][j] = self.round(i, j)
        self.data_transfer(new_matrix)


    def data_transfer(self, new_matrix):
        for i in range(self.height):
            for j in range(self.width):
                self.Matrix.Matrix[i][j] = new_matrix.Matrix[i][j]

    def round(self, y, x):
        cell_status = self.Matrix.Matrix[y][x]
        lx = x - 1
        hx = x + 2
        ly = y - 1
        hy = y + 2
        if x - 1 < 0:
            lx = 0
        elif x + 2 > self.width:
            hx = self.width

        if y - 1 < 0:
            ly = 0
        elif y + 2 > self.height:
            hy = self.height

        count = 0
        for i in range(ly, hy):
            for j in range(lx, hx):
                if self.Matrix.Matrix[i][j] == 1:
                    count += 1
        if cell_status == 1:
            count -= 1
            if count == 2 or count == 3:
                return 1
            else:
                return 0
        else:
            if count == 3:
                return 1
            else:
                return 0



    def upgrade_Matrix(self):
        self.Matrix = NewMatrix(self.width, self.height)

    def mousePressEvent(self, event):
        mousePosX = event.pos().x()
        mousePosY = event.pos().y()
        self.change_cell(mousePosX, mousePosY)
        self.update()

    def change_cell(self, mousePosX, mousePosY):
        x_max = 1700
        y_max = 950
        cell = []

        step = self.get_step()

        for i in range(self.height + 1):
            if mousePosX <= step * i:
                cell.append(i-1)
                break

        for i in range(self.width + 1):
            if mousePosY <= step * i:
                cell.append(i-1)
                break

        if len(cell) > 1:
            if self.Matrix.Matrix[cell[1]][cell[0]] == 1:
                self.Matrix.Matrix[cell[1]][cell[0]] = 0
            else:
                self.Matrix.Matrix[cell[1]][cell[0]] = 1

    def change_parameters(self):
        self.stop()
        w = self.ui.lineEdit_Width.text()
        h = self.ui.lineEdit_Height.text()

        if len(w) > 0 and len(h) > 0 and w.isdigit() and h.isdigit():
            self.width = int(w)
            self.height = int(h)

            self.upgrade_Matrix()

            self.update()



    def get_step(self):
        x_max = 1700
        y_max = 950

        stepX = int(x_max / self.width)
        stepY = int(y_max / self.height)

        if stepX > stepY:
            step = stepY
        else:
            step = stepX

        return step

    def draw_field(self, qp):
        x_max = 1700
        y_max = 950
        qp.setBrush(QColor(0, 0, 0, 210))
        qp.drawRect(0, 0, x_max, y_max)

        qp.setPen(QPen(QColor(255, 255, 255, 255), 0.15, Qt.SolidLine))

        step = self.get_step()

        for i in range(self.height):
            for j in range(self.width):
                if self.Matrix.Matrix[i][j] == 0:
                    qp.setBrush(QColor(0, 0, 0, 210))
                else:
                    qp.setBrush(QColor(self.RGB[0], self.RGB[1], self.RGB[2]))
                qp.drawRect(j * step, i * step, step, step)


app = QtWidgets.QApplication([])
application = Life()
application.show()

sys.exit(app.exec())