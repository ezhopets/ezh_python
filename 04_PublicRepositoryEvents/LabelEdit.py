import tkinter as tk
import tkinter.font as tkFont


class Application(tk.Frame):

    def __init__(self, master=None, title = 'App', **kwargs):
        super().__init__(master, **kwargs)

        self.master.rowconfigure(0, weight = 1)
        self.master.columnconfigure(0, weight = 1)
        self.master.title(title)

        self.grid(sticky="NEWS")
        self.configure(background='DarkOliveGreen1')


        self.buttons_design = dict(activebackground = 'DarkOliveGreen3',\
                activeforeground= 'grey10', bd = 4, bg = 'DarkOliveGreen2',\
                fg = 'grey20')

        self.createWidgets()

    def createWidgets(self, *kwargs):
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)

        textvar = tk.StringVar()
        textvar.set("pupa")


        self.quit = tk.Button(self, font = ('fixed', 10,  'bold'),text='Quit', command=self.master.quit, **self.buttons_design)
        self.l1 = InputLabel(self, font= "fixed", text='lupa', cursor='heart', takefocus=1, highlightthickness = 3, anchor = 'w')
        self.l2 = InputLabel(self, font= "fixed", textvariable=textvar, cursor='spider', takefocus=1, highlightthickness = 3,  anchor='w')
        self.l3 = InputLabel(self, font= "fixed", cursor='star', takefocus=1, highlightthickness = 3, anchor='w')

        self.l1.grid(row=0, column=0, sticky = "EW")
        self.l2.grid(row=1, column=0, sticky = "EW")
        self.l3.grid(row=2, column=0, sticky = "EW")
        self.quit.grid(row=3, column=0,sticky = "ES")


class InputLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.textvar = kwargs["textvariable"]
        except:
            self.textvar = None
            try:
                self.text = kwargs["text"]
            except:
                self.text = None

        self.bind("<KeyPress>", self.key_press)
        self.createWidgets()

    def createWidgets(self):
        self.xVar = tk.IntVar()
        self.y = 0

        self.xVar.set(0)
        self.frame = tk.Frame(self, height= 20, width = 4, bg = 'red')

        self.frame.place(x= self.xVar.get(), y = 0)

    def key_press(self, event):
        if (event.char):
            if self.textvar:
                self.textvar.set(self.textvar.get()[:] + event.char)
                self.xVar.set(self.xVar.get() + 10)
                self.frame.place(x= self.xVar.get(), y = self.y)
            else:
                self.config(text = self["text"][:] + event.char)
                self.xVar.set(self.xVar.get() + 10)
                self.frame.place(x= self.xVar.get(), y = self.y)


def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
