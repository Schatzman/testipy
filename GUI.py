
import tkinter
import traceback
from util.core import read_yaml

class Window(object):
    def __init__(self):
        self.WIN = tkinter.Tk()
        self.prtcl_name = ''
        self.func = ''
        self.title = '' 
        self.xy = [0,0]
        self.config_file = 'testipy.yaml'

    def window_closed(self):
        self.WIN.destroy()

    def window_show(self):
        self.WIN.deiconify()

    def configure(self, prtcl_name, resize, func, title, x, y):
        self.WIN.protocol(prtcl_name, func)
        self.WIN.wm_title(title)
        self.WIN.resizable(x,y)

    def auto_configure(self):
        self.yaml_dump = read_yaml(self.config_file)
        cfg_data = self.yaml_dump
        prtcl_name = cfg_data["protocol"]
        resize = cfg_data["resizeable"]
        func = self.window_closed
        title = cfg_data["title"]
        x = cfg_data["width"]
        y = cfg_data["height"]
        self.configure(
            prtcl_name,
            resize,
            func,
            title,
            x,y
            )

class Dialog(object):

    def __init__(self, main, info, title):

        top = self.top = tkinter.Toplevel(main)
        top.wm_title(title)
        tkinter.Label(top, text=info).pack()

        button = tkinter.Button(top,text="OK",command=self.ok)
        button.pack(pady=5)
        self.main = main

    def ok(self):
        self.main.deiconify()
        self.top.destroy()

## MAIN 

class AppGUI(object):

    def __init__(self, main, test=False):
        self.label_dir_path = tkinter.Label(main.WIN,text="Path to directory:")
        self.label_dir_path.grid(row=0,column=0)

        self.dir_path_input = tkinter.StringVar()
        self.dir_path_entry = tkinter.Entry(main.WIN,textvariable=self.dir_path_input)
        self.dir_path_entry.grid(row=0,column=1)

        self.label_log_path = tkinter.Label(main.WIN,text="Path to logfile:")
        self.label_log_path.grid(row=1,column=0)

        self.log_path_input = tkinter.StringVar()
        self.log_path_entry = tkinter.Entry(main.WIN,textvariable=self.log_path_input)
        self.log_path_entry.grid(row=1,column=1)

        self.label_check = tkinter.Label(main.WIN,text="Yes. Have some.:")
        self.label_check.grid(row=2,column=0)

        self.check_var = tkinter.IntVar()

        self.checkbutton_get_ref_list = tkinter.Checkbutton(main.WIN,variable=self.check_var)
        self.checkbutton_get_ref_list.grid(row=2,column=1)

        self.go_button = tkinter.Button(main.WIN,text="GO!",command=self.go_callback,width=15)
        self.go_button.grid(row=3,column=0)

        self.chk_input_button = tkinter.Button(main.WIN,text="Check input",command=self.check_input,width=15)
        self.chk_input_button.grid(row=3,column=1)

        self.main = main

        if not test:
            self.main.WIN.mainloop()

    def go_callback(self):
        dialog = self.spawn_dialog("<default go callback msg>", "DEFAULT TITLE!!1")
        self.main.WIN.wait_window(dialog.top)

    def spawn_dialog(self, msg, title):
        dialog = Dialog(self.main.WIN, msg, title)
        return dialog

    def convert_check_to_bool(self, check_val):
        if check_val == 1:
            return True
        elif check_val == 0:
            return False
        else:
            print(traceback.format_exc())
            raise Exception(
                "convert_check_to_bool failed, " +
                "check_input param != 1 or 0. Instead got " + 
                repr(check_val)
                )

    def check_input(self):
        check_val = self.convert_check_to_bool(self.check_var.get())
        input_string = (
        "Directory path: " +
        self.dir_path_input.get() +
        "\n" +
        "Log path: " +
        self.log_path_input.get() +
        "\n" +
        "Checked?: " +
        str(check_val)
        )
        dialog = self.spawn_dialog(input_string, "Check input??/")
        self.main.WIN.wait_window(dialog.top)
