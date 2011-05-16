import unittest
from sudoku.sudoku_solver import SudokuSolver

class SudokuSolverTests(unittest.TestCase):
	def setUp(self):
		self.solver = SudokuSolver()

	def test_empty_sudoku(self):
		board = [[-1] * 9 for x in xrange(9)]
		ok, res = self.solver.solve(board)
		self.assertTrue(ok)
		ok2, res2 = self.solver.solve(res)
		self.assertTrue(ok2)

suite = unittest.TestLoader().loadTestsFromTestCase(SudokuSolverTests)
unittest.TextTestRunner(verbosity = 2).run(suite)
