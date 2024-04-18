from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import string
import random
from cryptography.fernet import Fernet
import os
import sqlite3

#configration
bg_color = "#2A2A2A"
frame_bg_color = "#1F1F1F"
label_fg_color = "cyan"
btn_fg_color = "cyan"
btn_bg_color = "#1F1F1F"
entry_bg_color = "#1F1F1F"
entry_fg_color = "red"

#functions

def create_db(userid,userid_key,password,password_key):
    try:
        os.chdir("Assets\\Data")
    except FileNotFoundError:
        os.mkdir("Assets\\Data")
        os.chdir("Assets\\Data")

    conn = sqlite3.connect('vault.db')
    cursor = conn.cursor()  
    table ="""CREATE TABLE IF NOT EXISTS VAULT(USERID BLOB, USERID_KEY BLOB, PASSWORD BLOB, PASSWORD_KEY BLOB);"""
    cursor.execute(table)   

    unique_index_query = """CREATE UNIQUE INDEX IF NOT EXISTS idx_link_username_password_key ON VAULT(userid,password);"""
    cursor.execute(unique_index_query)  
    # Queries to INSERT records.
    cursor.execute('''INSERT OR REPLACE INTO VAULT VALUES (?,?,?,?)''',(userid,userid_key,password,password_key))
    conn.commit()   
    # Closing the connection
    conn.close()

    os.chdir("..\\..")


def encrypt_data(data):
    data = data.encode()
    key = Fernet.generate_key()
    f = Fernet(key)
    enc_data = f.encrypt(data)
    return enc_data,key

def newwin():
    def handle_save(e):
        save_data()

    def save_data():
        userid = win_userid_var.get()
        password = win_password_var.get()

        if userid == "" or password == "":
            messagebox.showerror("Error","Invalid userid or password!")
            return None

        enc_userid,userid_key = encrypt_data(userid)
        enc_password,password_key = encrypt_data(password)

        create_db(enc_userid,userid_key,enc_password,password_key)
        messagebox.showinfo("Success","Your data is stored inside the database!")


    def set_password():
        password = gen_pass()
        win_password_var.set(value=password)

    def gen_pass():
        keys = []
        password_key = []
        len = win_passlen_var.get()
        digits = string.digits
        uppers = string.ascii_uppercase
        lowers = string.ascii_lowercase
        punctuations = "!@#$%^&*"
        for punctuation in punctuations:
            keys.append(punctuation)
        for digit in digits:
            keys.append(digit)
        for upper in uppers:
            keys.append(upper)
        for lower in lowers:
            keys.append(lower)
        
        random.shuffle(keys)
        
        for i in range(len):
            char = random.choice(keys)
            password_key.append(char)
            
        password = "".join(password_key)
        return password
            
    def decrypt_data(enc_data,key):
        f = Fernet(key)
        data = f.decrypt(enc_data).decode()
        return data


        
    def showpasswin():
        def show_passwords():
            try:
                os.chdir("Assets\\Data")
            except FileNotFoundError:
                messagebox.showerror("Error","Assets\\Data folder not found!")
                return False
            
            if os.path.isfile("vault.db") == False:
                os.chdir("..\\..")
                messagebox.showerror("Error","Database doesn't exist in Assets\\Data folder!")
                return False


            connection_obj = sqlite3.connect('vault.db')
            cursor_obj = connection_obj.cursor()
            statement = '''SELECT * FROM VAULT'''
            cursor_obj.execute(statement)
            output = cursor_obj.fetchall()

            txtbox.config(state=NORMAL)
            txtbox.delete("0.0","end")

            for row in output:
                enc_userid = row[0]
                userid_key = row[1]
                enc_password = row[2]
                enc_pass_key = row[3]

                userid = decrypt_data(enc_userid,userid_key)
                password = decrypt_data(enc_password,enc_pass_key)

                
                txtbox.insert(END,"____________________________________VAULT____________________________________\n")
                txtbox.insert(END,f"                                  userid = {userid}                              \n")
                txtbox.insert(END,f"                                  password = {password}                            \n")

            txtbox.config(state=DISABLED)
            os.chdir("..\\..")

        for widget in All_Frame.winfo_children():
            widget.destroy()
            
        txtbox = Text(All_Frame,bg=frame_bg_color,state=DISABLED,font=("Arial 14"),fg="red")
        txtbox.pack()
        

        show_btn = Button(All_Frame,text="Show",font=("sarif 20 bold"), bg=btn_bg_color,fg=btn_fg_color,cursor="hand2",command=show_passwords)
        show_btn.pack(pady=(15,15))
        


    def createpasswin():
        global win_logo,win_img,win_passlen_var,win_userid_var,win_password_var

        def handle_save(e):
            save_data()

        def save_data():
            userid = win_userid_var.get()
            password = win_password_var.get()

            if userid == "" or password == "":
                messagebox.showerror("Error","Invalid userid or password!")
                return None

            enc_userid,userid_key = encrypt_data(userid)
            enc_password,password_key = encrypt_data(password)

            create_db(enc_userid,userid_key,enc_password,password_key)
            messagebox.showinfo("Success","Your data is stored inside the database!")

        def set_password():
            password = gen_pass()
            win_password_var.set(value=password)

        for widget in All_Frame.winfo_children():
            widget.destroy()

        #textvariables
        win_userid_var = StringVar()  
        win_passlen_var = IntVar(value=12)  
        win_password_var = StringVar(value=gen_pass())  

        #image
        win_img = Image.open("Assets\\Images\\death2.png")
        win_img = win_img.resize((100,100))
        win_logo = ImageTk.PhotoImage(win_img)
        win_logo_lb1 = Label(All_Frame,image=win_logo,bg=frame_bg_color)
        win_logo_lb1.grid(row=0,column=0,pady=(15,15))

        #title
        win_logo_txt = Label(All_Frame,text="PASSGEN",fg="#fb1466",bg=frame_bg_color,font=("sarif 40 bold"))
        win_logo_txt.grid(row=0,column=1,pady=(15,15),padx=(0,0))

        win_user_lb = Label(All_Frame,text="Email Id",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color)
        win_user_lb.grid(row=1,column=0,padx=(60,30),pady=(0,15))

        win_passlen_lb = Label(All_Frame,text="Length",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color)
        win_passlen_lb.grid(row=2,column=0,padx=(60,30),pady=(0,15))      

        #entry
        win_user_en = Entry(All_Frame,textvariable=win_userid_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,justify="center")
        win_user_en.grid(row=1,column=1,padx=(0,30),pady=(0,15))
        win_user_en.focus()
        win_user_en.bind('<Return>',handle_save)

        win_passlen_en = Entry(All_Frame,textvariable=win_passlen_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,justify="center")
        win_passlen_en.grid(row=2,column=1,padx=(0,30),pady=(0,15))
        win_passlen_en.bind('<Return>',handle_save)

        win_pass_en = Entry(All_Frame,textvariable=win_password_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,justify="center")
        win_pass_en.grid(row=3,column=1,padx=(0,30),pady=(0,15))
        win_pass_en.bind('<Return>',handle_save)
        
        #button
        win_password_btn = Button(All_Frame,text="Password",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color,bd=0,cursor="hand2",command=set_password)
        win_password_btn.grid(row=3,column=0,padx=(60,30),pady=(0,15))
        win_password_btn.bind('<Enter>',on_enter)
        win_password_btn.bind('<Leave>',on_leave)

        win_save_btn = Button(All_Frame,text="Save",font=("sarif 20 bold"), bg=btn_bg_color,fg=btn_fg_color,cursor="hand2",command=save_data)
        win_save_btn.grid(row=4,column=1,pady=(0,15))


    root.destroy()
    win = Tk()
    win.title("PassGen")
    win.iconbitmap("Assets\\Images\\death.ico")
    win.geometry("950x725+200+20")
    win.config(bg=bg_color)

    #frames
    win_main_frame = Frame(win,bg=bg_color)
    win_main_frame.pack()

    btn_frame = Frame(win_main_frame,bg=bg_color)
    btn_frame.grid(row=0,column=0)

    All_Frame = Frame(win_main_frame,bg=frame_bg_color)
    All_Frame.grid(row=1,column=0,pady=(40,15))

    # win_logo = ImageTk.PhotoImage(img)
    # win_logo_lb = Label(All_Frame,image=win_logo,bg=frame_bg_color)
    # win_logo_lb.grid(row=0,column=0,pady=(15,15))


    #change pages
    p1 = Button(btn_frame,text="Create Passwords",bg=frame_bg_color,fg="cyan",font=("Arial 20 bold"),cursor="hand2",bd=0,command=createpasswin)
    p1.grid(row=0,column=0,padx=(0,16),pady=8)
    p1.bind('<Enter>',on_enter)
    p1.bind('<Leave>',on_leave)

    p2 = Button(btn_frame,text="Show Passwords",bg=frame_bg_color,fg="cyan",font=("Arial 20 bold"),cursor="hand2",bd=0,command=showpasswin)
    p2.grid(row=0,column=1,padx=(0,16),pady=8)
    p2.bind('<Enter>',on_enter)
    p2.bind('<Leave>',on_leave)

    #main frame content
    #textvariables
    win_userid_var = StringVar()  
    win_passlen_var = IntVar(value=12)  
    win_password_var = StringVar(value=gen_pass())  
    #image
    win_img = Image.open("Assets\\Images\\death2.png")
    win_img = win_img.resize((100,100))
    win_logo = ImageTk.PhotoImage(win_img)
    win_logo_lb1 = Label(All_Frame,image=win_logo,bg=frame_bg_color)
    win_logo_lb1.grid(row=0,column=0,pady=(15,15))
    #title
    win_logo_txt = Label(All_Frame,text="PASSGEN",fg="#fb1466",bg=frame_bg_color,font=("sarif 40 bold"))
    win_logo_txt.grid(row=0,column=1,pady=(15,15),padx=(0,0))
    win_user_lb = Label(All_Frame,text="Email Id",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color)
    win_user_lb.grid(row=1,column=0,padx=(60,30),pady=(0,15))
    win_passlen_lb = Label(All_Frame,text="Length",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color)
    win_passlen_lb.grid(row=2,column=0,padx=(60,30),pady=(0,15))      
    #entry
    win_user_en = Entry(All_Frame,textvariable=win_userid_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,justify="center")
    win_user_en.grid(row=1,column=1,padx=(0,30),pady=(0,15))
    win_user_en.focus()
    win_user_en.bind('<Return>',handle_save)

    win_passlen_en = Entry(All_Frame,textvariable=win_passlen_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,justify="center")
    win_passlen_en.grid(row=2,column=1,padx=(0,30),pady=(0,15))
    win_passlen_en.bind('<Return>',handle_save)

    win_pass_en = Entry(All_Frame,textvariable=win_password_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,justify="center")
    win_pass_en.grid(row=3,column=1,padx=(0,30),pady=(0,15))
    win_pass_en.bind('<Return>',handle_save)
    
    #button
    win_password_btn = Button(All_Frame,text="Password",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color,bd=0,cursor="hand2",command=set_password)
    win_password_btn.grid(row=3,column=0,padx=(60,30),pady=(0,15))
    win_password_btn.bind('<Enter>',on_enter)
    win_password_btn.bind('<Leave>',on_leave)

    win_save_btn = Button(All_Frame,text="Save",font=("sarif 20 bold"), bg=btn_bg_color,fg=btn_fg_color,cursor="hand2",command=save_data)
    win_save_btn.grid(row=4,column=1,pady=(0,15))

    

    win.mainloop()


def check_user_input():
    username = user_var.get().lower()
    password = pass_var.get()

    if username == "darkstar" and password == "3udwdxx68p":
        newwin()
    else:
        messagebox.showerror("Error","Invalid Username or Password, Please try again!")
        return False
        

def on_enter(e):
    e.widget['foreground'] = '#fb1466'

def on_leave(e):
    e.widget['foreground'] = 'cyan'

def handle_click(e):
    check_user_input()

#main window
root = Tk()
root.iconbitmap("Assets\\Images\\death.ico")
root.config(bg=bg_color)
root.title("Login")
root.geometry("800x600+200+50")

#frame
f = Frame(root,bg=frame_bg_color)
f.pack(pady=120)


#header
img = Image.open("Assets\\Images\\death.png")
img = img.resize((100,100))
logo = ImageTk.PhotoImage(img)
logo_lb = Label(f,image=logo,bg=frame_bg_color)
logo_lb.grid(row=0,column=0,pady=(15,15))

logo_txt = Label(f,text="PASSGEN",fg="#fb1466",bg=frame_bg_color,font=("sarif 40 bold"))
logo_txt.grid(row=0,column=1,pady=(15,0),padx=(0,0))



#label
user_lb = Label(f,text="Username",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color)
user_lb.grid(row=1,column=0,padx=(60,30),pady=(0,0))

pass_lb = Label(f,text="Password",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color)
pass_lb.grid(row=2,column=0,padx=(60,30),pady=(15,15))

#variables
user_var = StringVar(value="Darkstar")
pass_var = StringVar()

#entry
user_en = Entry(f,textvariable=user_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,justify="center")
user_en.grid(row=1,column=1,padx=(0,30),pady=(0,0))
user_en.bind("<Return>", handle_click)

pass_en = Entry(f,textvariable=pass_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,show='*',justify="center")
pass_en.grid(row=2,column=1,padx=(0,30),pady=(15,15))
pass_en.bind("<Return>", handle_click)
pass_en.focus()

#button
log_btn = Button(f,text="Login",font=("sarif 20 bold"), bg=btn_bg_color,fg=btn_fg_color,cursor="hand2",command=check_user_input)
log_btn.grid(row=3,column=1,pady=(0,70))

#btnconfig
log_btn.bind('<Enter>',on_enter)
log_btn.bind('<Leave>',on_leave)

root.mainloop()