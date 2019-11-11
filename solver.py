from copy import deepcopy
from random import randint
from time import time


class SudokuSolver:
	class EntryError(Exception):
		pass

	def __init__(self, sudoku):
		self.init_sudoku = sudoku
		self.sudoku_complete = False
		self.finished_sudoku = None
		self.sudoku_is_correct = True
		self.pool = {k + 1 for k in range(9)}

	def __repr__(self):
		sud = self.finished_sudoku
		if sud:
			for l in range(9):
				sud[l] = list(map(lambda x: str(x), sud[l]))
			string = ''
			for k in range(9):
				string += ' '.join(sud[k][:3]) + '   ' + ' '.join(
					sud[k][3:6]) + '   ' + ' '.join(sud[k][6:9]) + '\n'
				if (k + 1) % 3 == 0:
					string += '\n'
			return string
		else:
			return 'No finished sudoku'

	def solve_sudoku(self):
		'''
		starts main func
		'''
		if self.precheck_sudoku(self.init_sudoku):
			try:
				self.timer = time()
				self._solve_sudoku(self.init_sudoku)
			except SudokuSolver.EntryError:
				pass
		else:
			self.sudoku_is_correct = False
			#print('Sudoku incorrect!')

	def _solve_sudoku(self, sudoku, delay=3):
		'''
		recursive function that solves sudoku
		'''
		if not self.sudoku_complete and not (self.timer + delay) < time():
			self._do_trivial_cycles(sudoku)
			if self.check_correctness_of_finished_sudoku(sudoku):
				self.sudoku_complete = True
				self.finished_sudoku = sudoku
			possible_nums = self._find_the_best_possible_nums(sudoku)
			row = possible_nums[1]
			col = possible_nums[2]
			for num in possible_nums[0]:
				updated_sudoku = deepcopy(sudoku)
				updated_sudoku[row][col] = num
				self._solve_sudoku(updated_sudoku)

	def _find_the_best_possible_nums(self, sudoku):
		max_len = 0
		for row in range(9):
			for col in range(9):
				field = sudoku[row][col]
				if not field:
					entries = set().union(*self._get_all_filled_nums(sudoku, row, col))
					if len(entries) > max_len:
						max_len = len(entries)
						res_row = row
						res_col = col
						res_entries = entries
		try:
			return (self.pool.difference(res_entries), res_row, res_col)
		except:
			raise SudokuSolver.EntryError

	def _do_trivial_cycles(self, sudoku):
		'''
		While we can insert possible nums we do it
		'''
		while True:
			changed = self._insert_all_possible_nums(sudoku)
			if not changed:
				return sudoku

	def _insert_all_possible_nums(self, sudoku):
		'''
		Inserts num if its defined by 8 other
		'''
		changed = False
		for row in range(9):
			for col in range(9):
				field = sudoku[row][col]
				if not field:
					entries = set().union(*self._get_all_filled_nums(sudoku, row, col))
					if len(entries) == 8:
						for num in range(9):
							if not num + 1 in entries:
								sudoku[row][col] = num + 1
								changed = True
								continue
		return changed

	def _get_all_filled_nums(self, sudoku, row, col):
		'''
		Returns a tuple of row,column and square dicts
		'''
		square_position = (row // 3, col // 3)
		entries_row = set()
		entries_col = set()
		entries_square = set()
		for field in range(9):
			entry_row = sudoku[field][col]
			entry_col = sudoku[row][field]
			entry_square = sudoku[(3 * square_position[0]) +
																									field // 3][(3 * square_position[1]) + field % 3]
			if entry_row:
				entries_row.add(entry_row)
			if entry_col:
				entries_col.add(entry_col)
			if entry_square:
				entries_square.add(entry_square)
		return (entries_row, entries_col, entries_square)

	def _check_correctness_of_field(self, sudoku, row, col):
		'''
		Checks correctnes of field and return True if it is correct
		'''
		dicts = self._get_all_filled_nums(sudoku, row, col)
		if self.pool == dicts[0] == dicts[1] == dicts[2]:
			return True
		else:
			return False

	def check_correctness_of_finished_sudoku(self, sudoku):
		'''
		Checks all sudoku
		'''
		for row in range(9):
			for col in range(9):
				if not self._check_correctness_of_field(sudoku, row, col):
					return False
		return True

	def precheck_sudoku(self, sudoku):
		for i in range(9):
			row_set = set()
			col_set = set()
			square_set = set()
			for t in range(9):
				row_num = sudoku[t][i]
				col_num = sudoku[i][t]
				sqrow = ((3 * t) // 9) + 3 * (i // 3)
				sqcol = 3 * ((9 * i) // 9) % 9 + (t % 3)
				sq_num = sudoku[sqrow][sqcol]
				if not (row_num in row_set):
					if row_num != 0: row_set.add(row_num)
				else: return False
				if not (col_num in col_set):
					if col_num != 0: col_set.add(col_num)
				else: return False
				if not (sq_num in square_set):
					if sq_num != 0: square_set.add(sq_num)
				else: return False
		return True

	def test_sud(begin, end, rep):
		suds = []
		for num_of_nums in range(begin, end):
			for re in range(rep):
				nums = []
				sud = [[0 for x in range(9)] for k in range(9)]
				pool = set()
				for k in range(num_of_nums):
					nums.append(randint(1, 9))
					while True:
						index = randint(0, 80)
						if not index in pool:
							pool.add(index)
							break
				for num in nums:
					ind = pool.pop()
					sud[ind // 9][ind % 9] = num
				suds.append(sud)
		return suds


if __name__ == '__main__':

	sudoku = []
	with open('sud.txt') as file:
		for line in file:
			a = [int(x) for x in line.rsplit()]
			sudoku.append(a)

	solver = SudokuSolver(sudoku)
	solver.solve_sudoku()
	print(solver)
