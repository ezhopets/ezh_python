import os
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfile

class Application(tk.Frame):
    def __init__(self, master=None, title="App",
            geometry = "800x600", filename = 'pupa.txt', **kwargs):

        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.geometry(geometry)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.file = filename
        self.if_press = False
        self.ifmove = False

        self.grid(sticky="NEWS")
        self.create_widgets()

        self.columnconfigure(0, weight=10)
        self.rowconfigure(0, weight=10)
        self.columnconfigure(1, weight=1)

    def create_widgets(self):
        self.F1 = tk.LabelFrame(self, text=self.file)
        self.F1.grid(row=0, column=0, sticky="NEWS")
        self.F1.rowconfigure(0, weight=1)
        self.F1.columnconfigure(0, weight=1)

        self.F2 = tk.Frame(self)
        self.F2.grid(row=0, column=1, sticky="NEWS")
        self.F2.rowconfigure(1, weight=1)
        self.F2.columnconfigure(0, weight=1)
        self.F2.columnconfigure(1, weight=1)
        self.F2.columnconfigure(2, weight=1)
        self.F2.columnconfigure(3, weight=1)
        self.F2.columnconfigure(4, weight=1)
        self.F2.columnconfigure(5, weight=1)

        self.F3 = tk.Frame(self)
        self.F3.grid(row=1, column=0, columnspan=2, sticky="NEWS")
        self.F3.columnconfigure(2, weight=1)

        self.T = tk.Text(self.F1, undo = True, font = "Courier", wrap=tk.WORD,
                inactiveselectbackground = "Lime")
        self.load_file(ask=False)

        self.T.grid(row=0, column=0, sticky="NEWS")

        self.C = tk.Canvas(self.F2)
        self.C.grid(row=1, column=0, columnspan = 6, sticky="NEWS")
        self.C.bind("<Button-1>", self.press)
        self.C.bind("<ButtonRelease>", self.release)
        self.C.bind("<Motion>", self.move_draw)

        self.ink = tk.Menubutton(self.F2, text = 'Ink', width=7)
        self.width = tk.Menubutton(self.F2, text='1', width=7)
        self.fill = tk.Menubutton(self.F2, text='Fill', width=7)
        self.pic_fill = tk.Menubutton(self.F2, text = 'lol', width=7)
        self.shape = tk.Menubutton(self.F2, text = 'oval', width=7)
        self.coord = tk.Label(self.F2, text = '1:1', width=7)

        self.ink.grid(row=0, column=0, sticky="EW")
        self.width.grid(row=0, column=1, sticky="EW")
        self.fill.grid(row=0, column=2, sticky="EW")
        self.pic_fill.grid(row=0, column=3, sticky="EW")
        self.shape.grid(row=0, column=4, sticky="EW")
        self.coord.grid(row=0, column=5, sticky="EW")

        self.load = tk.Button(self.F3, text = 'Load', width=7, command=self.load_file)
        self.save = tk.Button(self.F3, text='Save', width=7, command=self.save_file)
        self.quit = tk.Button(self.F3, text = 'Quit', command=self.master.quit, width=7)

        self.load.grid(row=0, column=0, sticky="W")
        self.save.grid(row=0, column=1, sticky="W")
        self.quit.grid(row=0, column=2, sticky="E")

    def move(self, event):
        self.index = self.C.find_closest(event.x, event.y)
        self.C.tag_raise(self.index)
        self.ifmove = True
        self.last_x, self.last_y = event.x, event.y

    def move_draw(self, event):
        self.mx2 = event.x
        self.my2 = event.y

        if (self.if_press):
            if (self.ifmove):
                self.C.move(self.index, event.x - self.last_x, event.y - self.last_y)
                self.last_x, self.last_y = event.x, event.y
            else:
                self.C.delete(self.cur_obj)
                self.cur_obj = self.C.create_oval(self.mx1, self.my1, self.mx2, self.my2, fill='red')

    def press(self, event):
        self.mx1 = event.x
        self.my1 = event.y
        self.if_press = True
        if self.ifmove:
            pass
        else:
            self.cur_obj = self.C.create_oval(self.mx1, self.my1, self.mx1, self.my1, fill='red')

    def release(self, event):
        self.if_press = False
        self.ifmove = False
        self.mx2 = event.x
        self.my2 = event.y
        self.C.tag_bind(self.cur_obj, '<Button-1>', self.move)

    def load_file(self, ask= True):
        if ask:
            filename = askopenfilename()
        else:
            filename = self.file

        if not filename:
            return

        self.T.delete('1.0', tk.END)
        try:
            with open(filename, 'r') as file:
                self.F1.config(text=os.path.basename(file.name))
                self.T.insert('1.0', file.read())
        except:
            self.F1.config(text="Untitled.txt")


    def save_file(self, *arg):
        f = asksaveasfile(mode='w', defaultextension=".txt")
        try:
            self.F1.config(text=os.path.basename(f.name))
        except:
            pass
        if f is None:
            return
        save_text = str(self.T.get(1.0, tk.END))
        f.write(save_text)
        f.close()


def main():
    app = Application(title="Graph Edit",
                        geometry = "750x450",
                        filename = "pupa.txt")
    app.mainloop()


if __name__ == "__main__":
    main()
    print('lol')

