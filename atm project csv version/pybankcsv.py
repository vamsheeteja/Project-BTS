# imports
from tkinter import *
import os
from PIL import ImageTk, Image


# Python OOP 
# Program displays cash transactions messages of a bank account
import sys
import random
import csv

class Bank():
    def __init__(self, cnt=None, acc_no=None, pin=None, name=None, age=None, balance=None):
        
        if(isinstance(self, Custom)): # creates a object for each new entry
            self.cnt = cnt
            self.acc = acc_no
            self.pin = pin
            self.name = name
            self.age = age
            self.bal = balance
            
            
            self.add2csv(self.cnt, self.acc, self.pin, self.name, self.age, self.bal)
            

    def add2csv(self, cnt, acc, pin, name, age, bal):
        
        file = open("bank_accounts.csv", "a")
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow([cnt, acc, pin, name, age, bal])
        file.close()
            

class Custom(Bank):
    flag = 0
    counter = 0
    try:
        file = open("bank_accounts.csv")
    except FileNotFoundError:
        with open("bank_accounts.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["SNO", "ACC_NO", "PIN", "Name", "AGE", "BALANCE"])
            flag = 1
            file.close()
            pass
    
    if flag == 0:
        file =  open("bank_accounts.csv", "r")
        data = file.readlines()
        counter = int(data[-1][0])
        file.close()
        
    def __init__(self, acc_no, epin, name, age, balance):
        flag = 1
        Custom.counter += 1
        super().__init__(Custom.counter, acc_no, epin, name, age, balance)
    
    # transactions method.
    @staticmethod
    def transaction(fl, pin, amt=0):
        
        # here the following code (lines ) copies the data (each row as a list) and returns list to the mylist variable
        file =  open("bank_accounts.csv", "r")
        reader = csv.reader(file)
        mylist = list(reader) # contains the data of csv file as a list of all rows
        file.close()
        
        flag = 0 # flag variable to print message if pin is not found
        
        # the updatefile method is used to update the file everytime when a transaction is made. (pratically it somewhat different than what it said) 
        def updatefile(mylist):
            upfile = open("bank_accounts.csv", "w", newline = '')
            writer = csv.writer(upfile)
            writer.writerows(mylist)
            upfile.close()

        # here checking the pin whether it is present or not and peforming ops
        for i in range(2, len(mylist)):
            
            if int(mylist[i][2]) == int(pin):
                flag = 1
                # deposit op
                if fl == 'd':
                    pamt = mylist[i][5]
                    mylist[i][5] = int(pamt) + int(amt)
                    updatefile(mylist)
                    # deposit message
                    dep_msg_screen = Toplevel(deposit_screen)
                    msg = "Transaction Successful" + "\nDeposited Rs." + str(amt) + " to Account Number: "+ str(mylist[i][1]) +", Account Holder: " + str(mylist[i][3]) + " New Balance: " + str(mylist[i][5])
                    Label(dep_msg_screen, text=msg, font=('Calibri', 14)).grid(row=1, sticky=N, pady=10)
                    break
                
                # withdraw op
                elif fl == 'w':
                    pamt = mylist[i][5]
                    # witd screen
                    witd_msg_screen = Toplevel(withdraw_screen)
                    if int(amt) > int(pamt):
                        msg = "Insuffient Balance! Sorry you can't make that! your current balance is: " + str(pamt)
                        Label(witd_msg_screen, text=msg, font=('Calibri', 14)).grid(row=1, sticky=N, pady=10)
                        break    
                    mylist[i][5] = int(pamt) - int(amt)
                    updatefile(mylist)
                    # withdraw message
                    msg = "Transaction Successful" + "\nRs." + str(amt) + " withdrawn from Account Number: "+ str(mylist[i][1]) +", Account Holder: " + str(mylist[i][3]) + " New Balance: " + str(mylist[i][5])
                    Label(witd_msg_screen, text=msg, font=('Calibri', 14)).grid(row=1, sticky=N, pady=10)
                    break

                # status op
                elif fl == 's':
                    # balance-check message
                    bal_chk_msg_screen = Toplevel(stat_screen)
                    msg = "Account Number: " + str(mylist[i][1]) + "\nAccount Holder: " + str(mylist[i][3]) + "\nNew Balance: " + str(mylist[i][5])
                    Label(bal_chk_msg_screen, text=msg, font=('Calibri', 14)).grid(row=1, sticky=N, pady=10)
                    break
                    

        # msg is printed if pin not found
        if flag == 0:
            if fl == 'd':
                notif2_.config(fg="red", text="Invalid PIN*")
            elif fl == 'w':
                notif3_.config(fg="red", text="Invalid PIN*")
            else:
                notif4_.config(fg="red", text="Invalid PIN*")

# main screen
master = Tk()
master.title("Banking App")

# functions
def dep_go():

    pin = temp_spin.get()
    amt = temp_samt.get()

    global notif2_
    notif2 = Label(deposit_screen, font=('Calibri', 12))
    notif2_ = Label(deposit_screen, font=('Calibri', 12))
    notif2.grid(row=6, sticky=N, pady=10)
    notif2_.grid(row=7, sticky=N, pady=10)

    if pin == "" or amt == "":
        notif2.config(fg="red", text="All fields required*")
    else:
        Custom.transaction('d', pin, amt)
        

# deposit
def dep():
    global temp_spin
    global temp_samt
    temp_spin = StringVar()
    temp_samt = StringVar()

    # deposit_screen
    global deposit_screen
    deposit_screen = Toplevel(atm_mode_screen)
    deposit_screen.title("deposit amount")
    
    Label(deposit_screen, text="Please enter your pin and deposit amount", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(deposit_screen, text="Pin", font=('Calibri', 12)).grid(row=2, sticky=W)
    Label(deposit_screen, text="Amount", font=('Calibri', 12)).grid(row=3, sticky=W)
    
    # entries 
    Entry(deposit_screen, textvariable=temp_spin).grid(row=2, column=1)
    Entry(deposit_screen, textvariable=temp_samt).grid(row=3, column=1)
    
    # buttons
    Button(deposit_screen, text="Submit", command = dep_go, font=("Calibri", 12)).grid(row=5, sticky=N, pady=10)

# withdraw
def witd_go():
    pin = temp_spin.get()
    amt = temp_samt.get()

    global notif3_
    notif3 = Label(withdraw_screen, font=('Calibri', 12))
    notif3_ = Label(withdraw_screen, font=('Calibri', 12))
    
    notif3.grid(row=6, sticky=N, pady=10)
    notif3_.grid(row=7, sticky=N, pady=10)
    
    if pin == "" or amt == "":
        notif3.config(fg="red", text="All fields required*")
    else:
        Custom.transaction('w', pin, amt)
    

def witd():
    global temp_spin
    global temp_samt
    temp_spin = StringVar()
    temp_samt = StringVar()

    # withdraw_screen
    global withdraw_screen
    withdraw_screen = Toplevel(atm_mode_screen)
    withdraw_screen.title("withdraw amount")
    
    Label(withdraw_screen, text="Please enter your pin and amount to be withdrawn", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(withdraw_screen, text="Pin", font=('Calibri', 12)).grid(row=2, sticky=W)
    Label(withdraw_screen, text="Amount", font=('Calibri', 12)).grid(row=3, sticky=W)
    
    # entries 
    Entry(withdraw_screen, textvariable=temp_spin).grid(row=2, column=1)
    Entry(withdraw_screen, textvariable=temp_samt).grid(row=3, column=1)
    
    # buttons
    Button(withdraw_screen, text="Submit", command = witd_go, font=("Calibri", 12)).grid(row=5, sticky=N, pady=10)
    
# status/ Balance-check
def stat_go():
    pin = temp_spin.get()

    global notif4_
    notif4 = Label(stat_screen, font=('Calibri', 12))
    notif4_ = Label(stat_screen, font=('Calibri', 12))
    
    notif4.grid(row=6, sticky=N, pady=10)
    notif4_.grid(row=7, sticky=N, pady=10)

    if pin == "":
        notif4.config(fg="red", text="field required*")
    else:
        Custom.transaction('s', pin)

def stat():
    global temp_spin
    temp_spin = StringVar()
    
    # bal_check_screen
    global stat_screen
    stat_screen = Toplevel(atm_mode_screen)
    stat_screen.title("Balance Check")
    
    Label(stat_screen, text="Please enter your pin", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(stat_screen, text="Pin", font=('Calibri', 12)).grid(row=2, sticky=W)
    
    # entries 
    Entry(stat_screen, textvariable=temp_spin).grid(row=2, column=1)

    # buttons
    Button(stat_screen, text="Submit", command = stat_go, font=("Calibri", 12)).grid(row=4, sticky=N, pady=10)
    

# finish register
def finish_reg():

    # finish_reg_screen
    finish_reg_screen = Toplevel(register_screen)
    finish_reg_screen.title("Success")

    name = temp_name.get().upper()
    age = temp_age.get()
    damt = temp_damt.get()
    if name=="" or age=="" or damt=="":
        notif.config(fg="red", text="All fields required*")
    else:
        acc_no = int(random.randint((10 ** 8), (10 ** 9)-1))
        pin = int(random.randint((10 ** 3), (10 ** 4)-1))
        Custom(acc_no, pin, name, age, damt)
        Label(finish_reg_screen, text="your account has been created. Thank you!", font=('Calibri', 14)).grid(row=0, sticky=N, pady=10)
        message = "YOUR ACCOUNT NUMBER: "+ str(acc_no) +"\nACCOUNT HOLDER: " + name + "\nPIN: " + str(pin)
        Label(finish_reg_screen, text=message, font=('Calibri', 14)).grid(row=1, sticky=N, pady=10)
        notif1 = Label(finish_reg_screen, font=('Calibri', 12))
        notif1.grid(row=6, sticky=N, pady=10)
        notif1.config(fg="red", text="WARNING! PLEASE DON'T SHARE YOUR PIN WITH ANYONE.")
        


# register mode function

def register():

    # vars
    global temp_name
    global temp_age
    global temp_damt
    global notif

    temp_name = StringVar()
    temp_age = StringVar()
    temp_damt = StringVar()

    # register screen 
    global register_screen
    register_screen = Toplevel(master)
    register_screen.title("Register")

    # labels
    Label(register_screen, text="Please enter your details below to register", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)

    Label(register_screen, text="Name", font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(register_screen, text="Age", font=('Calibri', 12)).grid(row=2, sticky=W)
    Label(register_screen, text="Deposit amt (>= 1000)", font=('Calibri', 12)).grid(row=3, sticky=W)
    # Label(register_screen, text="", font=('Calibri', 12)).grid(row=4, sticky=w, pady=10)
    notif = Label(register_screen, font=('Calibri', 12))
    notif.grid(row=6, sticky=N, pady=10)

    # entries
    Entry(register_screen, textvariable=temp_name).grid(row=1, column=1)
    Entry(register_screen, textvariable=temp_age).grid(row=2, column=1)
    Entry(register_screen, textvariable=temp_damt).grid(row=3, column=1)
    # Entry(register_screen, textvariable=name).grid(row=1, column=0)

    # button
    Button(register_screen, text="Register", command = finish_reg, font=("Calibri", 12)).grid(row=8, sticky=N, pady=10)

# atm_mode function
def atm():
    global atm_mode_screen
    # atm_mode screen
    atm_mode_screen = Toplevel(master)
    atm_mode_screen.title("Atm Mode")

    # labels
    Label(atm_mode_screen, text = "ATM-Mode", font=('Calibri', 14)).grid(row=0, sticky=N, pady=10)
    Label(atm_mode_screen, text = "select the option", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)


    # buttons
    Button(atm_mode_screen, text="Deposit", command = dep, font=("Calibri", 12), width=20).grid(row=2)
    Button(atm_mode_screen, text="Withdraw", command = witd, font=("Calibri", 12), width=20).grid(row=3)
    Button(atm_mode_screen, text="Balance Check", command = stat, font=("Calibri", 12), width=20).grid(row=4, sticky=N)



# exit mode
def exit():
    sys.exit()

# image
img = Image.open("pyBank_logo.png")
img = img.resize((250, 250))
img = ImageTk.PhotoImage(img)

# Labels
Label(master, text = "Automatic Teller Machine", font=('Calibri', 14)).grid(row=0, sticky=N, pady=10)
Label(master, image = img).grid(row=1, sticky=N, pady=15)

# Button
Button(master, text="Register", font=('Calibri', 12), width=20, command=register).grid(row=3)
Button(master, text="Atm Mode", font=('Calibri', 12), width=20, command=atm).grid(row=4)
Button(master, text="Exit", font=('Calibri', 12), width=20, command=exit).grid(row=5, sticky=N)

master.mainloop()
