import sys
import time
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLineEdit, QSlider, QLabel, QCheckBox
from PyQt5.QtCore import QBasicTimer, Qt


TEXT_SIZE = 14
CELL_SIZE = 15
WIDTH = 40
HEIGHT = 40
MARGIN_TOP = 30
MARGIN_LEFT = 30
MARGIN_BUTTON = int(MARGIN_TOP/2)
BTN_SIDE_WIDTH = 250
BTN_SIDE_HEIGHT_base = 50
BTN_SIDE_HEIGHT = BTN_SIDE_HEIGHT_base
SIDE = 2*MARGIN_LEFT + BTN_SIDE_WIDTH

BTN_CONFIRM_COLOR_STYLE = "border-radius: 0.4em; background-color: #119215"
BTN_CONFIRM_SIZE_STYLE = "border-radius: 0.4em; background-color: #119215"
BTN_START_STYLE = "border-radius: 0.4em; background-color: #119215"
BTN_CLOSE_STYLE = "border-radius: 0.4em; background-color: #8b2309"
BTN_CLEAR_STYLE = "border-radius: 0.4em; background-color: #28d4e0"
BTN_GRID_STYLE = "border-radius: 0.4em; background-color: #979797"

WIN_STYLE = "background-color: #b4b4b4; border: 0; font-family: Arial; font-size: "+ str(TEXT_SIZE) +"px;" \
            "font-weight: 600; color: white;"

INPUT_STYLE = "background-color: white; border: 0; border-radius: 0.4em; color: black; font-size: 14px; font-weight: 600;"

NON_ACTIVE_STYLE_base = "background-color:"
ACTIVE_STYLE_base = "background-color:"

GRID_STYLE = ";border: 0.5px solid #eee"
NO_GRID_STYLE = ";border: 0px"

DEFAULT_COLOR_ACTIVE = "#438909"
DEFAULT_COLOR_NON_ACTIVE = "#ddd"

CURRENT_COLOR = DEFAULT_COLOR_ACTIVE

NON_ACTIVE_STYLE = NON_ACTIVE_STYLE_base +  DEFAULT_COLOR_NON_ACTIVE + GRID_STYLE
ACTIVE_STYLE = ACTIVE_STYLE_base + DEFAULT_COLOR_ACTIVE + GRID_STYLE


class GameOfLife(QMainWindow):

	def __init__(self):
		super().__init__()

		self.initUI()


	def initUI(self):

		self.setStyleSheet(WIN_STYLE)
		self.setFixedSize(WIDTH * CELL_SIZE + SIDE + MARGIN_LEFT, HEIGHT*CELL_SIZE + 2*MARGIN_TOP)
		
		self.generations_counter = 0
		self.main_counter = 0
		self.buttons = list()
		self.isGrid = True
		self.speed = 85
		self.is_circled = True
		
		self.timer =  QBasicTimer()
		
		self.speed_sld = QSlider(Qt.Horizontal, self)
		self.speed_sld.setFocusPolicy(Qt.NoFocus)
		self.speed_sld.valueChanged[int].connect(self.changeSpeed)
		self.speed_sld.setValue(50)

		self.label_speed = QLabel("Speed:", self)
		
		self.btn_start = QPushButton("START", self)
		self.btn_start.clicked.connect(self.start_simulate)
		self.btn_start.setStyleSheet(BTN_START_STYLE)
		
		self.btn_close = QPushButton("QUIT", self)
		self.btn_close.clicked.connect(self.exit)
		self.btn_close.setStyleSheet(BTN_CLOSE_STYLE)
		
		self.input_h = QLineEdit(self)
		self.input_w = QLineEdit(self)
		self.input_w.setStyleSheet(INPUT_STYLE)
		self.input_h.setStyleSheet(INPUT_STYLE)
		
		self.btn_confirm = QPushButton("OK", self)
		self.btn_confirm.clicked.connect(self.resize)
		self.btn_confirm.setStyleSheet(BTN_START_STYLE)

		self.label_size_h = QLabel("Height:", self)
		self.label_size_w = QLabel("Width:", self)
		
		self.btn_color_confirm = QPushButton("SET", self)
		self.btn_color_confirm.clicked.connect(self.color_confirm)
		self.btn_color_confirm.setStyleSheet(BTN_START_STYLE)

		self.input_color = QLineEdit(self)
		self.input_color.setStyleSheet(INPUT_STYLE)

		self.label_color = QLabel("Set color (CSS-style):", self)
		
		self.btn_clear = QPushButton("Clear", self)
		self.btn_clear.clicked.connect(self.clear_field)
		self.btn_clear.setStyleSheet(BTN_CLEAR_STYLE)
		
		self.btn_show_grid = QPushButton("Hide grid", self)
		self.btn_show_grid.clicked.connect(self.grid)
		self.btn_show_grid.setStyleSheet(BTN_GRID_STYLE)

		self.checkbox_circled = QCheckBox("FIELD: CIRCLED", self)
		self.checkbox_circled.toggle()
		self.checkbox_circled.stateChanged.connect(self.change_circled)
		
		self.replace_btns()

		for i in range(HEIGHT):
			'''заполнение посточно, слева направо'''
			self.buttons.append(list())

			for j in range(WIDTH):

				btn = QPushButton("", self)
				btn.setStyleSheet(NON_ACTIVE_STYLE)
				btn.clicked.connect(self.buttonClicked)
				btn.status = False
				btn.setGeometry(MARGIN_LEFT+j*CELL_SIZE, MARGIN_TOP + i*CELL_SIZE, CELL_SIZE, CELL_SIZE)

				self.buttons[i].append(btn)

		self.statusBar()
		
		self.setGeometry(300, 300, WIDTH * CELL_SIZE + SIDE + MARGIN_LEFT, HEIGHT*CELL_SIZE + 2*MARGIN_TOP)
		self.setWindowTitle('Game Of Life')
		self.show()

	def exit(self):
		self.hide()

	def change_circled(self):
		if self.is_circled:
			self.checkbox_circled.setText("FIELD : UNCIRCLED")
		else:
			self.checkbox_circled.setText("FIELD : CIRCLED")
		self.is_circled = not self.is_circled

	def replace_btns(self):
		x0 = MARGIN_LEFT*2 + WIDTH * CELL_SIZE

		self.btn_start.setGeometry(x0, MARGIN_TOP, BTN_SIDE_WIDTH, BTN_SIDE_HEIGHT)
		self.label_size_h.setGeometry(x0,
									MARGIN_TOP + BTN_SIDE_HEIGHT + int((MARGIN_TOP - TEXT_SIZE)/2),   
									int((BTN_SIDE_WIDTH - 2*MARGIN_BUTTON)/3),
									TEXT_SIZE)
		self.label_size_w.setGeometry(x0 + int((BTN_SIDE_WIDTH + MARGIN_BUTTON)/3),
									MARGIN_TOP + BTN_SIDE_HEIGHT + int((MARGIN_TOP - TEXT_SIZE)/2), 
									int((BTN_SIDE_WIDTH - 2*MARGIN_BUTTON)/3), 
									TEXT_SIZE)

		self.input_h.setGeometry(x0,
									MARGIN_TOP + MARGIN_TOP + BTN_SIDE_HEIGHT,  
									int((BTN_SIDE_WIDTH - 2*MARGIN_BUTTON)/3),
									BTN_SIDE_HEIGHT)
		self.input_w.setGeometry(x0 + int((BTN_SIDE_WIDTH + MARGIN_BUTTON)/3),
									MARGIN_TOP + MARGIN_TOP + BTN_SIDE_HEIGHT,  
									int((BTN_SIDE_WIDTH - 2*MARGIN_BUTTON)/3), 
									BTN_SIDE_HEIGHT)
		self.btn_confirm.setGeometry(x0 + 2*int((BTN_SIDE_WIDTH + MARGIN_BUTTON)/3),
										MARGIN_TOP + MARGIN_TOP + BTN_SIDE_HEIGHT,  
										int((BTN_SIDE_WIDTH - 2*MARGIN_BUTTON)/3), 
										BTN_SIDE_HEIGHT)
		self.label_color.setGeometry(x0,
										MARGIN_TOP + 2*BTN_SIDE_HEIGHT + MARGIN_TOP + int((MARGIN_TOP - TEXT_SIZE)/2),
										BTN_SIDE_WIDTH,
										TEXT_SIZE)

		self.input_color.setGeometry(MARGIN_LEFT*2 + WIDTH * CELL_SIZE, 
										MARGIN_TOP + 2*MARGIN_TOP + 2*BTN_SIDE_HEIGHT,  
										int((BTN_SIDE_WIDTH - MARGIN_BUTTON)/3 *2),
										BTN_SIDE_HEIGHT)
		self.btn_color_confirm.setGeometry(MARGIN_LEFT*2 + WIDTH * CELL_SIZE + 2*int((BTN_SIDE_WIDTH + MARGIN_BUTTON)/3),
											MARGIN_TOP + 2*MARGIN_TOP + 2*BTN_SIDE_HEIGHT,  
											int((BTN_SIDE_WIDTH - 2*MARGIN_BUTTON)/3), 
											BTN_SIDE_HEIGHT)

		self.label_speed.setGeometry(x0,
										MARGIN_TOP + 3*BTN_SIDE_HEIGHT + 2*MARGIN_TOP + int((MARGIN_TOP - TEXT_SIZE)/2),
										BTN_SIDE_WIDTH,
										TEXT_SIZE)

		self.speed_sld.setGeometry(MARGIN_LEFT*2 + WIDTH * CELL_SIZE, 
								MARGIN_TOP + 3*MARGIN_TOP + 3*BTN_SIDE_HEIGHT,  
								BTN_SIDE_WIDTH,
								BTN_SIDE_HEIGHT)

		self.checkbox_circled.setGeometry(x0,
											MARGIN_TOP + 3*MARGIN_TOP + 4*BTN_SIDE_HEIGHT + MARGIN_BUTTON,   
											BTN_SIDE_WIDTH,
											MARGIN_TOP)
		self.btn_show_grid.setGeometry(MARGIN_LEFT*2 + WIDTH * CELL_SIZE, 
										HEIGHT*CELL_SIZE - MARGIN_BUTTON - 2*BTN_SIDE_HEIGHT + MARGIN_TOP, 
										int((BTN_SIDE_WIDTH - MARGIN_BUTTON)/2), 
										BTN_SIDE_HEIGHT)
		self.btn_clear.setGeometry(MARGIN_LEFT*2 + WIDTH * CELL_SIZE + int((BTN_SIDE_WIDTH + MARGIN_BUTTON)/2), 
									HEIGHT*CELL_SIZE - MARGIN_BUTTON - 2*BTN_SIDE_HEIGHT + MARGIN_TOP, 
									int((BTN_SIDE_WIDTH - MARGIN_BUTTON)/2), 
									BTN_SIDE_HEIGHT)
		self.btn_close.setGeometry(MARGIN_LEFT*2 + WIDTH * CELL_SIZE, 
									HEIGHT*CELL_SIZE - BTN_SIDE_HEIGHT + MARGIN_TOP, 
									BTN_SIDE_WIDTH, BTN_SIDE_HEIGHT)


	def changeSpeed(self, val):
		if val > 60:
			self.speed = int(-7/4*val + 177)
		else:
			self.speed = int(1065/val**0.5 - 65)
		if self.timer.isActive():
			self.timer.start(self.speed, self)

	def clear_field(self):
		for i in range(HEIGHT):
			for j in range(WIDTH):
				self.buttons[i][j].status = False
				self.buttons[i][j].setStyleSheet(NON_ACTIVE_STYLE)
		self.main_counter = 0

	def timerEvent(self, e):
		self.simulate()
		if  self.main_counter <= 0:
			self.timer.stop()

	def grid(self):
		global ACTIVE_STYLE
		global NON_ACTIVE_STYLE
		if self.btn_show_grid.text() == "Hide grid":
			ACTIVE_STYLE = ACTIVE_STYLE_base + CURRENT_COLOR + NO_GRID_STYLE
			NON_ACTIVE_STYLE = NON_ACTIVE_STYLE_base + DEFAULT_COLOR_NON_ACTIVE + NO_GRID_STYLE

			self.isGrid = False;

			self.btn_show_grid.setText("Show grid")
			for i in range(HEIGHT):
				for j in range(WIDTH):
 					if self.buttons[i][j].status:
						self.buttons[i][j].setStyleSheet(ACTIVE_STYLE)
					else:
						self.buttons[i][j].setStyleSheet(NON_ACTIVE_STYLE)
		else:

			self.isGrid = True;

			ACTIVE_STYLE = ACTIVE_STYLE_base + CURRENT_COLOR + GRID_STYLE
			NON_ACTIVE_STYLE = NON_ACTIVE_STYLE_base + DEFAULT_COLOR_NON_ACTIVE + GRID_STYLE
			self.btn_show_grid.setText("Hide grid")
			for i in range(HEIGHT):
				for j in range(WIDTH):
 					if self.buttons[i][j].status:
						self.buttons[i][j].setStyleSheet(ACTIVE_STYLE)
					else:
						self.buttons[i][j].setStyleSheet(NON_ACTIVE_STYLE)


	def color_confirm(self):
		st = str(self.input_color.text())
		global CURRENT_COLOR
		global ACTIVE_STYLE
		if st == "":
			CURRENT_COLOR = DEFAULT_COLOR_ACTIVE
			if self.isGrid:
				ACTIVE_STYLE = ACTIVE_STYLE_base + DEFAULT_COLOR_ACTIVE + GRID_STYLE
			else:
				ACTIVE_STYLE = ACTIVE_STYLE_base + DEFAULT_COLOR_ACTIVE + NO_GRID_STYLE
		else:
			CURRENT_COLOR = str(st)
			if self.isGrid:
				ACTIVE_STYLE = ACTIVE_STYLE_base + CURRENT_COLOR + GRID_STYLE
			else:
				ACTIVE_STYLE = ACTIVE_STYLE_base + CURRENT_COLOR + NO_GRID_STYLE
		for i in range(len(self.buttons)):
			for j in range(len(self.buttons[i])):
				if self.buttons[i][j].status == True:
					self.buttons[i][j].setStyleSheet(ACTIVE_STYLE)


	def resize(self):
		'''TODO: 5 buttons'''
		self.main_counter = 0
		self.generations_counter = 0
		global BTN_SIDE_HEIGHT

		new_h = int(self.input_h.text())
		new_w = int(self.input_w.text())
		if new_h*CELL_SIZE < (6*BTN_SIDE_HEIGHT + 4*MARGIN_TOP + 3*MARGIN_BUTTON):
			self.input_h.setText("Too few!")
			return
		for i in range(len(self.buttons)):
			for j in range(len(self.buttons[i])):
				self.buttons[i][j].deleteLater()
		global HEIGHT
		HEIGHT = new_h
		global WIDTH
		WIDTH = new_w
		self.buttons.clear()
		for i in range(new_h):
			self.buttons.append(list())
			for j in range(new_w):
				temp = QPushButton("", self)
				temp.setStyleSheet(NON_ACTIVE_STYLE)
				temp.clicked.connect(self.buttonClicked)
				temp.status = False
				temp.setGeometry(MARGIN_LEFT+j*CELL_SIZE, MARGIN_TOP + i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
				temp.show()

				self.buttons[i].append(temp)
		
		BTN_SIDE_HEIGHT = BTN_SIDE_HEIGHT_base
		if HEIGHT*CELL_SIZE < (6*BTN_SIDE_HEIGHT + 5*MARGIN_BUTTON):
			BTN_SIDE_HEIGHT = int((HEIGHT*CELL_SIZE - 5*MARGIN_BUTTON)/6)
		self.setGeometry(300, 300, WIDTH * CELL_SIZE + SIDE + MARGIN_LEFT, HEIGHT*CELL_SIZE + 2*MARGIN_TOP)

		self.replace_btns()
		self.setFixedSize(WIDTH * CELL_SIZE + SIDE + MARGIN_LEFT, HEIGHT*CELL_SIZE + 2*MARGIN_TOP)


	def buttonClicked(self):

		sender = self.sender()
		if sender.status == False:
			sender.status = True
			sender.setStyleSheet(ACTIVE_STYLE)
			self.main_counter += 1
		else:
			sender.status = False
			sender.setStyleSheet(NON_ACTIVE_STYLE)
			self.main_counter -= 1


	def start_simulate(self):
		self.generations_counter = 0
		self.isAnythingChanged = False
		if self.timer.isActive():
			self.timer.stop()
			self.btn_start.setText('STAPT')
		else:
			self.timer.start(self.speed, self)
			self.btn_start.setText('STOP')

	def simulate(self):
		self.isAnythingChanged = False

		cur_gen = list()
		for i in range(HEIGHT):
			cur_gen.append(list())
			for j in range(WIDTH):
				cur_gen[i].append(self.count(i, j))

		for i in range(HEIGHT):
			for j in range(WIDTH):
				if cur_gen[i][j] == 3 and not self.buttons[i][j].status:
					self.buttons[i][j].status = True
					self.buttons[i][j].setStyleSheet(ACTIVE_STYLE)
					self.main_counter += 1
					self.isAnythingChanged = True
				elif cur_gen[i][j] not in (2, 3) and self.buttons[i][j].status:
					self.buttons[i][j].status = False
					self.buttons[i][j].setStyleSheet(NON_ACTIVE_STYLE)
					self.main_counter -= 1
					self.isAnythingChanged = True
				self.buttons[i][j].show()

		self.generations_counter += 1
		self.statusBar().showMessage("   GENERATIONS : {}".format(self.generations_counter))

		if self.main_counter <= 0 or not self.isAnythingChanged:
			self.btn_start.setText("START")
			self.timer.stop()


	def count(self, i, j):
		if self.is_circled:
			count = 0
			if i == 0:
				next_i = 1
				prev_i = HEIGHT-1;
			elif i == HEIGHT - 1:
				prev_i = HEIGHT - 2;
				next_i = 0;
			else:
				prev_i = i-1
				next_i = i+1

			if j == 0:
				next_j = 1
				prev_j = WIDTH - 1
			elif j == WIDTH - 1:
				prev_j = WIDTH - 2;
				next_j = 0
			else:
				next_j = j+1
				prev_j = j-1
			if self.buttons[prev_i][prev_j].status:
				count += 1
			if self.buttons[prev_i][j].status:
				count += 1
			if self.buttons[prev_i][next_j].status:
				count += 1
			if self.buttons[i][prev_j].status:
				count += 1
			if self.buttons[i][next_j].status:
				count += 1
			if self.buttons[next_i][prev_j].status:
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
				if j < WIDTH - 1:
					if self.buttons[i - 1][j + 1].status:
						count += 1
				if self.buttons[i - 1][j].status:
					count += 1
			if i < HEIGHT - 1:
				if j > 0:
					if self.buttons[i + 1][j - 1].status:
						count += 1
				if j < WIDTH - 1:
					if self.buttons[i + 1][j + 1].status:
						count += 1
				if self.buttons[i + 1][j].status:
					count += 1
			if j > 0:
				if self.buttons[i][j - 1].status:
					count += 1
			if j < WIDTH - 1:
				if self.buttons[i][j + 1].status:
					count += 1
			return count


if __name__ == '__main__':

	app = QApplication(sys.argv)
	ex = GameOfLife()
	sys.exit(app.exec_())
