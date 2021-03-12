import tkinter as tk
from tkinter import messagebox


class Application(tk.Frame):
    def __init__(self, master=None, title = 'App', **kwargs):
        super().__init__(master, **kwargs)

        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.master.title(title)

        self.grid(sticky="NEWS")

        self.the_end = []
        for i in range(1, 5):
            for j in range(0, 4):
                self.the_end.append([i,j])
        self.the_end.pop()

        self.createWidgets()


    def createWidgets(self):
        self.void_col = 3
        self.void_row = 4

        for i in range(1, 4):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        self.new = tk.Button(self, text='New')
        self.quit = tk.Button(self, text='Quit', command=self.quit)

        self.buttons = dict()
        for i in range(1, 16):
            self.buttons[i] = tk.Button(self, text = str(i), command=lambda i=i: self.change_location(i))

        row_ = 1
        col_ = 0
        for i in range(1, 16):
            self.buttons[i].grid(row = row_, column = col_, sticky = "NEWS")
            col_ += 1
            if col_ == 4:
                col_ = 0
                row_ += 1

        self.new.grid(row=0, column=0, columnspan = 2, sticky="NS")
        self.quit.grid(row=0, column= 2, columnspan = 2, sticky="NS")

    def change_location(self, i):
        row = self.buttons[i].grid_info()['row']
        col = self.buttons[i].grid_info()['column']
        if col == self.void_col and abs(row - self.void_row) == 1 or row == self.void_row and abs(col - self.void_col) == 1:
            self.buttons[i].grid(row = self.void_row, column = self.void_col)
            self.void_col = col
            self.void_row = row
            if self.check():
                tk.messagebox.showinfo("Victory", "You Win!")

    def check(self):
        position = []
        for i in range(1, 16):
            row = self.buttons[i].grid_info()['row']
            col = self.buttons[i].grid_info()['column']
            position.append([row,col])
        if self.the_end == position:
            return True
        return False


def main():
    app = Application(title = '15 puzzle')
    app.mainloop()


if __name__ == "__main__":
    main()
