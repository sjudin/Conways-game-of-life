# Conways game of life
import threading
import functools
import tkinter
import pdb
import time
import numpy as np
from itertools import product

class Conways:
    def __init__(self, initial):
        assert type(initial) == np.ndarray
        self.grid = initial
        
    def update(self):
        new = np.copy(self.grid)
        for i,j in np.ndenumerate(self.grid):
            count = self.check_surrounding(i[0], i[1])

            # Cell being born
            if count == 3:
                new[i[0],i[1]] = 1
            # Isolation and throng
            elif count < 2 or count > 3:
               new[i[0],i[1]] = 0
        self.grid = new 


    def check_surrounding(self, row, col):
        # Count how many objects surround the current one
        self.grid[row,col]
        count = 0
        l = [[0, -1, 1],[0, -1, 1]]
        
        for r in product(l[0], l[1]):
            try:
                if self.grid[row + r[0], col + r[1]] and not (r[0] == 0 and r[1] == 0):
                    count += 1
            except IndexError:
                pass

        return count

class ConwayGui:
    def __init__(self):
        # Prompt user to input grid size
        print('What gridsize do you want?')
        rows = input('rows\n')
        columns = input('columns\n')
        self.visible_grid = np.empty((int(rows),int(columns)),dtype=object)
        self.conway = Conways(np.zeros((int(rows),int(columns))))

        self.top = tkinter.Tk()
        self.exit_flag = False
        for i in range(int(rows)):
            for j in range(int(columns)):
                a = Square(i, j, self.top, self.conway, width=20, heigh=20)
                self.visible_grid[i,j] = a
                a.grid(row=i, column=j)

        self.start_b = tkinter.Button(self.top, text='Go', command=self.start)
        self.start_b.grid()
        stop_b = tkinter.Button(self.top, text='Stop', command=self.stop).grid()
        self.top.protocol('WM_DELETE_WINDOW', self.stop)
        self.top.mainloop()

    def update_colors(self):
        for a in np.nditer(self.visible_grid, flags=['refs_ok']):
            a.item().update_square()

    def start(self):
        self.game_thread = threading.Thread(target=self.conway_thread).start()
        self.start_b.grid_forget()

    def conway_thread(self):
        while not self.exit_flag:
            self.conway.update()
            self.update_colors()
            time.sleep(0.3)

    def stop(self):
        print('stop')
        self.top.destroy()
        self.exit_flag = True


class Square(tkinter.Canvas):
    def __init__(self, i, j, top, conways, **kwargs):
        super().__init__(top, **kwargs)
        self.i = i
        self.j = j
        self.create_square()
        self.conways = conways

    def create_square(self):
        width = height = 20
        rcorner = (0, 0)
        lcorner = (width, height)

        self.bind('<Button-1>', self.set_square)
        self.rect = self.create_rectangle(rcorner, lcorner, activefill='red')

    def set_square(self, event=None):
        if self.conways.grid[self.i, self.j] == 0:
            self.conways.grid[self.i,self.j] = 1
            self.itemconfig(self.rect, fill='green')
        else:
            self.conways.grid[self.i,self.j] = 0
            self.itemconfig(self.rect, fill='')
    def update_square(self):
        if self.conways.grid[self.i, self.j] == 1:
            self.itemconfig(self.rect, fill='green')
        else:
            self.itemconfig(self.rect, fill='')

c = ConwayGui()
