from Tkinter import *
from sudoku_solver import SudokuSolver
import tkMessageBox

class SudokuGUI:
	def __init__(self, parent):
		self.ncells = 9
		self.margin = 10
		self.pixel_width = 500
		self.canvas = Canvas(parent, width = self.pixel_width + 2 * self.margin,							 height = self.pixel_width + 2 * self.margin)
		self.canvas.bind("<Button-1>", self.change_cell)
		self.canvas.pack()

		self.button_solve = Button(parent, text = "Solve it!")
		self.button_solve.configure(command = self.solve)
		self.button_solve.pack()

		self.button_save = Button(parent, text = "Print")
		self.button_save.configure(command = self.save)
		self.button_save.pack()
	
		self.board = [[-1]*self.ncells for x in xrange(self.ncells)]
		self.solver = SudokuSolver()

	def save(self):
		out = 'sudoku.ps'
		tkMessageBox.showinfo("Print", "Printed solution to file %s"%out)
		self.canvas.postscript(file = 'sudoku.ps', colormode = 'color')

	def get_value(self, x):
		if x == -1:
			return '  '
		return str(x)

	def solve(self):
		ok, ans = self.solver.solve(self.board)
		if not ok:
			tkMessageBox.showerror("FAIL", "Sudoku cannot be solved")
			return 
		self.canvas.delete('all')
		for i in xrange(self.ncells):
			for j in xrange(self.ncells):
				if self.board[i][j] != ans[i][j]:
					self.draw_cell(i, j, self.get_value(ans[i][j]),
									 color='blue')					
				else:
					self.draw_cell(i, j, self.get_value(self.board[i][j]),
									 color = 'black')
		print self.board

	def _get_next_value(self, snum):
		if snum == '  ':
			return '1'
		num = int(snum)
		num = (num + 1)%10
		if num == 0:
			return '  '
		else:
			return str(num)

	def update_text(self, e):
		value = self._get_next_value(self.canvas.itemcget(e, 'text'))
		self.canvas.itemconfigure(e, text = value)
		x, y = self.canvas.gettags(e)[1].split(' ')
		x, y = int(x), int(y)
		if value == '  ':
			self.board[x][y] = -1 
		else:
			self.board[x][y] = int(value)

	def change_cell(self, event):
		e = self.canvas.find_closest(event.x, event.y)
		if 'text' in self.canvas.gettags(e):
			self.update_text(e)
		else:
			if 'rectangle' in self.canvas.gettags(e):
				text_tag = self.canvas.gettags(e)[1]
				for x in self.canvas.find_withtag(text_tag):
					if 'text' in self.canvas.gettags(x):
						self.update_text(x)

	def draw_cell(self, i, j, value = '  ', color = 'black'):
		cellsize = self.pixel_width/self.ncells
		x1 = self.margin + i * cellsize
		y1 = self.margin + j * cellsize
		x2 = x1 + cellsize
		y2 = y1 + cellsize
		r_index = self.canvas.create_rectangle(x1, y1, x2, y2)
		t_index = self.canvas.create_text((x1 + x2)/2, (y1 + y2)/2, text=value,	font = ('Helvectica', 30), fill = color)

		self.canvas.addtag_withtag('rectangle', r_index)
		self.canvas.addtag_withtag('%d %d'%(i, j), r_index)

		self.canvas.addtag_withtag('text', t_index)
		self.canvas.addtag_withtag('%d %d'%(i, j), t_index)

		if i % 3 == 0 and i > 0:
			self.canvas.create_line(x1, y1, x1, y1 + cellsize , width = 3)
		if j % 3 == 0 and j > 0:
			self.canvas.create_line(x1, y1, x1 + cellsize , y1, width = 3)	
	
	def draw_board(self):
		for i in xrange(self.ncells):
			for j in xrange(self.ncells):
				if self.board[i][j] == -1:
					self.draw_cell(i, j)
				else:
					self.draw_cell(i, j, value = str(self.board[i][j]))

if __name__ == '__main__':
	root = Tk()
	root.title("Sudoku Solver")
	sudoku = SudokuGUI(root)
	sudoku.draw_board()
	root.mainloop()
