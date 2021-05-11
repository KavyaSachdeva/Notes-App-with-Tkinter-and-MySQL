from tkinter import *
import mysql.connector
from tkinter import messagebox
from datetime import datetime


root = Tk()
root.title("HomePage")

root.configure(bg='#145660')
root.geometry('800x600')
root.resizable(False, False)
l = Label(root, text='MyNotes', height='2',
          bg='#145660', fg='white', font=("Times", "24", "bold italic"))
l.place(x=300, y=0)
noteid = 0
rno = 0
####################################LISTBOX###########################################################
f1 = Frame(root, bg='green')
f1.place(x=120, y=200, height=250, width=500)

scroll_bar = Scrollbar(f1)

scroll_bar.pack(side=RIGHT,
                fill=Y)

r = Listbox(f1, height=20, width=110, bg='white', yscrollcommand=scroll_bar.set,
            fg='black', font=('Helvetica', 7, 'italic'))

r.pack()
scroll_bar.config(command=r.yview)

##################################### CONNECTION ######################################################

con = mysql.connector.connect(host='localhost',
                              user='root',
                              password='admin',
                              database='mynotes',
                              port=3307)

c = con.cursor()
#####################################MAKE TABLE#######################################################
#c.execute('CREATE DATABASE MYNOTES')
c.execute('CREATE TABLE IF NOT EXISTS Noteskavya (note_id int AUTO_INCREMENT PRIMARY KEY , title varchar(20),content varchar(100), date_published date);')

titles = []


def showlist():
    c.execute("SELECT * FROM noteskavya;")
    r.delete("0", "end")
    for row in c:
        # print(row)
        r.insert(1, row[1])


showlist()

##################################### ADD NOTES ######################################################


def addnote():
    root = Tk()
    root.geometry('600x400')
    root.title('Add Note')
    root.configure(bg='#145660')
    root.resizable(False, False)
    l = Label(root, text='Enter Note Title', height='2',
              bg='#145660', fg='white', font=("Times", "15", "bold italic"))
    l.place(x=100, y=0)
    entry_title = Entry(root)
    entry_title.grid(row=0, column=2, pady=15)
    entry_title.place(x=300, y=20)

    l = Label(root, text='Write Note Here', height='2',
              bg='#145660', fg='white', font=("Times", "15", "bold italic"))
    l.place(x=100, y=100)
    entry_add = Entry(root)
    entry_add.grid(row=2, column=2, pady=15)
    entry_add.place(x=300, y=120, height=100)

    def submit():
        date = '12/04/21'
        title_name = entry_title.get()
        content = entry_add.get()
        data_user = (title_name, content, date)
        r.insert(rno, title_name)
        # rno += 1
        # add note titles in listbox
        add_user = 'INSERT INTO noteskavya (title, content, date_published) VALUES (%s, %s, %s);'
        c.execute(add_user, data_user)

        con.commit()

    sub_button = Button(root, text="Add Note", command=submit)
    sub_button.place(x=250, y=300)


button1 = Button(root, text='Add new note', command=addnote)
button1.place(x=100, y=150)

##################################### EDIT NOTES ######################################################


def fileSelection(temp):                    # DOUBLE CLICK FOR PRINT TITLE IN LISTBOX
    global old_title
    selection = r.curselection()
    for i in selection:
        print(r.get(i))
        old_title = r.get(i)
        return old_title


def editnote():
    global old_title
    root = Tk()
    root.geometry('600x400')
    root.title('Edit Note')
    root.configure(bg='#145660')
    root.resizable(False, False)
    l = Label(root, text='Enter New Title', height='2',
              bg='#145660', fg='white', font=("Times", "15", "bold italic"))
    l.place(x=100, y=0)
    entry_title = Entry(root)
    entry_title.grid(row=0, column=2, pady=15)
    entry_title.place(x=300, y=20)

    l = Label(root, text='Write Note Here', height='2',
              bg='#145660', fg='white', font=("Times", "15", "bold italic"))
    l.place(x=100, y=100)
    entry_add = Entry(root)
    entry_add.grid(row=2, column=2, pady=15)
    entry_add.place(x=300, y=120, height=100)

    def submit():
        global old_title
        date = '12/04/21'
        title = entry_title.get()
        content = entry_add.get()
        data_user = (title, content, date, old_title)
        add_user = 'UPDATE noteskavya SET title= %s, content=%s, date_published=%s WHERE title = %s;'
        c.execute(add_user, data_user)
        con.commit()

    sub_button = Button(root, text="Update Changes", command=submit)
    sub_button.place(x=250, y=300)


button2 = Button(root, text='Edit note', command=editnote)
button2.place(x=350, y=150)

##################################### DELETE NOTES ######################################################


def delnote():
    global old_title
    q = """DELETE FROM noteskavya WHERE title=%s"""
    c.execute(q, (old_title,))

    con.commit()
    showlist()


button3 = Button(root, text='Delete note', command=delnote)
button3.place(x=600, y=150)


r.bind("<Button-1>", fileSelection)


print(con)


root.mainloop()


# UPDATE STATEMENT USING NOTEID OR TITLE
# CONNECTION AT THE TOP
# DELETE BUTTON--> LISTBOX SHOWING ACTIVE NOTES
