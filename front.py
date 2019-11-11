from tkinter import *
from solver import SudokuSolver
import time
import threading as th

def fill_sudoku():

	def fill_sudoku_th():
		sudoku = [[] for _ in range(9)]

		for k in range(81):
			field = fields[k].get() 
			if field.isdigit() and (0 < int(field) <= 9):
				sudoku[k//9].append(int(field))
			elif not field:
				sudoku[k//9].append(0)
			else:
				lbl.config(text='Wrong format!',fg='red')
				time.sleep(1)
				lbl.config(text='Enter valid sudoku',fg='black')
				return

		solver = SudokuSolver(sudoku)
		solver.solve_sudoku()
		if not solver.sudoku_is_correct:
			lbl.config(text='Sudoku is incorrect!',fg='red')
			time.sleep(1)
			lbl.config(text='Enter valid sudoku',fg='black')

		solved_sudoku = solver.finished_sudoku
		try:
			for k in range(81):
				fields[k].delete(0,END)
				fields[k].insert(0,str(solved_sudoku[k//9][k%9]))
		except: pass

	thread1 = th.Thread(target=fill_sudoku_th)
	thread1.start()


def clear():
	for field in fields:
		field.delete(0,END)

def get_from_txt():

	def get_from_txt_th():
		for field in fields:
			field.delete(0,END)
		sudoku = []
		try:
			with open(filename_field.get()) as file:
				for line in file:
					a = [int(x) for x in line.rsplit()]
					sudoku.append(a)
		except:
			lbl.config(text='No such file here!',fg='red')
			time.sleep(1)
			lbl.config(text='Enter valid sudoku',fg='black')
			return
		for k in range(81):
			num = sudoku[k//9][k%9]
			if num != 0:
				fields[k].insert(0,str(num))

	thread2 = th.Thread(target=get_from_txt_th)
	thread2.start()



	


window = Tk()
window.geometry('395x670')
window.resizable(width=False,height=False)
window.title('SudokuSolver')
window.config(bg='#70d9ff')

fields = [Entry(window, width=2, font='Times 30', justify=CENTER) for k in range(81)]
for k in range(81):
	fields[k].grid(column=(k%9),row=(k//9))	

lbl = Label(window, text='Enter valid sudoku', font='Times 18',bg='#70d9ff')
lbl.grid(column=2, row=11, columnspan=5, pady=20)

solve_button = Button(window, text="Solve!", font='Times 18', width=8, command=fill_sudoku, bg='#abe9ff', activebackground='#86c4db')
solve_button.grid(column=1, row=12, columnspan=3, pady=10)

clear_button = Button(window, text="Clear", font='Times 18',width=8,command=clear, bg='#abe9ff', activebackground='#86c4db')
clear_button.grid(column=5, row=12, columnspan=3, pady=10)

get_button = Button(window,text="From .txt", font='Times 18',width=8,command=get_from_txt, bg='#abe9ff', activebackground='#86c4db')
get_button.grid(column=0, row=13, columnspan=5, pady=10)

filename_field = Entry(window,font='Times 16',width=12)
filename_field.grid(column=4 ,row=13, columnspan=5,padx=40)
filename_field.insert(0,'Enter filename')

window.mainloop()