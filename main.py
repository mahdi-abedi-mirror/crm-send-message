from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import requests
import time 
import pywhatkit
import pyautogui
from pynput.keyboard import Key, Controller
import requests
import json


root = Tk()
root.title("پنل مدیریت مشتریان")
width = 900
height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="black")

#============================VARIABLES===================================
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
CONTACT = StringVar()
TOKEN = "0000000000000000000000000000000000000000000000"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
urlfaraz = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"
apikeyfaraz = '000000000000000000000000000000000000000000000000000'
message = "Hello welcome"
chat_id = "0000000000000000000000"


#============================METHODS=====================================

def Database():
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, gender TEXT, contact INTEGER)")
    cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitData():
    if  FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or CONTACT.get() == "":
        result = tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `member` (firstname, lastname, gender, contact) VALUES(?, ?, ?, ?)", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(CONTACT.get())))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        CONTACT.set("")
        
        #this part for telegram
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
        print(requests.get(url).json()) # this sends the message
        print("Telegram Message sent!")
        
        #this part for whatsapp
        phone_numer = CONTACT
        keyboard = Controller()
        pywhatkit.sendwhatmsg_instantly(
            phone_no="+98"+phone_numer, 
            message=message
        )
        time.sleep(10)
        pyautogui.click()
        time.sleep(2)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        pywhatkit.sendwhatmsg_instantly(
            tab_close=True)
        print("Whatsapp Message sent!")
        
        #this part for SMS
        PersonName= FIRSTNAME+LASTNAME
        payload = json.dumps({
        "code": "3jqa90l7iyvttqf",
        "sender": "+983000505",
        "recipient": "000000000000000",
        "variable": {
        PersonName: message
        }
        })
        headers = {
        'apikey': '0000000000000000000000000000000000',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)

        
def UpdateData():
    if GENDER.get() == "":
       result = tkMessageBox.showwarning('', 'لطفا فیلدهارا کامل کنید', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `firstname` = ?, `lastname` = ?, `gender` =?, `contact` = ? WHERE `mem_id` = ?", (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        CONTACT.set("")
        
    
def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    CONTACT.set("")
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    CONTACT.set(selecteditem[6])
    UpdateWindow = Toplevel()
    UpdateWindow.title("پنل مدیریت مراجعین موسسه دی ")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) + 450) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    UpdateWindow.resizable(0, 0)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'NewWindow' in globals():
        NewWindow.destroy()

    #===================FRAMES==============================
    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="آقا", variable=GENDER, value="Male",  font=('arial', 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="خانم", variable=GENDER, value="Female",  font=('arial', 14)).pack(side=LEFT)
    
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="ثبت تماس", font=('arial', 16), bg="orange",  width = 300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="نام", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(ContactForm, text="نام خانوادگی", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(ContactForm, text="جنسیت", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_contact = Label(ContactForm, text="شماره تماس", font=('arial', 14), bd=5)
    lbl_contact.grid(row=5, sticky=W)

    #===================ENTRY===============================
    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT,  font=('arial', 14))
    contact.grid(row=5, column=1)
    

    #==================BUTTONS==============================
    btn_updatecon = Button(ContactForm, text="ثبت", width=50, command=UpdateData)
    btn_updatecon.grid(row=6, columnspan=2, pady=10)


#fn1353p    
def DeleteData():
    if not tree.selection():
       result = tkMessageBox.showwarning('', 'لطفا گزینه ای را انتخاب کنید', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'آیا برای حذف مطمئن هستید؟', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("pythontut.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
    
def AddNewWindow():
    global NewWindow
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    CONTACT.set("")
    NewWindow = Toplevel()
    NewWindow.title("پنل مدیریت مراجعین موسسه دی ")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()
    
    #===================FRAMES==============================
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="آقا", variable=GENDER, value="Male",  font=('arial', 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="خانم", variable=GENDER, value="Female",  font=('arial', 14)).pack(side=LEFT)
    
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="اضافه کردن", font=('arial', 16), bg="#66ff66",  width = 300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="نام", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(ContactForm, text="نام خانوادگی", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(ContactForm, text="جنسیت", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_contact = Label(ContactForm, text="شماره تماس", font=('arial', 14), bd=5)
    lbl_contact.grid(row=5, sticky=W)

    #===================ENTRY===============================
    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT,  font=('arial', 14))
    contact.grid(row=5, column=1)
    

    #==================BUTTONS==============================
    btn_addcon = Button(ContactForm, text="ذخیره", width=50, command=SubmitData)
    btn_addcon.grid(row=6, columnspan=2, pady=10)




    
#============================FRAMES======================================
Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500,  bg="black")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="black")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)
#============================LABELS======================================
lbl_title = Label(Top, text="پنل مدیریت مراجعین موسسه دی ", font=('arial', 16), width=500,bg="blue")
lbl_title.pack(fill=X)

#============================ENTRY=======================================

#============================BUTTONS=====================================
btn_add = Button(MidLeft, text="+ اضافه کردن", bg="#66ff66", command=AddNewWindow)
btn_add.pack()
btn_delete = Button(MidRight, text="- حذف", bg="red", command=DeleteData)
btn_delete.pack(side=RIGHT)

#============================TABLES======================================
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Firstname", "Lastname", "Gender", "Contact"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Firstname', text="Firstname", anchor=W)
tree.heading('Lastname', text="Lastname", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=80)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

#============================INITIALIZATION==============================
if __name__ == '__main__':
    Database()
    root.mainloop()
    
