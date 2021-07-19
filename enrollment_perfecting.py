#!/usr/bin/env python3

# GUI Module
from tkinter import *
import tkinter
from tkinter import messagebox
from tkinter import simpledialog

# Fingerprint sensor module
import Fingerprint_functions

# Firebase Module
import pyrebase

from CameraCapture import CameraCapture

# SMS Module
from Way2SMS import SMS

# Date Module
from datetime import date
import datetime

# Encryption - Decryption Module
import AES

# Hash module
import hashlib

# Random Module for sms otp
from random import randint

# Fingerprint sensor module
import Fingerprint_functions

import image_printing

# Time module
from time import sleep


flag = {"Aadhar_Num":False,"Name":False,"DOB":False,"Age_Id":False,"Address_Id":False,"Ph_Num":False,"Password":False,"Fingerprint":False,"Image":False,"OTP":False}

def exit_func():
    Aadhar_Num = Aadhar_var.get()
    pwd = password_tk.get()
    if(Aadhar_Num == "1234 5" and pwd == "password"):
        Main_Window.destroy()
    else:
        messagebox.showerror("Sorry","Sorry cant exit without admin priveleges")

#Default Screen
def Default():
    global flag
    Aadhar_var.set("1234 1234 1234")
    Name_var.set("John Lennon")
    DOB_var.set("05/01/2001")
    age_type_tk.set("DL")
    age_id_tk.set("AB-1234567890123")
    address_type_tk.set("DL")
    address_id_tk.set("AB-1234567890123")
    phone_tk.set("1234567890")

    e1.config(bg = "white")
    e2.config(bg="white")
    e3.config(bg="white")
    e4.config(bg="white")
    e5.config(bg="white")
    e6.config(bg="white")
    e7.config(bg="white")

    flag = dict.fromkeys(flag,False)

    test.setImage("default.png");

#Flag Checker
def Flag_Check():
    global flag
    if all(value == True for value in flag.values()):
        upload_button.config(state = NORMAL)
    else:
        print(flag)
        
    Main_Window.after(15, Flag_Check)

# A function which will upload the data to firestore cloud
def Upload_func():
    Aadhar_Num = Aadhar_var.get()
    Name = Name_var.get()
    dob = DOB_var.get()
    Age_Proof_Type = age_type_tk.get()
    Age_Proof_ID = age_id_tk.get()
    Address_Proof_Type = address_type_tk.get()
    Address_Proof_ID = address_id_tk.get()
    Ph_Num = phone_tk.get()
    pwd = password_tk.get()

    key = hashlib.sha256(pwd.encode()).digest()
    file_encryptor = AES.Encryptor(key)
    file_encryptor.encrypt_file("template.txt")

    data = {"Name" : Name,"DOB" : dob,"Age Proof Type" : Age_Proof_Type,"Age Proof ID" : Age_Proof_ID,"Address Proof Type" : Address_Proof_Type,"Address Proof ID" : Address_Proof_ID,'Phone':Ph_Num,'vote_flag' : 0}

    config = {
        "apiKey": "AIzaSyBjZ7kBApu-PsleX7-yYKv22d7JMgFUTZo",
        "authDomain": "cloud-based-biometric-voting.firebaseapp.com",
        "databaseURL": "https://cloud-based-biometric-voting.firebaseio.com",
        "storageBucket": "cloud-based-biometric-voting.appspot.com",
        "serviceAccount": "cloud-based-biometric-voting-firebase-adminsdk-gcwqk-d7b7ab4823.json"
    }

    firebase = pyrebase.initialize_app(config)

    db = firebase.database()
    storage = firebase.storage()
    sms = SMS('7JE5Z0LBP34CU9XI35UG2NGLSMUOYEYZ', 'GTHHSW4T22YTLKUN')

    template_path = "templates/" + Aadhar_Num + ".txt.enc"
    image_path = "images/" + Aadhar_Num + ".jpg"

    voter_enroll_check = db.child("Voter List").child(Aadhar_Num).get()

    if(voter_enroll_check.val() == None):
        messagebox.showinfo("Success","The record has been updated")
        db.child("Voter List").child(Aadhar_Num).set(data)
        storage.child(template_path).put("template.txt.enc")
        storage.child(image_path).put("image.jpg")

        sms.sendMessage(Ph_Num,"Your record has been updated")
        Default()
    else:
        messagebox.showerror("Error","The record already exists")

def func(c,Pic_Window):
    c.snap("image.jpg")
    c.stop()
    Pic_Window.destroy()
    test.setImage("image.jpg");
    flag["Image"]= True

# A function to click a picture of the voter
def pic_button():
    global flag
    Pic_Window = Toplevel()
    c = CameraCapture(tkWindow=Pic_Window, row=1)
    Pic_Window.title("Image Capture")
    b = Button(Pic_Window, text="Capture", command=lambda: func(c,Pic_Window))
    b.grid(row=0)
    Pic_Window.mainloop()


def fp_button():
    global flag
    fp = Fingerprint_functions.fingerprint_sensor()
    messagebox.showinfo("Fingerprint Acquisition", "Kindly place your left thumb on the fingerprint sensor")
    fp.enrollment()
    flag["Fingerprint"] = True

# OTP function
def OTP_Button():
    global flag
    sms = SMS('7JE5Z0LBP34CU9XI35UG2NGLSMUOYEYZ', 'GTHHSW4T22YTLKUN')
    OTP = randint(100000, 999999)
    Ph_Num = e6.get()
    sms.sendMessage(Ph_Num, str(OTP))
    Entered_otp = simpledialog.askstring("OTP Verification", "Enter the OTP you recieved on your phone", parent=Main_Window)
    if (Entered_otp == str(OTP)):
        messagebox.showinfo("Success", "Phone Number has been successfully verified")
        flag["OTP"] =True
    else:
        messagebox.showerror("ERROR", "OTP is wrong")

def password_key(event):
    global flag
    content = e7.get()
    pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    result = re.fullmatch(pattern,content)
    if result is not None:
        e7.config(bg = "green")
        flag["Password"] = True

    else:
        e7.config(bg = "red")

# Phone Number entry key
def phone_key(event):
    global flag
    phone_len = len(e6.get())
    if(phone_len == 9):
        content = e6.get()
        if event.char != '\b':
            content += event.char
        pattern = "^[0-9]{10}"
        result = re.fullmatch(pattern,content)
        if result is not None:
            e6.config(bg = "green")
            flag["Ph_Num"] = True
            e7.focus_set()
            otp_button.config(state = NORMAL)
        else:
            e6.config(bg = "red")

# Proof id key press
def address_id_key(event):
    global flag
    if (address_type_tk.get() == "DL"):
        dl_len = len(e5.get())
        if (dl_len is 2 and event.char != "\b"):
            e5.insert(END, "-")
        elif (dl_len == 15):
            content = e5.get() + event.char
            pattern = "^[A-Z]{2}-[0-9]{13}"
            result = re.fullmatch(pattern, content)
            if result is not None:
                e5.config(bg="green")
                flag["Address_Id"] = True
                e6.focus_set()
            else:
                e5.config(bg="red")
    if (address_type_tk.get() == "Passport"):
        pass_len = len(e5.get())
        if (pass_len is 1 and event.char != "\b"):
            e5.insert(END, "-")
        elif (pass_len == 8):
            content = e5.get() + event.char
            pattern = "^[A-Z]-[0-9]{7}"
            result = re.fullmatch(pattern, content)
            if result is not None:
                e5.config(bg="green")
                flag["Address_Id"] = True
                e6.focus_set()
            else:
                e5.config(bg="red")
# Proof ID format return
def format_ret():
    var1 = address_type_tk.get()
    if (var1 == "DL"):
        return "AB-1234567890123"
    if (var1 == "Passport"):
        return "A-1234567"

# Address proof dropdown
def address_proof_dropdown(*args):
    global flag
    flag["Address_Id"] = False
    address_id_tk.set(format_ret())

# Proof id key press
def age_id_key(event):
    global flag
    if (age_type_tk.get() == "DL"):
        dl_len = len(e4.get())
        if (dl_len is 2 and event.char != "\b"):
            e4.insert(END, "-")
        elif (dl_len == 15):
            content = e4.get() + event.char
            pattern = "^[A-Z]{2}-[0-9]{13}"
            result = re.fullmatch(pattern, content)
            if result is not None:
                e4.config(bg="green")
                flag["Age_Id"] = True
                popupMenu2.focus_set()
            else:
                e4.config(bg="red")
    if (age_type_tk.get() == "10th" or age_type_tk.get() == "12th"):
        c10_len = len(e4.get())
        if (c10_len == 5):
            content = e4.get()
            pattern = "^[0-9]{6}"
            result = re.fullmatch(pattern, content)
            if result is not None:
                e4.config(bg="green")
                flag["Age_Id"] = True
                popupMenu2.focus_set()
            else:
                e4.config(bg="red")
    if (age_type_tk.get() == "Passport"):
        pass_len = len(e4.get())
        if (pass_len is 1 and event.char != "\b"):
            e4.insert(END, "-")
        elif (pass_len == 8):
            content = e4.get() + event.char
            pattern = "^[A-Z]-[0-9]{7}"
            result = re.fullmatch(pattern, content)
            if result is not None:
                e4.config(bg="green")
                flag["Age_Id"] = True
                popupMenu2.focus_set()
            else:
                e4.config(bg="red")

# Proof ID format return
def format_return():
    var1 = age_type_tk.get()
    if (var1 == "DL"):
        return "AB-1234567890123"
    if (var1 == "10th"):
        return "123456"
    if (var1 == "12th"):
        return "123456"
    if (var1 == "Passport"):
        return "A-1234567"

# Age proof dropdown
def age_proof_dropdown(*args):
    global flag
    flag["Age_Id"] = False
    age_id_tk.set(format_return())

# Checks DOB
def dob_key_press(event):
    global flag
    dob_len = len(e3.get())
    if (dob_len in (2, 5) and event.char != "\b"):
        e3.insert(END, "/")
    elif (dob_len == 9):
        dob = e3.get()
        today = date.today()
        t = dob.strip().split('/')
        x = datetime.datetime(int(t[2]), int(t[1]), int(t[0]))
        age = today.year - x.year - ((today.month, today.day) < (x.month, x.day))
        content = e3.get() + event.char
        pattern = "^[0-9]{2}/[0-9]{2}/[0-9]{4}"
        result = re.fullmatch(pattern, content)
        if result is not None and age >= 18:
            e3.config(bg="green")
            flag["DOB"] =  True
            popupMenu.focus_set()
        else:
            e3.config(bg="red")

# Checks format of name
def name_key_press(event):
    global flag
    content = e2.get()
    pattern = "^[a-zA-Z]+ [a-zA-Z][a-zA-Z ]*"
    result = re.fullmatch(pattern,content)
    if(event.char == "\r"):
        if result is not None:
            e2.config(bg="green")
            flag["Name"] = True
            e3.focus_set()
            e3.delete(0,END)
        else:
          e2.config(bg="red")

# Gives space in appropriate places for aadhar
def aadhar_key_press(event):
    global flag
    aadhar_len = len(e1.get())
    if(aadhar_len in (4,9) and event.char != "\b"):
        e1.insert(END," ")
    elif(aadhar_len == 13):
        content = e1.get() + event.char
        pattern = "^[0-9]{4} [0-9]{4} [0-9]{4}"
        result = re.fullmatch(pattern,content)
        if result is not None:
            e1.config(bg= "green")
            flag["Aadhar_Num"] = True
            e2.focus_set()
            e2.delete(0, END)
        else:
            e1.config(bg = "red")

# Clears sample text upon focusin
def focus_in_func(event,entry_obj):
    entry_obj.delete(0,END)


# Checks format upon focusout
#def focus_out_func:

# Creates a window to hold all the widgets
Main_Window = Tk()
Main_Window.title('Voter List Enrollment')

# Global tkvar variables
Aadhar_var = StringVar(Main_Window)
Name_var = StringVar(Main_Window)
DOB_var = StringVar(Main_Window)
age_type_tk = StringVar(Main_Window)
age_id_tk = StringVar(Main_Window)
address_type_tk = StringVar(Main_Window)
address_id_tk = StringVar(Main_Window)
phone_tk = StringVar(Main_Window)
password_tk = StringVar(Main_Window)

# Widget to collect the Aadhar Number
Label(Main_Window, text='Aadhar Number').grid(row=0)
e1 = Entry(Main_Window,textvariable = Aadhar_var)
e1.grid(row=0, column=1)
Aadhar_var.set("1234 1234 1234")
e1.bind("<FocusIn>",lambda event:focus_in_func(event,e1))
e1.bind("<Key>",aadhar_key_press)

# Widget to collect the Name
Label(Main_Window, text='Name').grid(row=1)
e2 = Entry(Main_Window,textvariable = Name_var)
e2.grid(row=1, column=1)
Name_var.set("John Lennon")
e2.bind("<Key>",name_key_press)

# Widget to collect the D.O.B
Label(Main_Window, text='D.O.B').grid(row=2)
e3 = Entry(Main_Window,textvariable = DOB_var)
e3.grid(row=2, column=1)
DOB_var.set("05/01/2000")
e3.bind("<Key>",dob_key_press)

# Widget to collect the Age Proof Type
Label(Main_Window, text='Age Proof Type').grid(row=3)
choices = {'DL','10th','12th','Passport'} # Dictionary with options
age_type_tk.set('DL') # set the default option
popupMenu = OptionMenu(Main_Window,age_type_tk, *choices)
popupMenu.grid(row = 3, column =1)
age_type_tk.trace('w', age_proof_dropdown) # link function to change dropdown

# Widget to collect the Age Proof ID
Label(Main_Window, text='Age Proof ID').grid(row=4)
e4 = Entry(Main_Window, textvariable = age_id_tk)
e4.grid(row=4, column=1)
age_id_tk.set("AB-1234567890123")
e4.bind("<FocusIn>",lambda event: focus_in_func(event,e4))
e4.bind("<Key>",age_id_key)

# Widget to collect the Address Proof Type
Label(Main_Window, text='Address Proof Type').grid(row=5)
choices = {'DL','Passport'} # Dictionary with options
address_type_tk.set('DL') # set the default option
popupMenu2 = OptionMenu(Main_Window,address_type_tk, *choices)
popupMenu2.grid(row = 5, column =1)
address_type_tk.trace('w', address_proof_dropdown) # link function to change dropdown

# Widget to collect the Address Proof ID
Label(Main_Window, text='Address Proof ID').grid(row=6)
e5 = Entry(Main_Window, textvariable = address_id_tk)
e5.grid(row=6, column=1)
address_id_tk.set("AB-1234567890123")
e5.bind("<FocusIn>",lambda event: focus_in_func(event,e5))
e5.bind("<Key>",address_id_key)


# Widget to collect the Phone Number
Label(Main_Window, text='Phone Number').grid(row=7)
e6 = Entry(Main_Window,textvariable = phone_tk)
e6.grid(row=7, column=1)
phone_tk.set("1234567890")
e6.bind("<FocusIn>",lambda event: focus_in_func(event,e6))
e6.bind("<Key>",phone_key)

# Widget to collect the Password
Label(Main_Window, text='Password').grid(row=8)
e7 = Entry(Main_Window,show = '*', textvariable = password_tk)
e7.grid(row=8, column=1)
e7.bind("<Key>",password_key)


# Widget button to upload
upload_button = Button(Main_Window,text = 'Upload',width=10,command = Upload_func,state = DISABLED)
upload_button.grid(row = 5,column = 4)

# Widget button to send sms otp
otp_button = Button(Main_Window,text = 'Send SMS',width=10,command = OTP_Button,state = DISABLED)
otp_button.grid(row = 4,column = 4)

# Widget button for fingerprint acquisiton
FP = Button(Main_Window,text = 'Fingerprint',width=10,command = fp_button)
FP.grid(row = 3,column = 4)

# Widget button for image selection
FP = Button(Main_Window,text = 'Image',width=10,command = pic_button)
FP.grid(row = 2,column = 4)

canvas = Canvas(Main_Window, width=360, height=360)
canvas.grid(row=3, column=3, rowspan=9, sticky="ew")
test = image_printing.IMAGE(canvas)
test.setImage("default.png");

close_button = Button(Main_Window, text="Exit", command= exit_func)
close_button.grid(row=6, column=4)

Main_Window.after(15, Flag_Check)

Main_Window.attributes("-fullscreen", True)

mainloop()

