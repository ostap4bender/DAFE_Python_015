import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# Game configuration
width = 100
height = 100
screenShrink = 1.2


class GameScene(QGraphicsScene):
    def __init__(self):
        QObject.__init__(self)
        
        # Default cell width
        self.cW = 4
        # Default cell height
        self.cH = 4

        # Create instance of GameField and QTimer objects
        self.gameField = GameField()
        self.timer = QTimer()

        # Connect timer ticking to a slot
        self.timer.timeout.connect(self.timerTick)

        # Create a two-dimensional width * height unit graphic item array corresponding
        # each cell
        self.cellIcons = [[QGraphicsRectItem()] * height for i in range(width)]

        # Set game background
        self.addRect(0, 0, width * self.cW, height * self.cH, QPen(Qt.gray), QBrush(Qt.white))
        

        # Fill all graphical data for each cell to the two-dimensional array
        for x in range(width):
            for y in range(height):
                icon = QGraphicsRectItem()
                icon.setRect(x * self.cW, y * self.cH, self.cW, self.cH)
                icon.setPen(QPen(Qt.black)) #change border color
                icon.setBrush(QBrush(QColor('aquamarine'))) #changle fill color 
                icon.setVisible(False)
                self.cellIcons[x][y] = icon
                self.addItem(self.cellIcons[x][y])

        print("Scene created")

    def isInBounds(self, x, y):
        return x > 0 and x < width - 1 and y > 0 and y < height - 1

    def mousePressEvent(self, event):
        # Mouse coordinates have to be divided with cell width and height in
        # order to get them correctly
        x = int(event.lastScenePos().x() / self.cW)
        y = int(event.lastScenePos().y() / self.cH)

        # Check if mouse coordinates are out of bounds
        if (not self.isInBounds(x, y)):
            return

        isAlive = self.gameField.isAliveAt(x, y)

        # Invert cell
        self.toggleCell(x, y, not isAlive)
        print(f"Cell X: {x}, Y: {y}")

    def mouseMoveEvent(self, event):
        # See event mousePressEvent. This event applies while mouse is moving

        x = int(event.lastScenePos().x() / self.cW)
        y = int(event.lastScenePos().y() / self.cH)

        if (not self.isInBounds(x, y)):
            return

        if (not self.gameField.isAliveAt(x, y)):
            self.toggleCell(x, y, True)
            print(f"Cell X: {x}, Y: {y}")

    def setVisible(self, x, y, visible):
        self.cellIcons[x][y].setVisible(visible)

    def toggleCell(self, x, y, alive):
        self.gameField.cells[x][y] = alive
        self.setVisible(x, y, alive)

    def timerTick(self):
        # This method is called each time the timer "ticks"

        # The game field call the setVisible function for each cell.
        # This reduces the amount of looping for the large array
        self.gameField.calculateCells(self.setVisible)

    def clearScene(self):
        # Set all cells dead
        for x in range(width):
            for y in range(height):
                self.toggleCell(x, y, False)

        print("Scene cleared")


class GameField:

    def __init__(self):
        self.cells = None
        self.reset()

        print("Field created")

    def reset(self):
        # Create two two-dimensional arrays for the cells
        self.cells = [[False] * height for i in range(width)]

    def isAliveAt(self, x, y):
        return self.cells[x][y]

    def calculateNeighbours(self, x, y):


        # Set the count of neighbours of each cell as zero at start
        neighbours = 0
        
        if (x - 1 < 0):
            x = width - 1
        if (y - 1 < 0):
            y = height - 1
        if (x + 1 == width):
            x = 0
        if (y + 1 == height):
            y = 0

        # Top row
        if (self.cells[x - 1][y + 1]):
            neighbours += 1
        if (self.cells[x][y + 1]):
            neighbours += 1
        if (self.cells[x + 1][y + 1]):
            neighbours += 1

        # Middle row
        if (self.cells[x - 1][y]):
            neighbours += 1
        if (self.cells[x + 1][y]):
            neighbours += 1

        # Bottom row
        if (self.cells[x - 1][y - 1]):
            neighbours += 1
        if (self.cells[x][y - 1]):
            neighbours += 1
        if (self.cells[x + 1][y - 1]):
            neighbours += 1

        return neighbours

    def calculateCells(self, callback):
        neighbours = 0

        newCells = [[False] * height for i in range(width)]

        for x in range(0, width):
            for y in range(0, height):
                # Rules from: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
                neighbours = self.calculateNeighbours(x, y)
    

                # 1. Any live cell with fewer than two live neighbours dies,
                # as if by underpopulation.
                if (neighbours < 2):
                    newCells[x][y] = False
                    callback(x, y, False)
                    continue

                # 2. Any live cell with two or three live neighbours lives on
                # to the next generation.
                if ((neighbours == 2 or neighbours == 3) and self.cells[x][y]):
                    newCells[x][y] = True
                    callback(x, y, True)
                    continue

                # 3. Any live cell with more than three live neighbours dies,
                # as if by overpopulation.
                if (neighbours > 3):
                    newCells[x][y] = False
                    callback(x, y, False)
                    continue

                # 4. Any dead cell with exactly three live neighbours becomes
                # a live cell, as if by reproduction.
                if (neighbours == 3):
                    newCells[x][y] = True
                    callback(x, y, True)
                    continue
                    

                callback(x, y, False)

        # Swap the buffer, i.e. the changed cells to the actual ones
        self.cells = newCells


class LifeWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Set the LifeWindow widget to the middle of the screen and resize it

        screen = QGuiApplication.primaryScreen();
        screenGeometry = screen.geometry();
        w = screenGeometry.width() / screenShrink
        h = screenGeometry.height() / screenShrink
        x = screenGeometry.width() / screenShrink - w / screenShrink
        y = screenGeometry.height() / screenShrink - h / screenShrink
        self.setGeometry(x, y, w, h)

        self.setWindowTitle("Game of Life")

        # Initialize GraphicsView which contains our custom scene
        self.graphicsView = QGraphicsView()
        self.gameScene = GameScene()
        self.graphicsView.setScene(self.gameScene)

        # Enable graphicsview antialiasing and disable scrollbars
        self.graphicsView.setRenderHints(QPainter.Antialiasing)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Create pushbuttons
        self.pushButtonStart = QPushButton("Start", self)
        self.pushButtonPause = QPushButton("Pause", self)
        self.pushButtonNew = QPushButton("Reset", self)
        self.pushButtonSetColor = QPushButton("Set color", self)
            
        self.pushButtonSetColor.clicked.connect(self.setNewColor)
        
        # Enable and disable the pushbuttons suitable for the situation
        self.pushButtonStart.setEnabled(True)
        self.pushButtonPause.setDisabled(True)
        self.pushButtonNew.setDisabled(True)

        # Connect pushbutton clicks to their slots
        self.pushButtonStart.clicked.connect(self.pushButtonStartClicked)
        self.pushButtonPause.clicked.connect(self.pushButtonPauseClicked)
        self.pushButtonNew.clicked.connect(self.pushButtonNewClicked)

        self.colorLabel = QLabel(self)
        self.colorLabel.setText('Set color:')
        self.line = QLineEdit(self)
        
        

        # Create a gridlaoyt for the pushbuttons and the graphicsview
        gridLayout = QGridLayout(self)
        gridLayout.addWidget(self.graphicsView, 0, 0, 1, 3, Qt.Alignment(0))
        gridLayout.addWidget(self.pushButtonStart, 1, 0)
        gridLayout.addWidget(self.pushButtonPause, 1, 1)
        gridLayout.addWidget(self.pushButtonNew, 1, 2)
        gridLayout.addWidget(self.colorLabel, 2, 0)
        gridLayout.addWidget(self.line, 2, 1)
        gridLayout.addWidget(self.pushButtonSetColor, 2, 2)
        
        print("Window created")


    def setNewColor(self):
        new_color = self.line.text()
    
        for x in range(width):
            for y in range(height):
                self.gameScene.cellIcons[x][y].setBrush(QBrush(QColor(new_color)))
                

    def resizeEvent(self, event):
        # Allways upon user resizing the window the aspect ratio is kept at 3:2
        self.graphicsView.fitInView(0, 0, 400, 400, Qt.KeepAspectRatio)

    def pushButtonStartClicked(self):
        # Start the graphicsscenes own timer and start the whole game and its
        # logic
        self.gameScene.timer.start(50)
        print("Timer started")

        self.pushButtonStart.setDisabled(True)
        self.pushButtonPause.setEnabled(True)
        self.pushButtonNew.setDisabled(True)

    def pushButtonPauseClicked(self):
        # Stop the graphicsscenes own timer to "pause" the game
        self.gameScene.timer.stop()
        print("Timer stopped")

        self.pushButtonStart.setEnabled(True)
        self.pushButtonPause.setDisabled(True)
        self.pushButtonNew.setEnabled(True)

    def pushButtonNewClicked(self):
        # Stop the timer and call the graphicsscenes method clearScene for a
        # new start
        self.gameScene.timer.stop()
        self.gameScene.clearScene()
        print("New scene created")

        self.pushButtonStart.setEnabled(True)
        self.pushButtonPause.setDisabled(True)
        self.pushButtonNew.setEnabled(True)

if __name__ == '__main__':
    application = QApplication(sys.argv)
    application_window = LifeWindow()
    application_window.show()
    application_window.resizeEvent(None)
    application.exec_()
    