# GUI Module
from tkinter import *
from tkinter import messagebox,simpledialog,filedialog



# Firebase Module
import pyrebase

# Time module
from time import sleep

filename = ""

def Clear():
    for x in [e1,e2,e3]:
        x.delete(0, END)

# A function to get symbol path
def symbol_button():
    global filename
    filename = filedialog.askopenfilename()
    print(filename)

# A function to upload to database
def upload_button():
    global filename

    party_name = e1.get()
    candidate_name = e2.get()
    candidate_id = e3.get()

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

    data = {"Candidata Name": candidate_name, "Party Name": party_name,"vote count": 0}
    candidate_check = db.child("Candidate List").child(candidate_id).get()
    if(candidate_check.val() == None):
        db.child("Candidate List").child(candidate_id).set(data)
        symbol_path = "partysymbols/" + candidate_name + ".jpg"
        storage.child(symbol_path).put(filename)
        messagebox.showinfo("Success", "The record has been updated")
        Clear()
    else:
        messagebox.showerror("Error", "The record already exists")
        Clear()

# Creates a window to hold all the widgets
Main_Window = Tk()
Main_Window.title('Candidate Database')

# Widget to collect the Party Name
Label(Main_Window, text='Party Name').grid(row=0)
e1 = Entry(Main_Window)
e1.grid(row=0, column=1)



# Widget to collect the Candidate Name
Label(Main_Window, text='Candidate Name').grid(row=1)
e2 = Entry(Main_Window)
e2.grid(row=1, column=1)

# Widget to collect the Candidate ID
Label(Main_Window, text='Candidate ID').grid(row=2)
e3 = Entry(Main_Window)
e3.grid(row=2, column=1)

# Widget to collect the Party Symbol
symbol = Button(Main_Window,text = 'Party Symbol',width=25,command = symbol_button)
symbol.grid(row = 3,column = 1)

# Widget to upload data
symbol = Button(Main_Window,text = 'Upload',width=25,command = upload_button)
symbol.grid(row = 5,column = 5)

mainloop()