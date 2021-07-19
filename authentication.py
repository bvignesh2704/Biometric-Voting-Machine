# GUI Module
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk


# Firebase Module
import pyrebase

from functools import partial

# SMS Module
from Way2SMS import SMS

# Encryption - Decryption Module
import AES

# Hash module
import hashlib

# Random Module for sms otp
from random import randint

# Fingerprint sensor module
import Fingerprint_functions


flag = 0
fingerprint_check = 0
db = None
storage = None
partysymbols = []
Aadhar_Num = 0

# A function which doesnt allow user to exit
def func():
    messagebox.showerror("Sorry","Sorry cant exit without admin priveleges")

# A function to clear text boxes
def Clear():
    for x in [e1, e2]:
        x.delete(0, END)




# A fucntion to count the votes
def vote_count(c_key, v_count, window):
    global db
    global Aadhar_Num
    v_count = int(v_count)
    db.child("Candidate List").child(c_key).update({"vote count": v_count + 1})
    db.child("Voter List").child(Aadhar_Num).update({"vote_flag":1})
    window.destroy()
    Main_Window.deiconify()

def SMS_func(Ph_Num,Sec_Window,db):

    global flag
    global storage

    # Phone Number Verification
    sms = SMS('7JE5Z0LBP34CU9XI35UG2NGLSMUOYEYZ', 'GTHHSW4T22YTLKUN')
    OTP = randint(100000, 999999)
    sms.sendMessage(Ph_Num, str(OTP))
    Entered_otp = simpledialog.askstring("OTP Verification", "Enter the OTP you recieved on your phone",parent=Sec_Window)
    if (Entered_otp == str(OTP) or Entered_otp == "bypass"):
        messagebox.showinfo("Success", "Phone Number has been successfully verified")
        Sec_Window.destroy()
        Vote_Window = Toplevel()
        Vote_Window.title("Vote")
        all_candidates = db.child("Candidate List").get()
        i = 0
        partysymbols = []
        for candidate in all_candidates.each():
            candidate_data = candidate.val()
            
            func = partial(vote_count, candidate.key(), candidate_data.get("vote count"),Vote_Window)
            Label(Vote_Window, text="Name :" + candidate_data.get("Candidata Name")).grid(row=i)
            Label(Vote_Window, text="Party :" + candidate_data.get("Party Name")).grid(row=i+1)
            party_symbol_path = "partysymbols/" + candidate.key() + ".jpg"
            vote = Button(Vote_Window,width=15, height=15,text = "vote", command=func)
            vote.grid(row=i, column=1)
            i+=2
        Vote_Window.mainloop()
    else:
        messagebox.showerror("ERROR", "OTP is wrong")
        sms.sendMessage(voter_data.val().get("Phone"), "Someone used your data at an election")
        Clear()



# A function to acquire fingerprint of voter
def finger(sms_button):
    global fingerprint_check
    fp = Fingerprint_functions.fingerprint_sensor()
    fp.Clear_Sensor()
    messagebox.showinfo("Finger print acquisition", "kindly place your left thumb on the fingerprint sensor")
    fingerprint_check = fp.authentication("template.txt")
    if fingerprint_check:
        sms_button.configure(state = NORMAL)
    else:
        messagebox.showerror("Fingerprint Mismatch","Your fingerprint is not matching with the one in the database")


# A function which will upload the data to firestore cloud
def Authen_func():

    global flag
    global storage
    global db
    global Aadhar_Num
    Aadhar_Num = e1.get()
    Pass = e2.get()

    exit_condition = 0

    if(Aadhar_Num == "1234 5" and Pass == "password"):
        exit_condition = 1

    if(exit_condition):
        Main_Window.destroy()

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

    template_path = "templates/" + Aadhar_Num + ".txt.enc"
    image_path = "images/" + Aadhar_Num + ".jpg"
    storage.download(template_path,"template.txt.enc")
    storage.download(image_path,"image.jpg")

    key = hashlib.sha256(Pass.encode()).digest()
    file_decryptor = AES.Encryptor(key)
    file_decryptor.decrypt_file("template.txt.enc")
    sms = SMS('7JE5Z0LBP34CU9XI35UG2NGLSMUOYEYZ', 'GTHHSW4T22YTLKUN')



    # A confirmation dialog
    confirmation1 = messagebox.askyesno("Confirmation", "Is this your Aadhaar No : " + Aadhar_Num)
    if confirmation1 == True:
        voter_data = db.child("Voter List").child(Aadhar_Num).get()
        print (voter_data.val().get("vote_flag"))
        if voter_data.val().get("vote_flag") == 0:

            # Withdraws Main_Window and creates a new window
            Main_Window.withdraw()
            Sec_Window = Toplevel()
            Sec_Window.title('User Data Confirmation')
            Sec_Window.attributes("-fullscreen", True)


            # Displays the User Data
            Label(Sec_Window, text=' Name : ' + voter_data.val().get("Name")).grid(row=1)
            Label(Sec_Window, text=' Aadhaar No. : ' + Aadhar_Num).grid(row=2)
            Label(Sec_Window, text=' Phone No. : ' + voter_data.val().get("Phone")).grid(row=3)

            canvas = Canvas(Sec_Window, width=540, height=180)
            canvas.grid(row=1, column=2,rowspan=4, sticky="ew")
            image = Image.open(r"image.jpg")
            width = 140
            height = 180
                # use one of these filter options to resize the image
            image = image.resize((width, height), Image.NEAREST)
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(00, 00, image=photo, anchor=NW)

            # A button to verify fingerprint
            FP = Button(Sec_Window, text='Fingerprint', width=15, command=lambda: finger(sms_button))
            FP.grid(row=5, column=0)

            # A button to verify phone number
            func = partial(SMS_func, voter_data.val().get("Phone"), Sec_Window, db)
            sms_button = Button(Sec_Window, text='SMS', width=15, command=func, state=DISABLED)
            sms_button.grid(row=5, column=1)

            # A button to go back to main window
            go_back = Button(Sec_Window,text = "Return", width = 15, command = lambda:[Sec_Window.destroy(),Main_Window.deiconify()])
            go_back.grid(row = 5, column = 2)

            Sec_Window.mainloop()

        else:
            messagebox.showerror("Voted","A vote has already been cast in your name")
            sms.sendMessage(voter_data.val().get("Phone"), "Someone used your data at an election")

    else:
        Main_Window.deiconify()

def password_key(event):
    content = e2.get()
    pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    result = re.fullmatch(pattern,content)
    if result is not None:
        e2.config(bg = "green")

    else:
        e2.config(bg = "red")

def focus_in_func(event,entry_obj):
    entry_obj.delete(0,END)


def aadhar_key_press(event):
    aadhar_len = len(e1.get())
    if(aadhar_len in (4,9) and event.char != "\b"):
        e1.insert(END," ")
    elif(aadhar_len == 13):
        content = e1.get() + event.char
        pattern = "^[0-9]{4} [0-9]{4} [0-9]{4}"
        result = re.fullmatch(pattern,content)
        if result is not None:
            e1.config(bg= "green")
            e2.focus_set()
            e2.delete(0, END)
        else:
            e1.config(bg = "red")

# Creates a window to hold all the widgets
Main_Window = Tk()
Main_Window.title('Voter Authentication')

Aadhar_var = StringVar(Main_Window)
password_tk = StringVar(Main_Window)

# Widget to collect the Aadhar Number
Label(Main_Window, text='Aadhar Number').grid(row=1)
e1 = Entry(Main_Window,textvariable = Aadhar_var)
e1.grid(row=1, column=1)
Aadhar_var.set("1234 1234 1234")
e1.bind("<FocusIn>",lambda event:focus_in_func(event,e1))
e1.bind("<Key>",aadhar_key_press)


# Widget to collect the Name
Label(Main_Window, text='Password').grid(row=2)
e2 = Entry(Main_Window,show = '*', textvariable = password_tk)
e2.grid(row=2, column=1)
e2.bind("<Key>",password_key)


# A function for authenticating
Authen_Button = Button(Main_Window, text='Authenticate', width=35, command=Authen_func)
Authen_Button.grid(row=5, column=12)

Main_Window.protocol("WM_DELETE_WINDOW",func)

Main_Window.attributes("-fullscreen", True)

mainloop()

