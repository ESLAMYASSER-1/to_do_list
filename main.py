import tkinter as tk 
from tkinter.messagebox import showinfo,askyesno
from tkinter.font import Font
from tkcalendar import DateEntry
from datetime import date
import mysql.connector 

# ##########################################################################
# ##########################################################################
                    # start the database 


def createDB():
    conn = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='engeslam@8505611.mysql',
    )
    mycursor = conn.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS TASKS;")

createDB()

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='engeslam@8505611.mysql',
    database='TASKS'
)

mycursor = conn.cursor()
mycursor.execute("create table if not exists tasks(task_id int , task_text varchar(255),task_date date, task_state bool)AUTO_INCREMENT=1;")
def insert_task(task_id,task_text,task_date,task_state):
    sql_statment="insert into tasks values('%i','%s','%s',%i)"% (task_id,task_text,task_date,task_state)
    mycursor.execute(sql_statment)
    conn.commit()
def update_task(task_state,task_id,task_date,tasks_to_update):
    sql_statement="UPDATE tasks set task_state = %i WHERE task_id = %i AND task_date = %s ;"%(task_state,task_id,task_date)
    mycursor.executemany(sql_statement,tasks_to_update)
    conn.commit()
def remove_task(task_text,task_date):
    
        sql_statement="DELETE from tasks where task_text = '%s' and task_date= '%s';"%(task_text,task_date)
        mycursor.execute(sql_statement)
        conn.commit()
    
# ##########################################################################
# get date time 
current_date = date.today()
current_year=int(current_date.year)
current_month=int(current_date.month)
current_day=int(current_date.day)
# ##########################################################################

root = tk.Tk()
root.geometry("530x870")
root.title("TO DO List")
root.iconbitmap("res\icon.ico")

my_font = Font(
    family = 'Times',
    size = 25,
    weight = 'bold',
    slant = 'roman',
    underline = 0,
    overstrike = 0
)


class Tasks:
    tasks = []
    checkbox_vars=[]
    popup=0
    def __init__(self,task_date):
        
        self.task_date=task_date
        def taskstoarr():
            sql_statement="SELECT * FROM tasks WHERE task_date = '%s'"% self.task_date
            mycursor.execute(sql_statement)
            res= mycursor.fetchall()
            Tasks.tasks.clear()
            for r in res:
                Tasks.tasks.append(r)
        taskstoarr()
        for task in Tasks.tasks:
            Tasks.addframe(task[1])
    def remove_parent(widget):
        answer = askyesno("REMOVE TASK?","REMOVE TASK? \n if yes no redo.")
        if answer:
            print(widget.winfo_children()[-1].cget("text"))
            print(cal.get_date())
            remove_task(widget.winfo_children()[-1].cget("text"),cal.get_date())
            widget.destroy()
        else:
            pass
        
    def addframe(tasktxt):
        var = tk.BooleanVar()
        if len(Tasks.tasks)>5:
            showinfo("max number of tasks","cant add more that 5 tasks")
        else:
            Task_frame=tk.Frame(Tasksframe,bg="#03abf9",width=510,height=110)
            Task_frame.pack(padx=10,pady=10,expand="yes",fill="x")
            Task_frame.pack_propagate(0)
            leftframe=tk.Frame(Task_frame,width=100,height=110,bg="#03abf9",)   
            leftframe.pack(side=tk.LEFT)
            leftframe.pack_propagate(0)
            statecheck= tk.Checkbutton(leftframe,bg="#211290",fg="green",variable=var)
            statecheck.pack(padx=10,pady=20,expand="yes")
            statecheck.bind("<Button-1>",Tasks.on_checkbox_click)
            Tasks.checkbox_vars.append(var)
            removebtn = tk.Button(Task_frame,text="X",command=lambda: Tasks.remove_parent(Task_frame))
            removebtn.place(x=480,y=80)
            tasktext = tk.Label(Task_frame, text=tasktxt,font="Verdana 13",wraplength=400,bg="#03abf9",)
            tasktext.pack(side=tk.LEFT)
            if len(Tasks.checkbox_vars)>len(Tasks.tasks):
                Tasks.checkbox_vars=Tasks.checkbox_vars[:len(Tasks.tasks)+1]
    def difference (list1, list2):
        list_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
        return list_dif
    def on_checkbox_click(event):
        for [i,var],x in zip(enumerate(Tasks.checkbox_vars),Tasks.tasks):
            print(Tasks.difference([int(var.get()),i,cal.get_date()],x))
    
    def get_text(x):
        text = x
        if len(Tasks.tasks)<5:
            insert_task(len(Tasks.tasks),f'{text.strip()}',f'{cal.get_date()}',0)
            for widget in Tasksframe.winfo_children():
                widget.destroy()
                Tasks.tasks.clear()
            Tasks(cal.get_date())
        else:
            showinfo("max number of tasks","cant add more that 5 tasks")
    def open_popup():
        popup = tk.Toplevel(root)
        popup.geometry("570x300")
        popup.title("Add Task")
        pframe = tk.Frame(popup,bg="#1f07d8",width=570,height=300)
        pframe.pack()
        taskdatelbl=tk.Label(pframe,text="DATE:  ",font="verdana 13 bold",bg="#1f07d8",fg="#0bee21")
        taskdatelbl.place(x=20,y=20)
        taskdate = tk.Label(pframe,text=cal.get_date(),bg="#1f07d8",fg="#0bee21",font="verdana 13 bold") 
        taskdate.place(x=80,y=20)
        task_textlbl=tk.Label(pframe,text="Task: ",bg="#1f07d8",fg="#0bee21",font="verdana 13 bold",)
        task_textlbl.place(x=20,y=80)
        task_text=tk.Text(pframe,bg="#211290",fg="white",font="verdana 15 bold",width=30,wrap="word")#211290
        task_text.place(x=90,y=90,height=120)
        def x ():
            Tasks.get_text(task_text.get("1.0",tk.END))
            popup.destroy()
        savebtn = tk.Button(pframe,width=10,height=2,text="SAVE",command=x )
        savebtn.place(x=460,y=240)
        try:
            return task_text.get()
        except:
            pass




#Create main frame to include main items 
Fullframe = tk.Frame(root , bg="#03abf9",width=530,height=870)
Fullframe.pack()

TOlabel= tk.Label(Fullframe,text="TO", fg="#e93333" ,bg="#03abf9",font=my_font )
TOlabel.place(x=290,y=10)
DOlabel= tk.Label(Fullframe, text="DO", fg="#e81acd",bg="#03abf9",font=my_font)
DOlabel.place(x=345,y=10)
LISTlabel=tk.Label(Fullframe,text="LIST", fg="#0ea438",bg="#03abf9",font=my_font)
LISTlabel.place(x=400,y=10)



# create calender date entry 
def date_selected(event):
    date = event.widget.get_date()
    for widget in Tasksframe.winfo_children():
        widget.destroy()
        Tasks.tasks.clear()
    Tasks.checkbox_vars.clear()
    Tasks(date)
cal = DateEntry(root, width=10,height=30,font=("Arial",15), year=current_year, month=current_month, day=current_day, locale='en_US', date_pattern='yyyy/MM/DD',background='darkblue', foreground='white', borderwidth=2)
cal.place(x=40,y=20)
cal.bind("<<DateEntrySelected>>", date_selected)
##########################################################################
##########################################################################

Tasksframe= tk.Frame(Fullframe,width=530, height=670,bg="#03abf9")

Tasksframe.place(x=0,y=100,)

# ##########################################################################
# ##########################################################################







# create ADD TASK BUTTON 
ADDTASKbtn = tk.Button(Fullframe,text="ADD TASK",font=("Arial",15,"bold"),bg="blue",fg="#01ec5f",command=Tasks.open_popup)
ADDTASKbtn.place(x=370,y=790)



# ##########################################################################
# ##########################################################################


Tasks(f"{current_year}-{current_month}-{current_day}")

root.mainloop()