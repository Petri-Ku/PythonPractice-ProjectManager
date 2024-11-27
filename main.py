import tkinter, os
import ctypes as ct
import tkinter.messagebox
import tkinter.scrolledtext
import tkinter.simpledialog

# Make title bar dark, code from: https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter
def dark_title_bar(window):
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                         ct.sizeof(value))

class UI:
    def __init__(self, app):
        self.app = app
        self.static()
        self.login()
        self.projects()

    # Remove selection on button click
    def change_focus(event):
        event.widget.focus_set()

    # Active username and what was done text on top left
    def static(self):
        self.username = ""
        self.active_user = tkinter.Label(self.app, text="", bg="#2e2e2e", fg="gray")
        self.action = tkinter.Label(self.app, text="", bg="#2e2e2e", fg="gray")

        self.active_user.place(x=5, y=0)
        self.action.place(x=70, y=0)

    # Login labels, entrys and button
    def login(self):
        self.user_label = tkinter.Label(self.app, text="Username:", bg="#2e2e2e", fg="white")
        self.user_entry = tkinter.Entry(self.app, bg="lightgray", fg="black")
        self.passw_label = tkinter.Label(self.app, text="Password:", bg="#2e2e2e", fg="white")
        self.passw_entry = tkinter.Entry(self.app, bg="lightgray", fg="black", show="*")
        self.login_button = tkinter.Button(self.app, text="Login", bg="gray", fg="white", command=self.click_login)

        self.add_new_user_button = tkinter.Button(self.app, text="New user", bg="gray", fg="white", command=self.click_new_user)

        self.show_login()

    # Login button click
    def click_login(self):
        user = False
        with open ("data/users.txt") as file:
            for row in file:
                row = row.replace("\n","")
                part = row.split(";")
                name = part[0]
                passw = part[1]
                if name == self.user_entry.get() and passw == self.passw_entry.get():
                    self.username = name
                    self.active_user.configure(text=name)
                    self.action.configure(text="Logged in")
                    
                    self.show_projects()
                    self.hide_login()
                      
                    user = True
                    break
            if user == False:
                self.action.configure(text="Wrong username or password")
                self.passw_entry.delete(0, "end")

    # New user button click
    def click_new_user(self):
        conflict = False
        with open ("data/users.txt") as file:
            for row in file:
                row = row.replace("\n", "")
                part = row.split(";")
                name = part[0]
                if name == self.user_entry.get():
                    self.action.configure(text="Username already exists")
                    conflict = True
                    break
        if self.user_entry.get() == "" or self.passw_entry.get() == "":
            self.action.configure(text="Username or password can't be empty")
        elif conflict == False:
            with open ("data/users.txt", "a") as file:
                file.write(self.user_entry.get())
                file.write(";")
                file.write(self.passw_entry.get())
                file.write("\n")
            self.action.configure(text=f"User: {self.user_entry.get()} added")
            self.user_entry.delete(0, "end")    
            self.passw_entry.delete(0, "end")

    # Select project with single click 1/2
    def select_line(self, event=None):
        self.projects_textbox.tag_add("sel", "insert linestart", "insert lineend")
        self.projects_textbox.tag_config("sel", background="black")

        self.task_move_inprogress_button.configure(state="disabled")
        self.inprogress_textbox.configure(state="normal")
        self.tasks_textbox.configure(state="normal")
        self.done_textbox.configure(state="normal")

        self.tasks_textbox.delete("1.0", tkinter.END)
        self.inprogress_textbox.delete("1.0", tkinter.END)
        self.done_textbox.delete("1.0", tkinter.END)
        
        try:
            self.project = self.projects_textbox.selection_get()
            with open (f"data/projects/{self.projects_textbox.selection_get()}/tasks.txt") as file:
                for row in file:
                    self.tasks_textbox.insert(tkinter.INSERT, row)   
            
            with open (f"data/projects/{self.projects_textbox.selection_get()}/inprogress.txt") as file:
                for row in file:
                    self.inprogress_textbox.insert(tkinter.INSERT, row)
            
            with open (f"data/projects/{self.projects_textbox.selection_get()}/done.txt") as file:
                for row in file:
                    self.done_textbox.insert(tkinter.INSERT, row)
            self.action.configure(text=f"Showing '{self.projects_textbox.selection_get()}' project tasks")
        except:
            self.project = ""
            self.action.configure(text="Clicked on empty spot on projects window")
        
        self.tasks_textbox.configure(state="disabled")
        self.inprogress_textbox.configure(state="disabled")
        self.done_textbox.configure(state="disabled")

    # App UI elements
    def projects(self):
        self.do = ""
        self.project = ""
        self.task = ""
        self.active_projects_button = tkinter.Button(self.app, relief="sunken", text="Active", bg="gray", fg="white", height=1, width=5, command=self.click_ap, state="disabled")
        self.done_projects_button = tkinter.Button(self.app, relief="raised", text="Done", bg="gray", fg="white", height=1, width=5, command=self.click_dp) 
        self.projects_label = tkinter.Label(self.app, font=("consolas", 14, "bold"), text="Projects", bg="#2e2e2e", fg="white")
        self.projects_textbox = tkinter.Text(self.app, cursor="arrow", bg="gray", fg="white", height=10, width=15)
        self.project_add_button = tkinter.Button(self.app, text="Add new", bg="gray", fg="white", height=1, width=7, command=self.click_new_p)
        self.project_markdone_button = tkinter.Button(self.app, text="Done", bg="gray", fg="white", height=1, width=7, command=self.click_mark_p_d)
        self.project_markundone_button = tkinter.Button(self.app, text="Not done", bg="gray", fg="white", height=1, width=7, command=self.click_notdone_p)
        self.project_remove_button = tkinter.Button(self.app, text="Delete", bg="gray", fg="white", height=1, width=7, command=self.click_remove_p)

        self.entrybox = tkinter.Entry(self.app, bg="lightgray", fg="black")
        self.entrybox_ok_button = tkinter.Button(self.app, text="Ok", bg="gray", fg="white", height=1, width=5, command=self.click_ok)
        self.entrybox_cancel_button = tkinter.Button(self.app, text="Cancel", bg="gray", fg="white", height=1, width=5, command=self.click_cancel)

        self.tasks_label = tkinter.Label(self.app, font=("consolas", 14, "bold"), text="Tasks", bg="#2e2e2e", fg="white")
        self.tasks_textbox = tkinter.Text(self.app, cursor="arrow", bg="gray", fg="white", height=10, width=15)
        self.task_add_button = tkinter.Button(self.app, text="Add new", bg="gray", fg="white", height=1, width=7, command=self.click_add_task)
        self.task_move_inprogress_button = tkinter.Button(self.app, text=">", bg="gray", fg="white", height=1, width=7, command=self.click_task_to_inprog, state="disabled")

        self.inprogress_label = tkinter.Label(self.app, font=("consolas", 14, "bold"), text="In progress", bg="#2e2e2e", fg="white")
        self.inprogress_textbox = tkinter.Text(self.app, cursor="arrow", bg="gray", fg="white", height=10, width=15)
        self.inprogress_move_tasks = tkinter.Button(self.app, text="<", bg="gray", fg="white", height=1, width=7, command=self.click_inprog_to_task, state="disabled")
        self.inprogress_move_done = tkinter.Button(self.app, text=">", bg="gray", fg="white", height=1, width=7, command=self.click_inprog_to_done, state="disabled")

        self.done_label = tkinter.Label(self.app, font=("consolas", 14, "bold"), text="Done", bg="#2e2e2e", fg="white")
        self.done_textbox = tkinter.Text(self.app, cursor="arrow", bg="gray", fg="white", height=10, width=15)
        self.done_move_inprogress = tkinter.Button(self.app, text="<", bg="gray", fg="white", height=1, width=7, command=self.click_done_to_inprog, state="disabled")
        
        self.logout_button = tkinter.Button(self.app, text="Logout", bg="gray", fg="white", command=self.click_logout)

         # Select with single click 2/2
        self.projects_textbox.bind("<ButtonRelease>", self.select_line)
        self.tasks_textbox.bind("<ButtonRelease>", self.select_task_line)
        self.inprogress_textbox.bind("<ButtonRelease>", self.select_inprogress_line)
        self.done_textbox.bind("<ButtonRelease>", self.select_done_line)

    # Add active projects to projects textbox
        for row in os.listdir("data/projects"):
            row = row + "\n"
            self.projects_textbox.insert(tkinter.INSERT, row)
        self.projects_textbox.configure(state="disabled")

    # Active projects button click
    def click_ap(self):
        self.action.configure(text="Opened active projects")
        self.projects_textbox.configure(state="normal")
        self.projects_textbox.delete("1.0", tkinter.END)
        for row in os.listdir("data/projects"):
            row = row + "\n"
            self.projects_textbox.insert(tkinter.INSERT, row)
        self.projects_textbox.configure(state="disabled")
        self.active_projects_button.configure(relief="sunken", state="disabled")
        self.done_projects_button.configure(relief="raised", state="normal")
        self.project_add_button.place(x=5, y=250)
        self.project_markdone_button.place(x=71, y=250)
        self.project_markundone_button.place_forget()
        self.project_remove_button.place_forget()

        self.inprogress_textbox.configure(state="normal")
        self.tasks_textbox.configure(state="normal")
        self.done_textbox.configure(state="normal")

        self.tasks_textbox.delete("1.0", tkinter.END)
        self.inprogress_textbox.delete("1.0", tkinter.END)
        self.done_textbox.delete("1.0", tkinter.END)

        self.inprogress_textbox.configure(state="disabled")
        self.tasks_textbox.configure(state="disabled")
        self.done_textbox.configure(state="disabled")

        self.task_add_button.place(x=150, y=250)
        self.task_move_inprogress_button.place(x=216, y=250)
        self.inprogress_move_tasks.place(x=295, y=250)
        self.inprogress_move_done.place(x=361, y=250)
        self.done_move_inprogress.place(x=440, y=250)

    # Done projects button click
    def click_dp(self):
        self.action.configure(text="Opened done projects")
        self.projects_textbox.configure(state="normal")
        self.projects_textbox.delete("1.0", tkinter.END)
        for row in os.listdir("data/done_projects"):
            row = row + "\n"
            self.projects_textbox.insert(tkinter.INSERT, row)
        self.projects_textbox.configure(state="disabled")
        self.active_projects_button.configure(relief="raised", state="normal")
        self.done_projects_button.configure(relief="sunken", state="disabled")
        self.project_add_button.place_forget()
        self.project_markdone_button.place_forget()
        self.project_markundone_button.place(x=5, y=250)
        self.project_remove_button.place(x=71, y=250)

        self.inprogress_textbox.configure(state="normal")
        self.tasks_textbox.configure(state="normal")
        self.done_textbox.configure(state="normal")

        self.tasks_textbox.delete("1.0", tkinter.END)
        self.inprogress_textbox.delete("1.0", tkinter.END)
        self.done_textbox.delete("1.0", tkinter.END)

        self.inprogress_textbox.configure(state="disabled")
        self.tasks_textbox.configure(state="disabled")
        self.done_textbox.configure(state="disabled")

        self.task_add_button.place_forget()
        self.task_move_inprogress_button.place_forget()
        self.inprogress_move_tasks.place_forget()
        self.inprogress_move_done.place_forget()
        self.done_move_inprogress.place_forget()
    
    # Add new project button click
    def click_new_p(self):
    # Open new window that asks new projects name, with ok and cancel buttons
    #    self.projects_textbox.configure(state="normal")
    #    self.add_project_window = tkinter.simpledialog.askstring(parent=self.app, title=None, prompt="New project:")
    #    if self.add_project_window != None:
    #        os.mkdir(path=f"data/projects/{self.add_project_window}")
    #        self.projects_textbox.insert(tkinter.INSERT, self.add_project_window)
    #        self.projects_textbox.delete("1.0", tkinter.END)
    #        for row in os.listdir("data/projects"):
    #            row = row + "\n"
    #            self.projects_textbox.insert(tkinter.INSERT, row)
    #        row = row.replace("\n", "")
    #        self.action.configure(text=f"New project: {row} added")
    #    elif self.add_project_window == None:
    #        self.action.configure(text="Adding new project canceled")
    #    self.projects_textbox.configure(state="disabled")
        self.do = "project"
        self.entrybox.place(x=5, y=285)
        self.entrybox_ok_button.place(x=5, y=310)
        self.entrybox_cancel_button.place(x=85, y=310)
        self.action.configure(text="Adding new project")

    # Ok button click
    def click_ok(self):
        if self.do == "project":
            try:
                if self.entrybox.get() != "":
                    self.projects_textbox.configure(state="normal")
                    os.mkdir(path=f"data/projects/{self.entrybox.get()}")
                    with open (f"data/projects/{self.entrybox.get()}/tasks.txt", "w") as file:
                        pass
                    with open (f"data/projects/{self.entrybox.get()}/inprogress.txt", "w") as file:
                        pass
                    with open (f"data/projects/{self.entrybox.get()}/done.txt", "w") as file:
                        pass
                    self.projects_textbox.insert(tkinter.INSERT, self.entrybox.get())

                    self.entrybox.place_forget()
                    self.entrybox_ok_button.place_forget()
                    self.entrybox_cancel_button.place_forget()
                    self.entrybox.delete(0, "end")
                    self.action.configure(text="New project added")
                    self.do = ""
                elif self.entrybox.get() == "":
                    self.action.configure(text="New project name can't be empty")
            except:
                self.action.configure(text="Project already exists")
            self.projects_textbox.configure(state="disabled")
        
        elif self.do == "task":
            if self.entrybox.get() != "":
                with open (f"data/projects/{self.project}/tasks.txt") as file:
                    task_found = False
                    for row in file:
                        row = row.replace("\n", "")
                        if self.entrybox.get() == row:
                            task_found = True
                            break
                    if task_found == True:
                        self.action.configure(text="Task already exists")
                    elif task_found == False:
                        with open (f"data/projects/{self.project}/tasks.txt", "a") as file:
                            add = f"{self.entrybox.get()}\n"
                            file.write(add)
                        self.tasks_textbox.config(state="normal")
                        self.tasks_textbox.insert(tkinter.INSERT, add)
                        self.tasks_textbox.config(state="disabled")
            
                        self.entrybox.place_forget()
                        self.entrybox_ok_button.place_forget()
                        self.entrybox_cancel_button.place_forget()
                        self.entrybox.delete(0, "end")
                        self.action.configure(text="New task added")
                        self.do = ""
            elif self.entrybox.get() == "":
                self.action.configure(text="New task name can't be empty")

    # Cancel button click
    def click_cancel(self):
        if self.do == "project":
            self.action.configure(text="Adding new project canceled")
        elif self.do == "task":
            self.action.configure(text="Adding new task canceled")
        self.entrybox.place_forget()
        self.entrybox_ok_button.place_forget()
        self.entrybox_cancel_button.place_forget()
        self.entrybox.delete(0, "end")

    # Mark project done button click
    def click_mark_p_d(self):
        try:
            self.projects_textbox.configure(state="normal")
            self.select_project = self.projects_textbox.selection_get()
            os.replace(f"data/projects/{self.select_project}", f"data/done_projects/{self.select_project}")
            self.projects_textbox.delete("1.0", tkinter.END)
            for row in os.listdir("data/projects"):
                row = row + "\n"
                self.projects_textbox.insert(tkinter.INSERT, row)
            self.action.configure(text=f"Project: {self.select_project} moved to done")
            self.projects_textbox.configure(state="disabled")
        except:
            self.action.configure(text="No project selected")
            self.projects_textbox.configure(state="disabled")

    # Not done project button click
    def click_notdone_p(self):
        try:
            self.projects_textbox.configure(state="normal")
            os.replace(f"data/done_projects/{self.projects_textbox.selection_get()}", f"data/projects/{self.select_project}")
            self.projects_textbox.delete("1.0", tkinter.END)
            for row in os.listdir("data/done_projects"):
                row = row + "\n"
                self.projects_textbox.insert(tkinter.INSERT, row)
            self.action.configure(text=f"Project: {self.projects_textbox.selection_get()} moved to active")
            self.projects_textbox.configure(state="disabled")
        except:
            self.action.configure(text="No project selected")
            self.projects_textbox.configure(state="disabled")

    # Remove done project button click
    def click_remove_p(self):
        try:
            self.projects_textbox.configure(state="normal")
            os.rmdir(f"data/done_projects/{self.projects_textbox.selection_get()}")
            self.projects_textbox.delete("1.0", tkinter.END)
            for row in os.listdir("data/done_projects"):
                row = row + "\n"
                self.projects_textbox.insert(tkinter.INSERT, row)
            self.action.configure(text=f"Project: {self.projects_textbox.selection_get()} deleted")
            self.projects_textbox.configure(state="disabled")
        except:
            self.action.configure(text="No project selected")
            self.projects_textbox.configure(state="disabled")
    
    # Add task button click
    def click_add_task(self):
        if self.project != "":
            self.do = "task"
            self.entrybox.place(x=5, y=285)
            self.entrybox_ok_button.place(x=5, y=310)
            self.entrybox_cancel_button.place(x=85, y=310)
            self.action.configure(text=f"Adding new task to {self.project}")
        elif self.project == "":
            self.action.configure(text="No project selected")

    # Select task with single click 1/2
    def select_task_line(self, event=None):
        self.tasks_textbox.tag_add("sel", "insert linestart", "insert lineend")
        self.tasks_textbox.tag_configure("sel", background="black")
        try:
            with open (f"data/projects/{self.project}/tasks.txt") as file:
                texts = file.read()
                if self.tasks_textbox.selection_get() in texts:
                    self.task = self.tasks_textbox.selection_get()
                    self.task_move_inprogress_button.configure(state="normal")
                    self.inprogress_move_tasks.configure(state="disabled")
                    self.action.configure(text=f"Task '{self.tasks_textbox.selection_get()}' selected")
                else:
                    self.action.configure(text="Clicked on empty spot on task window")
        except:
            self.task = ""
            self.task_move_inprogress_button.configure(state="disabled")
            self.action.configure(text="Clicked on empty spot on task window")
    def select_inprogress_line(self, event=None):
        self.inprogress_textbox.tag_add("sel", "insert linestart", "insert lineend")
        self.inprogress_textbox.tag_configure("sel", background="black")
        self.action.configure(text=f"In progress task '{self.inprogress_textbox.selection_get()}' selected")
        self.task = self.inprogress_textbox.selection_get()
        
        self.task_move_inprogress_button.configure(state="disabled")
        self.inprogress_move_tasks.configure(state="normal")
    def select_done_line(self, event=None):
        self.done_textbox.tag_add("sel", "insert linestart", "insert lineend")
        self.done_textbox.tag_configure("sel", background="black")
        self.action.configure(text=f"Done task '{self.done_textbox.selection_get()}' selected")
        self.task = self.done_textbox.selection_get()

    # Move tasks to in progress button
    def click_task_to_inprog(self):
        if self.task != "" and self.project != "":
            self.tasks_textbox.configure(state="normal")
            self.inprogress_textbox.configure(state="normal")
            with open (f"data/projects/{self.project}/inprogress.txt", "a") as file:
                file.write(f"{self.task} - {self.username}\n")
            with open (f"data/projects/{self.project}/tasks.txt") as file:
                content = file.read()
                update = content.replace(self.task, "")
            with open (f"data/projects/{self.project}/tasks.txt", "w") as file:
                file.write(update)
            rows =[]
            with open (f"data/projects/{self.project}/tasks.txt") as file:
                for row in file:
                    if row != "\n":
                        rows.append(row)
            with open (f"data/projects/{self.project}/tasks.txt", "w") as file:
                for row in rows:
                    file.write(row)
            self.tasks_textbox.delete("0.0", "end")
            self.inprogress_textbox.delete("0.0", "end")
            with open (f"data/projects/{self.project}/tasks.txt") as file:
                tasks = file.read()
                self.tasks_textbox.insert("0.0", tasks)
            with open (f"data/projects/{self.project}/inprogress.txt") as file:
                inprogress = file.read()
                self.inprogress_textbox.insert("0.0", inprogress)

            self.tasks_textbox.configure(state="disabled")
            self.inprogress_textbox.configure(state="disabled")
            self.action.configure(text=f"Task {self.task} moved to in progress")
            self.task = ""
        elif self.task == "" or self.project == "":
            self.action.configure(text="No project or task selected")


    # Move in progress to tasks button
    def click_inprog_to_task(self):
        print("inprogress to task")
    # move in progress to done button
    def click_inprog_to_done(self):
        print("inprogress to done")
    # move done to in progress button
    def click_done_to_inprog(self):
        print("done to inprogress")

    # Logout button click
    def click_logout(self):
        self.username = ""
        self.active_user.configure(text="")
        self.action.configure(text="User logged out")
        
        self.hide_projects()
        self.show_login()

    # Hide app elements, when going back to login screen
    def hide_projects(self):
        self.active_projects_button.place_forget()
        self.done_projects_button.place_forget()
        self.projects_label.place_forget()
        self.projects_textbox.place_forget()
        self.project_add_button.place_forget()
        self.project_markdone_button.place_forget()

        self.entrybox.place_forget()
        self.entrybox_ok_button.place_forget()
        self.entrybox_cancel_button.place_forget()

        self.tasks_label.place_forget()
        self.tasks_textbox.place_forget()
        self.task_add_button.place_forget()
        self.task_move_inprogress_button.place_forget()

        self.inprogress_label.place_forget()
        self.inprogress_textbox.place_forget()
        self.inprogress_move_tasks.place_forget()
        self.inprogress_move_done.place_forget()

        self.done_label.place_forget()
        self.done_textbox.place_forget()
        self.done_move_inprogress.place_forget()

        self.logout_button.place_forget()

    # Show app elements, when logging in
    def show_projects(self):
        self.active_projects_button.place(x=24, y=25)
        self.done_projects_button.place(x=71, y=25)
        self.projects_label.place(x=25, y=50)
        self.projects_textbox.place(x=5, y=80)
        self.project_add_button.place(x=5, y=250)
        self.project_markdone_button.place(x=71, y=250)

        self.tasks_label.place(x=185, y=50)
        self.tasks_textbox.place(x=150, y=80)
        self.task_add_button.place(x=150, y=250)
        self.task_move_inprogress_button.place(x=216, y=250)

        self.inprogress_label.place(x=300, y=50)
        self.inprogress_textbox.place(x=295, y=80)
        self.inprogress_move_tasks.place(x=295, y=250)
        self.inprogress_move_done.place(x=361, y=250)

        self.done_label.place(x=475, y=50)
        self.done_textbox.place(x=440, y=80)
        self.done_move_inprogress.place(x=440, y=250)

        self.logout_button.place(x=515, y=5)

    # Hide login ui
    def hide_login(self):
        self.user_label.place_forget()
        self.user_entry.delete(0, "end")
        self.user_entry.place_forget()
        self.passw_label.place_forget()
        self.passw_entry.delete(0, "end")
        self.passw_entry.place_forget()
        self.login_button.place_forget()
        self.add_new_user_button.place_forget()

    # Show login ui
    def show_login(self):
        self.user_label.place(x=5, y=25)
        self.user_entry.place(x=70, y=25)
        self.passw_label.place(x=5, y=50)
        self.passw_entry.place(x=70, y=50)
        self.login_button.place(x=70, y=80)
        self.add_new_user_button.place(x=135, y=80)

# App Frame
app = tkinter.Tk()
app.geometry("570x350")         # App window size
app.title("Project Manager")    # Title bar text
dark_title_bar(app)             # Dark title bar
app.configure(bg="#2e2e2e")     # Dark window background

# UI
UI(app)

app.bind_all("<Button>", UI.change_focus)   # Button click does change_focus function

# Run App
app.mainloop()