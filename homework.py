# AMDG
import sqlite3
from tkinter import *
import tkinter.font as tkFont
from datetime import datetime

# Tkinter
root = Tk()
root.title('Homework Tracker')
root.geometry('635x780')


#FONT LIST https://www.delftstack.com/howto/python-tkinter/how-to-set-font-of-tkinter-text-widget/
main_font = tkFont.Font(
    family = "Trebuchet MS",
    size = 11
)

track_font = tkFont.Font(
    family = "Ink Free",
    size = 13,
    weight='bold'
)

alt_font = tkFont.Font(
    family = "SimSun-ExtB",
    size = 10
)

#FRAMES
main_frame = Frame(root,highlightbackground='black',highlightthickness=2,bg="#a3caa8")
main_frame.grid(row=0,column=0,sticky='nw',padx=30,pady=30)

delete_frame = Frame(root,highlightbackground='black',highlightthickness=2,bg="#a3caa8",width=250,height=20)
delete_frame.grid(row=0,column=1,sticky='nws',padx=(0,30),pady=30)
delete_frame.grid_propagate(False)

tracker_frame = Frame(root,highlightbackground='black',highlightthickness=2,bg="#a3caa8")
tracker_frame.grid(row=1,column=0,sticky='nw',padx=30,pady=(0,30))

progress_frame = Frame(root,highlightbackground='black',highlightthickness=2,bg="#a3caa8",width=280,height=20)
progress_frame.grid(row=1,column=1,sticky='nws',padx=(0,30),pady=(0,30))
progress_frame.grid_propagate(False)

#DATABASE SETUP
conn = sqlite3.connect('homework_tracker.db')
cursor = conn.cursor()

'''
cursor.execute("""CREATE TABLE homework (
    student_name text,
    student_id text,
    assignment_name text,
    assignment_progress text,
    due_date text
    )""")
'''

#FUNCTIONS

# updates database
def update():
    conn = sqlite3.connect('homework_tracker.db')
    cursor = conn.cursor()

    try:
        date_obj = datetime.strptime(due_date.get().strip(), '%m/%d/%Y').date()
        
        cursor.execute("INSERT INTO homework VALUES (?,?,?,?,?)",(
            student_name.get(),
            student_id.get(),
            assignment_name.get(),
            0,
            due_date.get().strip()
        ))

        student_name.delete(0,END)
        student_id.delete(0,END)
        assignment_name.delete(0,END)
        due_date.delete(0,END)

        date_error.configure(text='Success!')
    except ValueError:
        date_error.configure(text='Invalid date!')

    conn.commit()
    conn.close()

    show_2()

# shows assignments when program runs
def show_1():
    conn = sqlite3.connect('homework_tracker.db')
    cursor = conn.cursor()

    cursor.execute("SELECT *, oid FROM homework")

    assignments = cursor.fetchall()

    all_assignments = ''

    for assignment in assignments:
        all_assignments += "----------------------------\n"
        all_assignments += "Student: " + assignment[0] + "\n"
        all_assignments += "ID: " + assignment[1] + "\n"
        all_assignments += "Assignment: " + assignment[2] + "\n"
        all_assignments += "Progress: " + assignment[3] + "%" + "\n"
        all_assignments += "Due: " + assignment[4] + "\n"
        all_assignments += "Assignment No. " + str(assignment[5]) + "\n"

    conn.commit()
    conn.close()

    return all_assignments

# shows assignments after any changes to database
def show_2():
    conn = sqlite3.connect('homework_tracker.db')
    cursor = conn.cursor()

    assignment_list.configure(state='normal')

    cursor.execute("SELECT *, oid FROM homework")

    assignments = cursor.fetchall()

    assignment_list.delete('1.0',END)

    all_assignments = ''

    for assignment in assignments:
        all_assignments += "----------------------------\n"
        all_assignments += "Student: " + assignment[0] + "\n"
        all_assignments += "ID: " + assignment[1] + "\n"
        all_assignments += "Assignment: " + assignment[2] + "\n"
        all_assignments += "Progress: " + assignment[3] + "%" + "\n"
        all_assignments += "Due: " + assignment[4] + "\n"
        all_assignments += "Assignment No. " + str(assignment[5]) + "\n"

    assignment_list.tag_configure('tag',justify='center')
    assignment_list.insert(END,all_assignments)
    assignment_list.tag_add('tag','1.0',END)
    assignment_list.configure(state='disabled')

    conn.commit()
    conn.close()

# deletes an assignment from database
def delete():
    conn = sqlite3.connect('homework_tracker.db')
    cursor = conn.cursor()

    cursor.execute("SELECT *,oid FROM homework")

    all = cursor.fetchall()
    all_oid = []

    for item in all:
        all_oid.append(item[5])

    try:
        if int(delete_entry.get()) and int(delete_entry.get()) in all_oid: 
            cursor.execute("DELETE from homework WHERE oid =" + delete_entry.get())
            delete_entry.delete(0,END)
            delete_error.configure(text="Nice!")
        else:
            delete_error.configure(text="No assignment\nnumber found")
    except ValueError:
        delete_error.configure(text="Invalid input!")

    conn.commit()
    conn.close()
    show_2()

# updates assignment progress
def progress_check():
    conn = sqlite3.connect('homework_tracker.db')
    cursor = conn.cursor()

    cursor.execute("SELECT *,oid FROM homework")

    all = cursor.fetchall()
    all_oid = [item[5] for item in all]
    
    try:
        if int(assignment_to_update.get()) in all_oid:
            if float(progress_update.get()) and float(progress_update.get()) < 100:
                cursor.execute("UPDATE homework SET assignment_progress = ? WHERE oid = ?",(
                    progress_update.get(),
                    assignment_to_update.get()
                ))
                progress_update.delete(0,END)
                assignment_to_update.delete(0,END)
                progress_error.configure(text='Success!')
            elif float(progress_update.get()) and float(progress_update.get()) == 100:
                cursor.execute("DELETE from homework WHERE oid=" + assignment_to_update.get())
                progress_update.delete(0,END)
                assignment_to_update.delete(0,END)
                progress_error.configure(text='Good job!')            
            else:
                progress_error.configure(text="New Progress should\nbe between 0-100!")
        else:
            progress_error.configure(text="No assignment number found")
    except ValueError:
        progress_error.configure(text="Invalid input!")

    conn.commit()
    conn.close()
    show_2()

# clears database
def destruction():
    conn = sqlite3.connect('homework_tracker.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM homework")

    conn.commit()
    conn.close()
    show_2()

    date_error.configure(text="Cleared!")

#ENTRIES
student_name = Entry(main_frame)
student_name.grid(row=0, column=1, pady = 10,padx=(0,20))

student_id = Entry(main_frame)
student_id.grid(row=1, column=1, pady = 10,padx=(0,20))

assignment_name = Entry(main_frame)
assignment_name.grid(row = 2, column = 1, pady = 10,padx=(0,20))

due_date = Entry(main_frame)
due_date.grid(row=3, column = 1, pady = 10, padx=(0,20))

progress_update = Entry(progress_frame)
progress_update.grid(row=0,column=1,pady=10,padx=(0,20))

assignment_to_update = Entry(progress_frame)
assignment_to_update.grid(row=1,column=1,pady=(0,10),padx=(0,20))

#LABELS
student_name_label = Label(main_frame, text = "Student Name", padx = 10,font=main_font,bg="#a3caa8")
student_name_label.grid(row = 0, column = 0)

student_id_label = Label(main_frame, text = "Student ID",font=main_font,bg="#a3caa8")
student_id_label.grid(row = 1, column = 0)

assignment_name_label = Label(main_frame, text = "Assignment",font=main_font,bg="#a3caa8")
assignment_name_label.grid(row = 2, column = 0)

due_date_label = Label(main_frame, text = "Due date\nmm/dd/yyyy",font=main_font,bg="#a3caa8")
due_date_label.grid(row = 3, column = 0)

progress_update_label = Label(progress_frame,text = "New Progress %\n(enter number)",font=main_font,bg="#a3caa8")
progress_update_label.grid(row=0,column=0, padx=10,pady=10)

assignment_to_update_label = Label(progress_frame,text="Assignment\nNo.",font=main_font,bg="#a3caa8")
assignment_to_update_label.grid(row=1,column=0,padx=10,pady=(0,10))

#TRACKER TEXT
assignment_list = Text(tracker_frame,font=main_font,pady=10,padx=10,height=18,width=30,bg="#FFFFD2")
assignment_list.insert(END,show_1())
assignment_list.tag_configure('tag',justify='center',font=track_font)
assignment_list.tag_add('tag','1.0',END)
assignment_list.configure(state='disabled')
assignment_list.grid()

#BUTTONS
add_button = Button(main_frame,text="Add Assignment",font=main_font,command=update,bg="#6cbd76")
add_button.grid(row=4,column=0,columnspan=2,pady=10)

clear_button = Button(main_frame,text="Clear All",font=main_font,command=destruction,bg="#6cbd76")
clear_button.grid(row=5,column=0,columnspan=2,pady=10)

progress_button = Button(progress_frame,text='Change',font=main_font,command=progress_check,bg="#6cbd76")
progress_button.grid(columnspan=2,row=2,column=0,ipadx=30,pady=(0,10))

#DELETING
delete_label = Label(delete_frame,text="Assignment\nNo.",font=main_font,bg="#a3caa8")
delete_label.grid(row=0,column=0,pady=10,padx=10)

delete_button = Button(delete_frame, text = "Finished",font=main_font,command=delete,bg="#6cbd76")
delete_button.grid(columnspan=2,row=1,column=0,ipadx=40,pady=(0,10))

delete_entry = Entry(delete_frame)
delete_entry.grid(row=0,column=1,padx=(0,20))

#ERRORS
progress_error = Label(progress_frame,text='',font=alt_font,bg="#a3caa8")
progress_error.grid(row=4,column=0,padx=20,columnspan=2)

delete_error = Label(delete_frame,text='',font=alt_font,bg="#a3caa8")
delete_error.grid(row=3,column=0,padx=20,columnspan=2)

date_error = Label(main_frame,text='',font=alt_font,bg="#a3caa8")
date_error.grid(row=6,column=0,padx=20,columnspan=2,pady=(0,10))

root.rowconfigure(0,weight=0)
root.columnconfigure(0,weight=0)

root.resizable(False, False)

root.mainloop()