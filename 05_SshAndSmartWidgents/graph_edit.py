import os
import re
import tkinter as tk
from colors import COLORS
from tkinter.filedialog import askopenfilename, asksaveasfile
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askfloat


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

        self.shape = tk.StringVar()
        self.shape.set('oval')

        self.xy = tk.IntVar()
        self.xy.set("1:1")

        self.ink = tk.StringVar()
        self.ink.set('black')

        self.fill = tk.StringVar()
        self.fill.set('white')

        self.width = 1.0

        self.text = tk.StringVar()
        self.pattern = re.compile("(oval|rectangle|arc|line) (\[(-?\d+\.\d+), "
                "(-?\d+\.\d+), (-?\d+\.\d+), (-?\d+\.\d+)\]) (\d+\.\d+) "
                "(#[a-fA-F\d][a-fA-F|\d][a-fA-F\d][a-fA-F\d][a-fA-F\d][a-fA-F\d]|" +
                '|'.join(COLORS) +
                ") (#[a-fA-F\d][a-fA-F|\d][a-fA-F\d][a-fA-F\d][a-fA-F\d][a-fA-F\d]|" +
                '|'.join(COLORS) +
                ")\n*")
        print(self.pattern)

        self.grid(sticky="NEWS")
        self.create_widgets()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
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
        self.C.bind_all("<Alt-KeyPress-x>", self.compile_right)
        self.C.bind_all("<Alt-KeyPress-z>", self.compile_left)

        self.ink_button = tk.Button(self.F2, text = 'Ink', width=7, command=self.choose_ink)
        self.width_button = tk.Button(self.F2, text='Width', command=self.choose_width)

        self.fill_button = tk.Button(self.F2, text='Fill', width=7, command=self.choose_fill)
        self.pic = tk.Label(self.F2, text = 'O', width=1, fg=self.ink.get(), bg=self.fill.get())
        self.shape_button = tk.Menubutton(self.F2, textvariable = self.shape, width=7)
        shapes = ('oval', 'rectangle', 'arc', 'line')

        self.shape_button.menu = tk.Menu(self.shape_button, tearoff=False)

        for shape in shapes:
            self.shape_button.menu.add_radiobutton(
                    label=shape,
                    value=shape,
                    variable=self.shape)

        self.shape_button['menu'] = self.shape_button.menu

        self.coord = tk.Label(self.F2, textvariable = self.xy, width=7)
        self.ink_button.grid(row=0, column=0, sticky="EW")
        self.width_button.grid(row=0, column=1, sticky="EW")
        self.fill_button.grid(row=0, column=2, sticky="EW")
        self.pic.grid(row=0, column=3, sticky="EW")
        self.shape_button.grid(row=0, column=4, sticky="EW")
        self.coord.grid(row=0, column=5, sticky="EW")

        self.load = tk.Button(self.F3, text = 'Load', width=7, command=self.load_file)
        self.save = tk.Button(self.F3, text='Save', width=7, command=self.save_file)
        self.quit = tk.Button(self.F3, text = 'Quit', command=self.master.quit, width=7)

        self.load.grid(row=0, column=0, sticky="W")
        self.save.grid(row=0, column=1, sticky="W")
        self.quit.grid(row=0, column=2, sticky="E")

    def choose_ink(self, *arg):
        color = askcolor()[-1]
        if color:
            self.ink.set(color)
            self.pic.config(fg=self.ink.get())

    def choose_fill(self, *arg):
        color = askcolor()[-1]
        if color:
            self.fill.set(color)
            self.pic.config(bg=self.fill.get())


    def choose_width(self, *arg):
        width = askfloat('lol', "Enter")
        if width:
            self.width = width


    def move(self, event):
        self.index = self.C.find_closest(event.x, event.y)
        self.C.tag_raise(self.index)
        self.ifmove = True
        self.last_x, self.last_y = event.x, event.y

    def move_draw(self, event):
        self.mx2 = event.x
        self.my2 = event.y
        self.xy.set(f"{event.x}:{event.y}")

        if (self.if_press):
            if (self.ifmove):
                self.C.move(self.index, event.x - self.last_x, event.y - self.last_y)
                self.last_x, self.last_y = event.x, event.y
            else:
                self.C.delete(self.cur_obj)
                if self.shape.get() == 'oval':
                    self.cur_obj = self.C.create_oval(self.mx1, self.my1, self.mx2, self.my2, fill=self.fill.get(), outline=self.ink.get(), width=self.width)
                elif self.shape.get() == 'rectangle':
                    self.cur_obj = self.C.create_rectangle(self.mx1, self.my1, self.mx2, self.my2, fill=self.fill.get(), outline=self.ink.get(), width=self.width)
                elif self.shape.get() == 'arc':
                    self.cur_obj = self.C.create_arc(self.mx1, self.my1, self.mx2, self.my2, fill=self.fill.get(), outline=self.ink.get(), width=self.width)
                elif self.shape.get() == 'line':
                    self.cur_obj = self.C.create_line(self.mx1, self.my1, self.mx2, self.my2, fill=self.fill.get(), width=self.width)

    def press(self, event):
        self.mx1 = event.x
        self.my1 = event.y
        self.if_press = True
        if not self.ifmove:
            if self.shape.get() == 'oval':
                self.cur_obj = self.C.create_oval(self.mx1, self.my1, self.mx1, self.my1, fill=self.fill.get(), outline=self.ink.get(), width=self.width)
            elif self.shape.get() == 'rectangle':
                self.cur_obj = self.C.create_rectangle(self.mx1, self.my1, self.mx1, self.my1, fill=self.fill.get(), outline=self.ink.get(), width=self.width)
            elif self.shape.get() == 'arc':
                self.cur_obj = self.C.create_arc(self.mx1, self.my1, self.mx1, self.my1, fill=self.fill.get(), outline=self.ink.get(), width=self.width)
            elif self.shape.get() == 'line':
                self.cur_obj = self.C.create_line(self.mx1, self.my1, self.mx1, self.my1, fill=self.fill.get(), width=self.width)

    def release(self, event):
        self.if_press = False
        self.ifmove = False
        self.mx2 = event.x
        self.my2 = event.y
        self.C.tag_bind(self.cur_obj, '<Button-1>', self.move)

    def compile_right(self, event):
        self.T.delete(0.0, tk.END)
        for index in self.C.find_all():
            self.text.set((f"{self.C.type(index)} "
                    f"{self.C.coords(index)} "
                    f"{self.C.itemconfigure(index)['width'][-1]} "
                    f"{self.C.itemconfigure(index)['outline'][-1]} "
                    f"{self.C.itemconfigure(index)['fill'][-1]}\n"))
            self.T.insert(tk.END, self.text.get())

    def compile_left(self, event):
        objects = []
        for i in range(1, int(self.T.index('end').split('.')[0])):
            line = self.T.get(f"{i}.0", f"{i}.end")
            if not line:
                continue
            objects += [self.pattern.fullmatch(line).groups()]
            if objects[-1] is None:
                print("LOshara")
                return

        self.C.delete("all")
        for obj in objects:
            if obj[0] == 'oval':
                self.cur_obj = self.C.create_oval(obj[2], obj[3], obj[4], obj[5], width=obj[6], outline=obj[7], fill=obj[8])
            elif obj[0] == 'rectangle':
                self.cur_obj = self.C.create_rectangle(obj[2], obj[3], obj[4], obj[5], width=obj[6], outline=obj[7], fill=obj[8])
            elif obj[0] == 'arc':
                self.cur_obj = self.C.create_arc(obj[2], obj[3], obj[4], obj[5], width=obj[6], outline=obj[7], fill=obj[8])
            elif obj[0] == 'line':
                self.cur_obj = self.C.create_line(obj[2], obj[3], obj[4], obj[5], width=obj[6], fill=obj[7])
            print(objects)
            print(self.C.find_all())
            print(self.cur_obj)
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
                        geometry = "1600x800",
                        filename = "pupa.txt")
    app.mainloop()


if __name__ == "__main__":
    main()
