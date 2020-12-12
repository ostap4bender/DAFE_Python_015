import sys
import time
import threading
from  PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDesktopWidget, QInputDialog,  QAction, QApplication, QLabel


class Universe(QWidget):
    
    
    def __init__(self, rows = 40, cols = 40):
        super().__init__()
        
        self.cols = cols
        self.rows = rows
        self.cellsize = 15
        
        self.win_width = max(self.cellsize*self.cols + 200, 400)
        self.win_height = max(self.cellsize*self.rows, 500)
        
        
        #self.colors = ["purple", "darkred", "yellow", "orange", "darkorange", "rgb(51, 0, 102)", "lightblue", "red",
                       #"lightgreen", "green", "darkgreen", "blue", "white", "grey", "aquamarine", "beige"]

        self.colors = ["rgb(122, 137, 146)", "rgb(137, 163, 175)", "rgb(171, 185, 190)", "rgb(205, 203, 204)",
                       "rgb(193, 171, 162)", "rgb(233, 218, 215)", "rgb(248, 241, 229)", "rgb(220, 221, 224)",
                       "rgb(187, 197, 200)", "rgb(203, 227, 230)", "rgb(209, 139, 105)", "lightblue",
                       "white", "grey", "rgb(164, 137, 136)", "beige"]
        for i in range(len(self.colors)):
            self.colors[i] = 'QPushButton {background-color: ' + self.colors[i] + ';}'
        
        self.pal_size = 4
        self.palette_alive = []
        self.palette_dead = []
        
        self.pal_act = False
    
        self.alive_color = 'QPushButton {background-color: ' + 'green' + ';}'#color: green}' blue white
        self.dead_color = 'QPushButton {background-color: ' + 'darkblue' + ';}'#color: orange}' white black darkorange        
        
        self.life_time = 350 #mscnds
        self.run_timer = QTimer()
        self.run_timer.timeout.connect(self.next_stage)        
        
        self.field = []
        self.initUI()
        
        self.running = False        
        

    def initUI(self):

        btn_left_margine = self.cellsize*self.cols + 25
        rsz = QPushButton('STEP>', self);
        rsz.resize(150, 40)
        rsz.move(btn_left_margine, 10)
        rsz.clicked.connect(self.next_stage)
        
        self.runbtn = QPushButton('>>RUN>>', self);
        self.runbtn.resize(150, 40)
        self.runbtn.move(btn_left_margine, 10 + 50) 
        self.runbtn.clicked.connect(self.run)
        
        self.stopbtn = QPushButton('||STOP||', self);
        self.stopbtn.resize(150, 40)
        self.stopbtn.move(btn_left_margine, 10 + 50)
        self.stopbtn.clicked.connect(self.stop)
        self.stopbtn.hide()
        
        rsz = QPushButton('RESIZE', self);
        rsz.resize(150, 40)
        rsz.move(btn_left_margine, 10 + 100)
        rsz.clicked.connect(self.sizeDialog)
        
        rsz = QPushButton('SET COLOR', self);
        rsz.resize(150, 40)
        rsz.move(btn_left_margine, 10 + 150)
        rsz.clicked.connect(self.palette_menu)        
        
        
        
        self.field = [[0]*(self.cols + 2) for i in range(self.rows + 2)]
        for i in range(self.rows):
            for j in range(self.cols):
                btn = QPushButton('', self)
                btn.setStyleSheet(self.dead_color)
                btn.resize(self.cellsize, self.cellsize)
                btn.move(self.cellsize*j, self.cellsize*i) 
                btn.clicked.connect(self.field_click)
                self.field[i + 1][j + 1] = btn
        
        self.palette_alive = [[0]*self.pal_size for i in range(self.pal_size)]
        self.palette_dead = [[0]*self.pal_size for i in range(self.pal_size)]
        pal_cell_size = 20
        for i in range(self.pal_size):
            for j in range(self.pal_size):
                btn = QPushButton('', self)
                btn.setStyleSheet(self.colors[i * self.pal_size + j])
                btn.resize(pal_cell_size, pal_cell_size)
                btn.move(pal_cell_size*j + btn_left_margine, pal_cell_size*i + 250) 
                btn.clicked.connect(self.pal_alive_click)
                btn.hide()
                self.palette_alive[i][j] = btn
                
                
                btn = QPushButton('', self)
                btn.setStyleSheet(self.colors[i * self.pal_size + j])
                btn.resize(pal_cell_size, pal_cell_size)
                btn.move(pal_cell_size*j + btn_left_margine, pal_cell_size*i + 350) 
                btn.clicked.connect(self.pal_dead_click)
                btn.hide()
                self.palette_dead[i][j] = btn                     
                
        self.lbl_alive_pal = QLabel(self)
        self.lbl_alive_pal.setText("Alive")
        self.lbl_alive_pal.move(btn_left_margine + 100, 270)
        
        self.lbl_dead_pal = QLabel(self)
        self.lbl_dead_pal.setText("Dead")
        self.lbl_dead_pal.move(btn_left_margine + 100, 370)
        
        self.lbl_alive_pal.hide()
        self.lbl_dead_pal.hide()
                
        self.setGeometry(200, 200, btn_left_margine + 200, self.win_height)
        self.center()
        self.setWindowTitle('Universe')
        #self.setWindowIcon(QIcon('alive_icon.png'))

        self.show()
        
    def field_click(self):
        sender = self.sender()
        if sender.styleSheet() == self.dead_color:
            sender.setStyleSheet(self.alive_color)
        else:
            sender.setStyleSheet(self.dead_color)
            
    def pal_alive_click(self):
        sender = self.sender()
        new_color = sender.styleSheet()
        
        #redrawing
        for i in range(1,self.rows + 1):
            for j in range(1, self.cols + 1):
                if self.field[i][j].styleSheet() == self.alive_color:
                    self.field[i][j].setStyleSheet(new_color)
                    
                    
        self.alive_color = new_color
        #self.repaint()
        
            
    def pal_dead_click(self):
        sender = self.sender()
        new_color = sender.styleSheet()
        
        #redrawing
        for i in range(1,self.rows + 1):
            for j in range(1, self.cols + 1):
                if self.field[i][j].styleSheet() == self.dead_color:                
                    self.field[i][j].setStyleSheet(new_color)
                
        self.dead_color = new_color
        
        
    def next_stage(self):
        self.prev_field = [[0]*(self.cols + 2) for i in range(self.rows + 2)]
        for i in range(1,self.rows + 1):
            for j in range(1, self.cols + 1):
                if self.field[i][j].styleSheet() == self.alive_color:
                    self.prev_field[i][j] = 1

        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                if self.cell_next_state(i, j):
                    if self.prev_field[i][j] != 1:
                        self.field[i][j].setStyleSheet(self.alive_color)
                elif self.prev_field[i][j] != 0:
                    self.field[i][j].setStyleSheet(self.dead_color)
          
        
    
    def cell_next_state(self, idxi, idxj):
        cnt_alive = 0
        for i in range(idxi - 1, idxi + 2):
            for j in range(idxj - 1, idxj + 2):
                if j == idxj and i == idxi:
                    continue
                if self.prev_field[i][j] == 1:
                    cnt_alive += 1

        if self.prev_field[idxi][idxj] == 1:
            if cnt_alive == 3 or cnt_alive == 2:
                return True
            return False
        else:
            if cnt_alive == 3:
                return True
            return False  
        
        
    def run(self):
        self.runbtn.hide()
        self.stopbtn.show()
        self.running = True
        self.run_timer.start(self.life_time)      


    def stop(self):
        if self.running:
            self.running = False
            self.run_timer.stop()
            self.stopbtn.hide()
            self.runbtn.show()
        return
        
    
    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()
            
    def center(self):
    
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def sizeDialog(self):
    
        text, ok = QInputDialog.getText(self, 'Resize field', 'Enter number of rows and cols(splitting by space):')
        
        vals = text.split()
        if len(vals) != 2 or not ok: return
        strdigit = vals[0] + vals[1]
        for i in range(len(strdigit)):
            if not strdigit[i].isdigit():
                return
        rows, cols = int(vals[0]), int(vals[1]) 
        self.hide()
        self.__init__(rows, cols)
        
    def palette_menu(self):
        if not self.pal_act:
            for i in range(len(self.palette_alive)):
                for j in range(len(self.palette_alive)):
                    self.palette_alive[i][j].show()
                    
            for i in range(len(self.palette_dead)):
                for j in range(len(self.palette_dead)):
                    self.palette_dead[i][j].show()
                    
    
            self.lbl_alive_pal.show()
            self.lbl_dead_pal.show()            
            
            self.pal_act = True
        else:
            for i in range(len(self.palette_alive)):
                for j in range(len(self.palette_alive)):
                    self.palette_alive[i][j].hide()
                    
            for i in range(len(self.palette_dead)):
                for j in range(len(self.palette_dead)):
                    self.palette_dead[i][j].hide()
                
            
            self.lbl_alive_pal.hide()
            self.lbl_dead_pal.hide()
            self.pal_act = False            
            
            

        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    un = Universe()
    sys.exit(app.exec_())