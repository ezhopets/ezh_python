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
        self.l = InputLabel(self, font= "fixed", text='Python <3', cursor='spider', takefocus=1, highlightthickness = 3, anchor = 'w')
        self.calc = tk.Button(self, font = ('fixed', 10,  'bold'),text=' = ', command = self.l.calc, **self.buttons_design)

        self.l.grid(row=0, column=0, columnspan = 2, sticky = "EW")
        self.calc.grid(row=1, column=0,sticky = "WS")
        self.quit.grid(row=1, column=1,sticky = "ES")


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
        self.bind("<Home>", self.move_home)
        self.bind("<End>", self.move_end)
        self.bind("<Tab>", self.ignore)
        self.bind("<Escape>", self.ignore)
        self.bind("<Return>", self.ignore)
        self.bind("<Delete>", self.delete)

        self.createWidgets()


    def createWidgets(self):
        self.xVar = tk.IntVar()
        self.xVar.set(0)
        self.y = 0

        self.frame = tk.Frame(self, height= self.metrix['linespace'], width = 4, bg = 'red')


    def key_press(self, event):
        if (event.char):
            if self.textvar:
                self.textvar.set(self.textvar.get()[:self.cur_pos] + event.char + self.textvar.get()[self.cur_pos:])
            else:
                self.config(text = self["text"][:self.cur_pos] + event.char + self["text"][self.cur_pos:])

            self.xVar.set(self.xVar.get() + self.m_len)
            self.frame.place(x= self.xVar.get(), y = self.y)
            self.right_border += self.m_len
            self.cur_pos += 1


    def ignore(self, event):
        pass


    def calc(self, *args, **kwargs):
        def sequre_check(s):
            for c in s:
                if c.isalpha():
                    return False

            return True

        if self.textvar:
            if sequre_check(self.textvar.get()):
                try:
                    self.textvar.set(str(eval(self.textvar.get())))
                except Exception as exc:
                    self.textvar.set(str(type(exc).__name__))

            else:
                self.textvar.set("Error!")

        else:
            if sequre_check(self["text"]):
                try:
                    self.config(text = str(eval(self["text"])))
                except Exception as exc:
                    self.config(text =str(type(exc).__name__))
            else:
                self.config(text = "Error!")

        self.right_border = len(self['text']) * self.m_len

        self.xVar.set(self.right_border)
        self.frame.place(x= self.xVar.get(), y = self.y)
        self.cur_pos = self.right_border // self.m_len


    def move_left(self, event = None):
        new_x = self.xVar.get() - self.m_len
        if (new_x >= 0):
            self.xVar.set(new_x)
            self.frame.place(x= self.xVar.get(), y = self.y)
            self.cur_pos -= 1
            return True
        return False


    def move_right(self, event=None):
        new_x = self.xVar.get() + self.m_len

        if (new_x <= self.right_border):
            self.xVar.set(new_x)
            self.frame.place(x= self.xVar.get(), y = self.y)
            self.cur_pos += 1


    def move_home(self, event):
        new_x = 0
        self.xVar.set(new_x)
        self.frame.place(x= self.xVar.get(), y = self.y)
        self.cur_pos = 0


    def move_end(self, event):
        new_x = self.right_border
        self.xVar.set(new_x)
        self.frame.place(x= self.xVar.get(), y = self.y)
        self.cur_pos = self.right_border // self.m_len


    def back_space(self, *arg):
        if self.textvar and self.textvar.get():
            if (self.move_left()):
                self.textvar.set(self.textvar.get()[:self.cur_pos] + self.textvar.get()[self.cur_pos + 1:])
                self.right_border -= self.m_len
        elif self["text"]:
            if (self.move_left()):
                self.config(text = self["text"][:self.cur_pos] + self["text"][self.cur_pos + 1:])
                self.right_border -= self.m_len


    def delete(self, *arg):
        if self.textvar and self.textvar.get():
            self.textvar.set(self.textvar.get()[:self.cur_pos] + self.textvar.get()[self.cur_pos + 1:])
        elif self["text"]:
            self.config(text = self["text"][:self.cur_pos] + self["text"][self.cur_pos + 1:])

        new_x = self.xVar.get() + self.m_len
        if (new_x <= self.right_border):
            self.right_border -= self.m_len


    def focus_in(self, event):
        self.frame.place(x= self.xVar.get(), y = self.y)


    def focus_out(self, event):
        self.frame.place_forget()


    def foc(self, event):
        self.focus_force()

        if (event.x > self.right_border):
            self.xVar.set(self.right_border)
        else:
            self.xVar.set((event.x + (1/4) * self.m_len) // self.m_len * self.m_len)

        self.cur_pos = self.xVar.get() // self.m_len
        self.frame.place(x= self.xVar.get(), y = self.y)


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()
