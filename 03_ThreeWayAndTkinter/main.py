import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None, title = 'App', **kwargs):
        super().__init__(master, **kwargs)

        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.master.title(title)

        self.grid(sticky="NEWS")

        self.createWidgets()

    def createWidgets(self):
        self.new = tk.Button(self, text='New')
        self.quit = tk.Button(self, text='Quit', command=self.quit)

        self.new.grid(row=0, column=0, sticky="NS")
        self.quit.grid(row=0, column= 1, sticky="NS")



def main():
    app = Application(title = '15 puzzle')
    app.mainloop()


if __name__ == "__main__":
    main()
