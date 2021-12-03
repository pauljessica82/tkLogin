from tkinter import *
from tkinter import messagebox as mb
import sqlite3

with sqlite3.connect('userdata.db') as db:
    cur = db.cursor()

sql_create_user_table = ("""CREATE TABLE IF NOT EXISTS user (
               username TEXT NOT NULL,
               password TEXT NOT NULL);
""")

sql_create_msg_table = ("""CREATE TABLE IF NOT EXISTS messages (
               username TEXT NOT NULL,
               message TEXT );
""")

cur.execute(sql_create_msg_table)
cur.execute(sql_create_user_table)
db.execute('SELECT * FROM user')
db.commit()
db.close()


class main():
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.my_text = StringVar()
        self.widgets()

    def widgets(self):
        self.head = Label(self.master, text=" LOGIN ", font=('freesansbold', 35), pady=40)
        self.head.pack()

        self.logf = Frame(self.master, padx=10, pady=10)
        Label(self.logf, text=" Username: ", font=('freesanbold', 20), padx=5, pady=5).grid(sticky=W)
        # The Entry widget is used to provide the single line text-box to the user to accept a value from the user.
        Entry(self.logf, textvariable=self.username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.logf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.logf, text=' Login ', bd=3, font=('', 15), padx=5, pady=5, command=self.login).grid()
        Button(self.logf, text=' Create Account ', bd=3, font=('', 15), padx=5, pady=5, command=self.cr).grid(row=2,
                                                                                                              column=1)
        self.logf.pack()

        self.crf = Frame(self.master, padx=10, pady=10)
        Label(self.crf, text='Username: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.crf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.crf, text='Create Account', bd=3, font=('', 15), padx=5, pady=5, command=self.new_user).grid()
        Button(self.crf, text='Go to Login', bd=3, font=('', 15), padx=5, pady=5, command=self.log).grid(row=2,
                                                                                                         column=1)

        self.my_text = Text(self.master, width=40, height=10, font=('Times', 14))
        self.button_frame = Frame(self.master, padx=10, pady=10)
        Button(self.button_frame, text="Clear Screen", padx=5, pady=5, command=self.clear_msg).grid(row=0, column=0)
        Button(self.button_frame, text="Save Text", padx=5, pady=5, command=self.save_msg).grid(row=0, column=2)
        Button(self.button_frame, text="Show My Messages", padx=5, pady=5,
               command=self.show_all_messages).grid(row=0, column=4)
        Button(self.button_frame, text="Logout", padx=5, pady=5, command=self.log).grid(row=0, column=6)

    def clear_msg(self):
        self.my_text.delete(1.0, END)

    def save_msg(self):
        with sqlite3.connect('userdata.db') as db:
            cur = db.cursor()
            mb.showinfo("Success!!", "Message Saved")
            username = self.username.get()
            print(username)
            insert_msg = "INSERT INTO messages(username, message) VALUES (?,?) ;"
            cur.execute(insert_msg, [username, (self.my_text.get(1.0, END))])
            db.commit()

    def login(self):
        with sqlite3.connect('userdata.db') as db:
            cur = db.cursor()
        sqlite3.connect('userdata.db')
        find_user = 'SELECT * FROM user WHERE username = ? AND password = ?;'
        cur.execute(find_user, [(self.username.get()), (self.password.get())])
        results = cur.fetchall()
        if not (self.username.get() and self.password.get()):
            mb.showerror("Error!!", " You are missing one or more fields ")
        elif results:
            self.logf.pack_forget()
            # have a message box show
            self.head["text"] = '\n Welcome, ' + self.username.get()
            self.head["pady"] = 20
            self.my_text.pack(pady=20)
            self.button_frame.pack()
        else:
            mb.showerror("Oops!!", "Invalid Credentials!")

    def show_all_messages(self):
        with sqlite3.connect('userdata.db') as db:
            cur = db.cursor()
        sql = "SELECT message FROM messages WHERE username = ? "
        records = cur.execute(sql, (self.username.get(),)).fetchall()
        print_records = ''
        for record in records:
            print_records += str(record[0]) + "\n"
        self.sql_label = Label(root, text=print_records)
        self.sql_label.pack(pady=40)

        db.commit()

    def new_user(self):
        with sqlite3.connect('userdata.db') as db:
            cur = db.cursor()
        find_user = 'SELECT * FROM user WHERE username = ?;'
        cur.execute(find_user, [(self.n_username.get())])
        if not (self.n_username.get() and self.n_password.get()):
            mb.showerror("Error!!", " Username and Password cant be empty ")
        elif cur.fetchall():
            mb.showerror("Error!!", "Username Taken. Please try a different one.")
        else:
            mb.showinfo("Success!!", "Account Created")
            self.log()
            insert = 'INSERT INTO user(username, password) VALUES(?,?);'
            cur.execute(insert, [(self.n_username.get()), (self.n_password.get())])
            db.commit()

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.my_text.pack_forget()
        self.button_frame.pack_forget()
        self.sql_label.pack_forget()
        self.head['text'] = " LOGIN "
        self.logf.pack()

    def cr(self):
        self.logf.pack_forget()
        self.head['text'] = " Create New Account "
        self.crf.pack()


# if __name__ == "__main__":
#     app.run(debug=True)


root = Tk()
main(root)
root.geometry("500x500")
root.mainloop()
