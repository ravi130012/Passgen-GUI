from tkinter import *
from tkinter import messagebox
import string
import random
from PIL import Image,ImageTk
from cryptography.fernet import Fernet
import sqlite3
import os


#credentials
root_username = "darkstar"
root_password = "3udwdxx68p"

#configrations
bg_color = "#2A2A2A"
frame_bg_color = "#1F1F1F"
label_fg_color = "cyan"
btn_fg_color = "cyan"
btn_bg_color = "#1F1F1F"
entry_bg_color = "#1F1F1F"
entry_fg_color = "red"

#defining root object
root = Tk()


#function


def encrypt(data):
    key = Fernet.generate_key()
    f = Fernet(key)
    enc_data = f.encrypt(data.encode())
    return enc_data,key



def create_db(link,username,password,key):
    if os.path.isdir("c:/passgen") == False:
        try:
            os.mkdir("c:/passgen")
            os.chdir("c:/passgen")

        except Exception as e:
            messagebox.showerror("Error",e)
            exit()
    elif os.path.isdir("c:/passgen") == True:
        try:
            os.chdir("c:/passgen")
        except Exception as w:
            messagebox.showerror("error",w)
            exit()

    


    conn = sqlite3.connect('vault.db')
    cursor = conn.cursor()  
    table ="""CREATE TABLE IF NOT EXISTS VAULT(link TEXT NOT NULL, username TEXT NOT NULL,
    password BYTE NOT NULL, key BYTE NOT NULL);"""
    cursor.execute(table)   
    unique_index_query = """CREATE UNIQUE INDEX IF NOT EXISTS idx_link_username_password_key ON VAULT(link,username);"""
    cursor.execute(unique_index_query)  
    # Queries to INSERT records.
    cursor.execute('''INSERT OR REPLACE INTO VAULT VALUES (?,?,?,?)''',(link,username,password,key))
    conn.commit()   
    # Closing the connection
    conn.close()



def on_enter(e):
    log_btn['foreground'] = '#fb1466'

def on_leave(e):
    log_btn['foreground'] = 'cyan'

    
def handle_click(e):
    check_user_input()

def passgen_window():
    
    #functions
    def passgen():
        length = len_pass_var.get()
        com = 0
        genpass = ""
        char = ['@','$','#','!','&']

        for i in string.ascii_letters:
            char.append(i)

        for j in string.digits:
            char.append(j)

        random.shuffle(char)

        while length > com:
            ch = random.choice(char)
            genpass = genpass+ch
            com = com+1

        tp_pass_var.set(genpass)

        

    def save_on_leave(e):
        save_btn['foreground'] = 'cyan'
    
    def save_on_enter(e):
        save_btn['foreground'] = '#fb1466'

    def gen_on_leave(e):
        gen_btn['foreground'] = 'cyan'
    
    def gen_on_enter(e):
        gen_btn['foreground'] = '#fb1466'

    def save_data():
        link = url_var.get()
        username = tp_usr_var.get()
        password = tp_pass_var.get()

        en_pass,pass_key = encrypt(password)
        create_db(link,username,en_pass,pass_key)
        messagebox.showinfo("Success","Your data is stored in database!")

    #toplevel
    top = Toplevel(root)
    top.geometry("800x700+200+50")
    top.title("Passgen")
    top.config(bg=bg_color)

    #topframe
    frame = Frame(top,bg=frame_bg_color)
    frame.pack(pady=120)

    #header
    top_logo = ImageTk.PhotoImage(img)
    top_logo_lb = Label(frame,image=top_logo,bg=frame_bg_color)
    top_logo_lb.grid(row=0,column=0,pady=(70,0))

    top_logo_txt = Label(frame,text="PASSGEN",fg="#fb1466",bg=frame_bg_color,font=("sarif 40 bold"))
    top_logo_txt.grid(row=0,column=1,pady=(70,0))

    #label
    url_lb =  Label(frame,text="Url",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color)
    url_lb.grid(row=1,column=0,padx=(15,15),pady=(15,15))

    user_lb =  Label(frame,text="Username",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color)
    user_lb.grid(row=2,column=0,padx=(15,15),pady=(0,15))

    pass_len_lb =  Label(frame,text="Length",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color)
    pass_len_lb.grid(row=3,column=0,padx=(15,15),pady=(0,15))

    #button
    gen_btn = Button(frame,text="Password",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color,bd=0,cursor="hand2",command = passgen)
    gen_btn.grid(row=4,column=0,padx=(0,15),pady=(0,15))

    save_btn = Button(frame,text="Save",font=("sarif 20 bold"),bg=frame_bg_color,fg=label_fg_color,cursor="hand2",command=save_data)
    save_btn.grid(row=5,column=1,pady=(0,70))

    #btn config
    save_btn.bind('<Enter>',save_on_enter)
    save_btn.bind('<Leave>',save_on_leave)

    gen_btn.bind('<Enter>',gen_on_enter)
    gen_btn.bind('<Leave>',gen_on_leave)

    #entryvar
    url_var = StringVar(value="https://google.com/")
    tp_usr_var = StringVar(value="ravishankar599955@gmail.com")
    tp_pass_var = StringVar()
    len_pass_var = IntVar(value=12)

    #entry
    url_en = Entry(frame,textvariable=url_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,justify="center")
    url_en.grid(row=1,column=1,padx=(0,15),pady=(15,15))

    tp_user_en = Entry(frame,textvariable=tp_usr_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,justify="center")
    tp_user_en.grid(row=2,column=1,padx=(0,15),pady=(0,15))

    len_pass_en = Entry(frame,textvariable=len_pass_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,justify="center")
    len_pass_en.grid(row=3,column=1,padx=(0,15),pady=(0,15))

    tp_pass_en = Entry(frame,textvariable=tp_pass_var,font=("san-sarif 20"),bg=entry_bg_color,fg=entry_fg_color,justify="center")
    tp_pass_en.grid(row=4,column=1,padx=(0,15),pady=(0,15))



    top.mainloop()


def check_user_input():
    password = str(pass_var.get())
    username = str(user_var.get().lower())
    # print(f"username = {username}\npassword = {password}")

    if username == root_username and password == root_password:
        passgen_window()
    else:
        messagebox.showerror("Error","Invalid username or password!")
        exit()
#main configrations
root.config(bg=bg_color)
root.title("Login")
root.geometry("800x600+200+50")

#frame
f = Frame(root,bg=frame_bg_color)
f.pack(pady=120)


#header
img = Image.open("death.png")
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

#button
log_btn = Button(f,text="Login",font=("sarif 20 bold"), bg=btn_bg_color,fg=btn_fg_color,cursor="hand2",command=check_user_input)
log_btn.grid(row=3,column=1,pady=(0,70))

#btnconfig
log_btn.bind('<Enter>',on_enter)
log_btn.bind('<Leave>',on_leave)

root.mainloop()