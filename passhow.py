import customtkinter
from customtkinter import *
from PIL import Image
from CTkMessagebox import CTkMessagebox
import sqlite3
import os
from cryptography.fernet import Fernet

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("green")


#functions
def decrypt(enc_data,key):
    f = Fernet(key)
    og_data = f.decrypt(enc_data).decode()
    return og_data

def passgen_window():
    def check_data():
        try:
            os.chdir("c:/passgen")
        except:
            CTkMessagebox(icon="warning",title="Error",message="Cannot find c:/passgen")
            exit()

        isfile = os.path.isfile("vault.db")
        if isfile == True:
            show_data()
        elif isfile == False:
            tbl.delete('0.0','end')
            return 0

    def show_data():
        tbl.delete("0.0", "end")
        connection_obj = sqlite3.connect('vault.db')
        cursor_obj = connection_obj.cursor()
        statement = '''SELECT * FROM VAULT'''
        cursor_obj.execute(statement)
        output = cursor_obj.fetchall()
        for row in output:
            link = row[0]
            username = row[1]
            enc_password = row[2]
            key = row[3]
            password = decrypt(enc_password,key)
            tbl.insert('end',f"---------------------------------x--DATA--x------------------------------------ \n link = {link}\n username = {username}\n password = {password}\n")

        connection_obj.commit()
        connection_obj.close()

    top =customtkinter.CTkToplevel(root)
    top.focus()
    top.geometry("800x600+250+50")
    tbl = CTkTextbox(top,width=800,height=550,text_color="red",font=customtkinter.CTkFont(family="sarif", size=25))
    tbl.pack()
    reload_btn = CTkButton(top,text="reload",cursor="hand2",font=customtkinter.CTkFont(family="sarif", size=30),command=check_data)
    reload_btn.pack()
    top.mainloop()


def check_userinput():
    username = user_var.get().lower()
    password = pass_var.get()

    if username == root_username and password == root_password:
        passgen_window()
    else:
        CTkMessagebox(root,icon="warning",title="Error",message="Invalid username or password!")
        return 0
        

root = customtkinter.CTk()

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

#main configrations
root.geometry("800x600+200+50")

#frame
f = CTkFrame(root)
f.pack(pady=120)


#header
logo = customtkinter.CTkImage(Image.open("death.png"), size=(90, 90))
logo_lb = CTkLabel(f,image=logo,text="")
logo_lb.grid(row=0,column=0,pady=(15,15))

logo_txt = CTkLabel(f,text="PASSGEN",font=customtkinter.CTkFont(family="sarif", size=50))
logo_txt.grid(row=0,column=1,pady=(15,0),padx=(0,30))



#label
user_lb = CTkLabel(f,text="Username",font=customtkinter.CTkFont(family="sarif", size=30))
user_lb.grid(row=1,column=0,padx=(60,30),pady=(0,0))

pass_lb =   CTkLabel(f,text="Password",font=customtkinter.CTkFont(family="sarif", size=30))
pass_lb.grid(row=2,column=0,padx=(60,30),pady=(15,15))

#variables
user_var = StringVar(value="Darkstar")
pass_var = StringVar()

#entry
user_en = CTkEntry(f,textvariable=user_var,justify="center",font=customtkinter.CTkFont(family="sarif", size=30),width=300)
user_en.grid(row=1,column=1,padx=(0,30),pady=(0,0))


pass_en = CTkEntry(f,textvariable=pass_var,show='*',justify="center",font=customtkinter.CTkFont(family="sarif", size=30),width=300)
pass_en.grid(row=2,column=1,padx=(0,30),pady=(15,15))


#button
log_btn = CTkButton(f,text="Login",cursor="hand2",font=customtkinter.CTkFont(family="sarif", size=30),command=check_userinput)
log_btn.grid(row=3,column=1,padx=(0,30),pady=(0,30))

#btnconfig


root.mainloop()