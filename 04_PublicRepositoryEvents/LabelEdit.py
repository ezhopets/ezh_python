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

        self.font = tkFont.Font(font=("Courier", 20))
        self.config(font = self.font)
        self.m_len = self.font.measure('A')
        self.metrix = self.font.metrics()

        try:
            self.textvar = kwargs["textvariable"]
            self.right_border = len(self.textvar.get()) * self.m_len
        except:
            self.textvar = None
            try:
                self.text = kwargs["text"]
                self.right_border = len(self.text) * self.m_len
            except:
                self.text = None
                self.right_border = 0

        self.cur_pos = self.right_border // self.m_len

        self.bind("<KeyPress>", self.key_press)
        self.bind("<KeyPress-BackSpace>", self.back_space)
        self.bind("<Button-1>", self.foc)
        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)
        self.bind("<Left>", self.move_left)
        self.bind("<Right>", self.move_right)

        self.createWidgets()

    def createWidgets(self):
        self.xVar = tk.IntVar()
        self.y = 0

        self.xVar.set(0)
        self.frame = tk.Frame(self, height= 20, width = 4, bg = 'red')

    def key_press(self, event):
        if (event.char):
            if self.textvar:
                self.textvar.set(self.textvar.get()[:self.cur_pos] + event.char + self.textvar.get()[self.cur_pos:])

                self.xVar.set(self.xVar.get() + self.m_len)
                self.frame.place(x= self.xVar.get(), y = self.y)
                self.right_border += self.m_len
                self.cur_pos += 1
            else:
                self.config(text = self["text"][:self.cur_pos] + event.char + self["text"][self.cur_pos:])
                self.xVar.set(self.xVar.get() + self.m_len)
                self.frame.place(x= self.xVar.get(), y = self.y)
                self.right_border += self.m_len
                self.cur_pos += 1

    def move_left(self, event = None):
        new_x = self.xVar.get() - self.m_len
        if (new_x >= 0):
            self.xVar.set(new_x)
            self.frame.place(x= self.xVar.get(), y = self.y)
            self.cur_pos -= 1
            return True
        return False


    def move_right(self, event):
        new_x = self.xVar.get() + self.m_len

        if (new_x <= self.right_border):
            self.xVar.set(new_x)
            self.frame.place(x= self.xVar.get(), y = self.y)
            self.cur_pos += 1

    def back_space(self, *arg):
        if self.textvar and self.textvar.get():
            if (self.move_left()):
                self.textvar.set(self.textvar.get()[:self.cur_pos] + self.textvar.get()[self.cur_pos + 1:])
                self.right_border -= self.m_len
        elif self["text"]:
            if (self.move_left()):
                self.config(text = self["text"][:self.cur_pos] + self["text"][self.cur_pos + 1:])
                self.right_border -= self.m_len

    def focus_in(self, event):
        self.frame.place(x= self.xVar.get(), y = self.y)

    def focus_out(self, event):
        self.frame.place_forget()

    def foc(self, event):
        self.focus_force()
        self.xVar.set(self.right_border)
        self.cur_pos = self.right_border // self.m_len
        self.frame.place(x= self.xVar.get(), y = self.y)


def main():
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()
