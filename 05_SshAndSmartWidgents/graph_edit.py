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

        self.grid(sticky="NEWS")
        self.create_widgets()

        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1] - 1):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        self.F1 = tk.LabelFrame(self, text='pupa')
        self.F1.grid(row=0, column=0, sticky="NEWS")
        self.F1.rowconfigure(0, weight=1)
        self.F1.columnconfigure(0, weight=1)

        self.F2 = tk.Frame(self)
        self.F2.grid(row=0, column=1, sticky="NEWS")
        self.F2.rowconfigure(0, weight=1)
        self.F2.columnconfigure(0, weight=1)

        self.F3 = tk.Frame(self)
        self.F3.grid(row=1, column=0, columnspan=2, sticky="NEWS")
        self.F3.columnconfigure(2, weight=1)


        self.T = tk.Text(self.F1, undo = True, font = "Courier", wrap=tk.WORD,
                inactiveselectbackground = "Lime")
        self.load_file(self.file)

        self.T.grid(row=0, column=0, sticky="NEWS")


        self.C = tk.Canvas(self.F2)
        self.C.grid(row=0, column=0, sticky="NEWS")

        self.load = tk.Button(self.F3, text = 'Load', width=7, command=self.load_file)
        self.save = tk.Button(self.F3, text='Save', width=7, command=self.save_file)
        self.quit = tk.Button(self.F3, text = 'Quit', command=self.master.quit, width=7)

        self.load.grid(row=0, column=0, sticky="W")
        self.save.grid(row=0, column=1, sticky="W")
        self.quit.grid(row=0, column=2, sticky="E")


    def load_file(self, *arg):
        filename = askopenfilename()
        self.T.delete('1.0', tk.END)
        with open(filename, 'r') as file:
            self.T.insert('1.0', file.read())


    def save_file(self, *arg):
        f = asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:
            return
        save_text = str(self.T.get(1.0, tk.END))
        f.write(save_text)
        f.close()


def main():
    app = Application(title="Graph Edit",
                        geometry = "800x600",
                        filename = "pupa.txt")
    app.mainloop()


if __name__ == "__main__":
    main()
