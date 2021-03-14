import tkinter as tk
import numpy as np
from tkinter import messagebox


class Application(tk.Frame):
    def __init__(self, master=None, title = 'App', geometry = '500x500', size = 4, **kwargs):
        super().__init__(master, **kwargs)

        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.master.title(title)
        self.master.geometry(geometry)

        self.grid(sticky="NEWS")
        self.configure(background='royal blue')

        self.size = tk.IntVar(value=size)
        self.size.trace_add('write', self.deleteWidgets)

        self.init_end_pos()
        self.void_col = self.size.get() - 1
        self.void_row = self.size.get()

        self.arr_size = (3, 4, 5)

        self.buttons_design = dict(activebackground = 'navy',\
                activeforeground= 'gold', bd = 4, bg = 'blue',\
                fg = 'yellow', font = ("Comic Sans MS", 20, "bold"))

        self.createWidgets()


    def init_end_pos(self):
        self.the_end = []
        for i in range(1, self.size.get() + 1):
            for j in range(0, self.size.get()):
                self.the_end.append([i,j])
        self.the_end.pop()


    def deleteWidgets(self, *args):
        self.grid_remove()
        self.__init__(title = '15 puzzle', geometry = '500x500', size = self.size.get())


    def createWidgets(self, *kwargs):
        for i in range(1, self.size.get()):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(self.size.get(), weight=1)

        self.new = tk.Button(self, text='New', command=self.random_gen, **self.buttons_design)
        self.quit = tk.Button(self, text='Quit', command=self.master.quit, **self.buttons_design)
        self.sizeButton = tk.Menubutton (self, text = 'Size', **self.buttons_design)
        self.sizeButton.menu = tk.Menu(self.sizeButton, tearoff = False, **self.buttons_design)
        self.sizeButton["menu"] =  self.sizeButton.menu

        for size in self.arr_size:
            self.sizeButton.menu.add_radiobutton(
                label=size,
                value=size,
                variable=self.size)

        self.buttons = np.empty(self.size.get() ** 2 - 1, dtype = tk.Button)
        for i in range(self.size.get() ** 2 - 1):
            self.buttons[i] = tk.Button(self, text = str(i + 1),\
                    command=lambda i=i: self.change_location(i), width=10, **self.buttons_design)

        self.random_gen()

        self.new.grid(row=0, column=0, sticky="NS")
        self.sizeButton.grid(row=0, column= (self.size.get() - 1) // 2,\
                columnspan = (self.size.get() + 1) % 2 + 1, sticky= "NS")
        self.quit.grid(row=0, column=self.size.get() - 1, sticky="NS")


    def show_buttons(self, gen):
        self.void_col = self.size.get() - 1
        self.void_row = self.size.get()

        self.create_solvable_gen(gen)

        row_ = 1
        col_ = 0
        for i in gen:
            self.buttons[i].grid(row = row_, column = col_, sticky = "NEWS")
            col_ += 1
            if col_ == self.size.get():
                col_ = 0
                row_ += 1


    def create_solvable_gen(self, gen):
        summ = 0
        for i in range(self.size.get() ** 2 - 1):
            for j in range(i + 1, self.size.get() ** 2 - 1):
                if gen[i] > gen[j]:
                    summ += 1
        if summ % 2:
            gen[self.size.get() ** 2 - 1 - 1], gen[self.size.get() ** 2 - 1 - 2] =\
                    gen[self.size.get() ** 2 - 1 - 2], gen[self.size.get() ** 2 - 1 - 1]


    def change_location(self, i):
        row = self.buttons[i].grid_info()['row']
        col = self.buttons[i].grid_info()['column']
        if col == self.void_col and abs(row - self.void_row) == 1 or\
                row == self.void_row and abs(col - self.void_col) == 1:
            self.buttons[i].grid(row = self.void_row, column = self.void_col)
            self.void_col = col
            self.void_row = row
            if self.check_win():
                tk.messagebox.showinfo("Victory", "You Win!")
                self.new.invoke()


    def random_gen(self):
        gen = np.random.permutation(range(self.size.get() ** 2 - 1))
        self.show_buttons(gen)


    def check_win(self):
        position = []
        for i in range(self.size.get() ** 2 - 1):
            row = self.buttons[i].grid_info()['row']
            col = self.buttons[i].grid_info()['column']
            position.append([row,col])
        if self.the_end == position:
            return True
        return False


def main():
    app = Application(title = '15 puzzle', geometry = '500x500', size = 4)
    app.mainloop()


if __name__ == "__main__":
    main()
