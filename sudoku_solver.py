import random

class SudokuSolver:
	def __init__(self):
		pass

	def is_valid(self, i, j, x):
		if self.col[j][x - 1]:
			return False
		
		if self.row[i][x - 1]:
			return False

		qx = (i/3) * 3 + j/3
		if self.quad[qx][x - 1]:
			return False
		return True

	def update(self, i, j, x):
		self.col[j][x - 1] = 1
		self.row[i][x - 1] = 1
		qx = (i/3) * 3 + j/3
		self.quad[qx][x - 1] = 1
		self.res[i][j] = x

	def delete(self, i, j, x):
		self.col[j][x - 1] = 0
		self.row[i][x - 1] = 0
		qx = (i/3) * 3 + j/3
		self.quad[qx][x - 1] = 0
		self.res[i][j] = 0

	def get_next(self, i, j):
		i = i + 1
		if i == self.n:	
			i = 0
			j = j + 1
		return (i, j)

	def _solve(self, i, j):
		if j == self.n:
			return True

		next_i, next_j = self.get_next(i, j)

		if self.res[i][j]:
			return self._solve(next_i, next_j)

		for x in xrange(1, self.n + 1):
			if self.is_valid(i, j, x):
				self.update(i, j, x)
				if self._solve(next_i, next_j):
					return True
				self.delete(i, j, x)
		return False

	def solve(self, board):
		self.n = len(board)
		self.res = [[0] * self.n for x in xrange(self.n)]
		self.col = [[0] * self.n for x in xrange(self.n)]
		self.row = [[0] * self.n for x in xrange(self.n)]
		self.quad = [[0] * self.n for x in xrange(self.n)]
		
		for i in xrange(self.n):
			for j in xrange(self.n):
				if board[i][j] != -1:
					x = board[i][j]	
					if not self.is_valid(i, j, x):
						return (False, [])
					self.update(i, j, x)
		can = self._solve(0, 0)
		if not can: 
			return (False, [])
		return (True, self.res)
