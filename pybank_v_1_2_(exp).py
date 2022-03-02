''' Note: all ui & backend is present in this single file. Apologies for the clumbsy code.'''

# UI imports 
from tkinter import *
import os
from PIL import ImageTk, Image

# Python OOP 
# Back-end imports
import sys
import random
import sqlite3
from sqlite3 import Error

# extra imports
from twilio.rest import Client
import os

class Bank():

    # the sqlite database
    @staticmethod
    def create_connection(db_file):
        """ creates a db connection and returns connection object """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        
        return conn 

    # creates the table 
    @staticmethod
    def create_table(conn, create_table_sql):
        """ utility function for creating a table """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
        finally:
            c.close()
        
    
    @staticmethod
    def main():
        database = r"pysqlite.db"
        sql_create_bank_accounts = """ 
                                CREATE TABLE IF NOT EXISTS bank_accounts (
                                    account_no INTEGER,
                                    pin INTEGER, 
                                    name TEXT,
                                    age INTEGER,
                                    phone_no INTEGER, 
                                    balance REAL 
                                );
                            """ # Schema : acc_no, pin, name, age, phone_no, balance
        conn = Bank.create_connection(database)

        if conn is not None:
            Bank.create_table(conn, sql_create_bank_accounts)
        else:
            print("Error! cannot create the database connection.")
    
    @staticmethod
    def otp_opr(v_fl, phone_number=0, otp=0):
        account_sid = 'ACf30a1fed8d98a3f1576de13e511db950'
        auth_token = '2c3914ae241f4d9af34f5f7aaeb40089'
        client = Client(account_sid, auth_token)
        verify = client.verify.services('VA3f98da905f54dc5f728300d7321f6ef4')
        
        if v_fl == "send_otp":
            # print("sent otp")
            verify.verifications.create(to=phone_number, channel='sms')
            return
        elif v_fl == "match_otp":
            # print("matching otp")
            result = verify.verification_checks.create(to=phone_number, code=otp)
            return result.status

    def __init__(self, acc_no=None, pin=None, name=None, age=None, phone_no=None, balance=None):
        
        if(isinstance(self, Custom)): # creates a object for each new entry

            self.acc = acc_no
            self.pin = pin
            self.name = name
            self.age = age
            self.phone = phone_no
            self.bal = balance
            
            self.add2database(self.acc, self.pin, self.name, self.age, self.phone, self.bal)
            
    def add2database(self, acc, pin, name, age, phone, bal):
        """ this method inserts the data into the sqlite db """
        # print("in add2database...")
        
        # connecting to sqlite db
        conn = Bank.create_connection("pysqlite.db")
        
        # creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # query /insertion
        cursor.execute("INSERT INTO bank_accounts (account_no, pin, name, age, phone_no, balance) VALUES (?, ?, ?, ?, ?, ?)", (self.acc, self.pin, self.name, self.age, self.phone, self.bal)) 
        conn.commit()
        conn.close()
        
# whenever this application is started this get clicked and as you can see it call the main method (in the bank class) and creates the sql table.
if __name__ == '__main__':
    Bank.main() # as you can see that the main() function is defined inside the class 'Bank'. we have declared it as a @staticmethod decorator, so that we can call it outside the class without creating an object.


class Custom(Bank):
    # counter = 0
    # print("in Custom class")
    def __init__(self, acc_no, epin, name, age, phone_no, balance):
        # print("in Custom constructor")
        super().__init__(acc_no, epin, name, age, phone_no, balance)
        

    # transactions method.
    @staticmethod
    def transaction(fl, pin, amt=0):
        
        def checkPin(pin):
            conn = Bank.create_connection("pysqlite.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bank_accounts WHERE pin=?", (pin,)) 
            rows = cursor.fetchall()
            conn.close()
            if len(rows) == 0:
                return False
            return True

        def fetch(fl, pin):
            # connecting to sqlite db
            conn = Bank.create_connection("pysqlite.db")
            
            # creating a cursor object using the cursor() method
            cursor = conn.cursor()

            # fetching the data (i,e. row) from the database
            cursor.execute("SELECT * FROM bank_accounts WHERE pin=?", (pin,)) 

            rows = cursor.fetchall()
            conn.close()
            
            # returns the ac_number, ac_holder, ac_balance
            return rows[0][0], rows[0][2], rows[0][5]
            
        def updateBalance(pin, uamt):
            """ used for deposits and withdrawals """
            conn = Bank.create_connection("pysqlite.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE bank_accounts SET BALANCE = ? WHERE pin = ?", (uamt, pin))
            conn.commit()
            conn.close()

        # all else : msg is printed if pin not found in db

        # deposit opr
        if fl=='d':
            
            if(checkPin(pin)):
                # deposit message
                dep_msg_screen = Toplevel(master)
            
                ac_no, ac_name, curr_amt = fetch(fl, pin)
                upd_amt = int(curr_amt) + int(amt)
                updateBalance(pin, upd_amt)
                
                msg = "Transaction Successful" + "\nDeposited Rs." + str(amt) + " to Account Number: "+ str(ac_no) +", Account Holder: " + str(ac_name) + " New Balance: " + str(upd_amt)
                Label(dep_msg_screen, text=msg, font=('Calibri', 14)).grid(row=1, sticky=N, pady=10)
            else:
                notif2_.config(fg="red", text="Invalid PIN*")
        
        # withdraw opr
        elif fl=='w':
            
            if(checkPin(pin)):
                # witd screen
                witd_msg_screen = Toplevel(master)
            
                ac_no, ac_name, curr_amt = fetch(fl, pin)
                
                if int(amt) > int(curr_amt):
                    msg = "Insuffient Balance! Sorry you can't make that! your current balance is: " + str(curr_amt)
                    Label(witd_msg_screen, text=msg, font=('Calibri', 14)).grid(row=1, sticky=N, pady=10)
                    return

                upd_amt = int(curr_amt) - int(amt)
                updateBalance(pin, upd_amt)

                # withdraw message
                msg = "Transaction Successful" + "\nRs." + str(amt) + " withdrawn from Account Number: "+ str(ac_no) +", Account Holder: " + str(ac_name) + " New Balance: " + str(upd_amt)
                Label(witd_msg_screen, text=msg, font=('Calibri', 14)).grid(row=1, sticky=N, pady=10)
            else:
                notif3_.config(fg="red", text="Invalid PIN*")
                
        # status opr
        elif fl == 's':
            
            if(checkPin(pin)):
                # balance-check screen
                bal_chk_msg_screen = Toplevel(master)
            
                ac_no, ac_name, curr_amt = fetch(fl, pin)
                # bal check msg
                msg = "Account Number: " + str(ac_no) + "\nAccount Holder: " + str(ac_name) + "\nNew Balance: " + str(curr_amt)
                Label(bal_chk_msg_screen, text=msg, font=('Calibri', 14)).grid(row=1, sticky=N, pady=10)
            else:
                notif4_.config(fg="red", text="Invalid PIN*")

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
        deposit_screen.destroy()
        Custom.transaction('d', pin, amt)
        

# deposit
def dep():
    global temp_spin
    global temp_samt
    temp_spin = StringVar()
    temp_samt = StringVar()

    # deposit_screen
    global deposit_screen
    deposit_screen = Toplevel(master)
    deposit_screen.title("deposit amount")
    
    Label(deposit_screen, text="Please enter your pin and deposit amount", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(deposit_screen, text="Pin", font=('Calibri', 12)).grid(row=2, sticky=W)
    Label(deposit_screen, text="Amount", font=('Calibri', 12)).grid(row=3, sticky=W)
    
    # entries 
    Entry(deposit_screen, textvariable=temp_spin, show="*").grid(row=2, column=1)
    Entry(deposit_screen, textvariable=temp_samt).grid(row=3, column=1)
    
    # buttons
    Button(deposit_screen, text="Submit", command = lambda:[dep_go()], font=("Calibri", 12)).grid(row=5, sticky=N, pady=10)

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
        withdraw_screen.destroy()
        Custom.transaction('w', pin, amt)
    
def witd():
    global temp_spin
    global temp_samt
    temp_spin = StringVar()
    temp_samt = StringVar()

    # withdraw_screen
    global withdraw_screen
    withdraw_screen = Toplevel(master)
    withdraw_screen.title("withdraw amount")
    
    Label(withdraw_screen, text="Please enter your pin and amount to be withdrawn", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(withdraw_screen, text="Pin", font=('Calibri', 12)).grid(row=2, sticky=W)
    Label(withdraw_screen, text="Amount", font=('Calibri', 12)).grid(row=3, sticky=W)
    
    # entries 
    Entry(withdraw_screen, textvariable=temp_spin, show="*").grid(row=2, column=1)
    Entry(withdraw_screen, textvariable=temp_samt).grid(row=3, column=1)
    
    # buttons
    Button(withdraw_screen, text="Submit", command = lambda:[witd_go()], font=("Calibri", 12)).grid(row=5, sticky=N, pady=10)
    
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
        stat_screen.destroy()
        Custom.transaction('s', pin)

def stat():
    global temp_spin
    temp_spin = StringVar()
    
    # bal_check_screen
    global stat_screen
    stat_screen = Toplevel(master)
    stat_screen.title("Balance Check")
    
    Label(stat_screen, text="Please enter your pin", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(stat_screen, text="Pin", font=('Calibri', 12)).grid(row=2, sticky=W)
    
    # entries 
    Entry(stat_screen, textvariable=temp_spin, show="*").grid(row=2, column=1)

    # buttons
    Button(stat_screen, text="Submit", command = lambda:[stat_go()], font=("Calibri", 12)).grid(row=4, sticky=N, pady=10)

    
# finish register
def finish_reg():

    name = temp_name.get().upper()
    age = temp_age.get()
    phone = temp_phone.get()
    damt = temp_damt.get()    
    
    if damt == "":
        fv_notif.config(fg="red", text="enter amount")
        return
    finish_verify_screen.destroy()
    # finish_register_screen
    finish_reg_screen = Toplevel(master)
    finish_reg_screen.title("Success")

    ac_gen = "43518733" +  str(random.randrange(10 ** 3, (10 ** 4)-1))
    acc_no = int(ac_gen)
    pin = int(random.randint((10 ** 3), (10 ** 4)-1))
    Custom(acc_no, pin, name, age, phone, damt)

    Label(finish_reg_screen, text="your account has been created. Thanks for using PyBank!", font=('Calibri', 14)).grid(row=0, sticky=N, pady=10)
    message = "Your Account Number: "+ str(acc_no) +"\nAccount Holder: " + name + "\nPhone: "+ phone +"\nPin: " + str(pin)
    Label(finish_reg_screen, text=message, font=('Calibri', 14)).grid(row=1, sticky=N, pady=10)
    notif1 = Label(finish_reg_screen, font=('Calibri', 12))
    notif1.grid(row=6, sticky=N, pady=10)
    notif1.config(fg="red", text="WARNING! PLEASE DON'T SHARE YOUR PIN WITH ANYONE.")


# finish verification
def finish_verify():

    global temp_damt
    temp_damt = StringVar()
    phone = temp_phone.get()
    in_otp = temp_otp.get() 
    
    if in_otp == "":
        vnotif.config(fg="red", text="required*")
        return
    ap = "+91"+phone
    
    result =  Bank.otp_opr("match_otp", phone_number = ap, otp = in_otp)

    if result != "approved":
        vnotif.config(fg="red", text="invalid*")
        return
    
    verify_screen.destroy()
    global finish_verify_screen
    # finish_verify_screen
    # Label(register_screen, text="Deposit amt (>= 1000)", font=('Calibri', 12)).grid(row=4, sticky=W)
    finish_verify_screen = Toplevel(master)
    finish_verify_screen.title("Verified Successfully")

    # labels
    Label(finish_verify_screen, text="phone number verified successfully", font=('Calibri', 8)).grid(row=0, sticky=W)
    Label(finish_verify_screen, text="please enter amount to be deposited", font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(finish_verify_screen, text="Deposit amt (>= 1000)", font=('Calibri', 12)).grid(row=2, sticky=W)
    
    # fv_notif
    global fv_notif
    fv_notif = Label(finish_verify_screen, font=('Calibri', 12))
    fv_notif.grid(row=4, sticky=N, pady=10)

    # entries
    Entry(finish_verify_screen, textvariable=temp_damt).grid(row=2, column=1)

    # buttons
    Button(finish_verify_screen, text="Deposit", command = lambda:[finish_reg()], font=("Calibri", 12)).grid(row=6, sticky=N, pady=10)
    

def verify():
    
    global temp_otp
    temp_otp = StringVar()

    name = temp_name.get().upper()
    age = temp_age.get()
    phone = temp_phone.get()
    
    if name=="" or age=="" or phone=="":
        notif.config(fg="red", text="All fields required*")
        return
    if len(phone) != 10:
        notif.config(fg="red", text="Enter a valid 10-digit phone number.*")
        return

    # appending india code "+91" 
    ap = "+91"+phone
    try:
        Bank.otp_opr("send_otp", phone_number = ap)
    except :
        print("in except")
        emsg = "entered phone number is invalid */ if it is a valid, there might be a api problem. please try after some time. Sorry for the inconvenience"
        notif.config(fg="red", text=emsg)
        return

    register_screen.destroy()
    global verify_screen
    # phone_verify screen
    verify_screen = Toplevel(master)
    
    # labels
    v_msg = "Please enter the 6-digit OTP sent to " + str(phone) + " to verify your Identity"
    Label(verify_screen, text=v_msg, font=('Calibri', 12)).grid(row=1, sticky=W)

    Label(verify_screen, text="OTP", font=('Calibri', 12)).grid(row=3, sticky=W)

    global vnotif
    vnotif = Label(verify_screen, font=('Calibri', 12))
    vnotif.grid(row=3, sticky=N, pady=10)

    # entries
    Entry(verify_screen, textvariable=temp_otp).grid(row=3, column=1)

    # button
    Button(verify_screen, text="Register", command = lambda:[finish_verify()], font=("Calibri", 12)).grid(row=5, sticky=N, pady=10)


# register mode function
def register():

    # vars
    global temp_name
    global temp_age
    global temp_phone
    
    global notif

    temp_name = StringVar()
    temp_age = StringVar()
    temp_phone = StringVar()
    

    # register screen 
    global register_screen
    register_screen = Toplevel(master)
    register_screen.title("Register")

    # labels
    Label(register_screen, text="Please enter your details below to register", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)

    Label(register_screen, text="Name", font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(register_screen, text="Age", font=('Calibri', 12)).grid(row=2, sticky=W)
    Label(register_screen, text="Phone Number", font=('Calibri', 12)).grid(row=3, sticky=W)

    
    notif = Label(register_screen, font=('Calibri', 12))
    notif.grid(row=6, sticky=N, pady=10)

    # entries
    Entry(register_screen, textvariable=temp_name).grid(row=1, column=1)
    Entry(register_screen, textvariable=temp_age).grid(row=2, column=1)
    Entry(register_screen, textvariable=temp_phone).grid(row=3, column=1)
    # Entry(register_screen, textvariable=temp_damt).grid(row=4, column=1)
    
    # button
    Button(register_screen, text="Register", command = lambda:[verify()], font=("Calibri", 12)).grid(row=8, sticky=N, pady=10)


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
    Button(atm_mode_screen, text="Deposit", command = lambda:[dep(), atm_mode_screen.destroy()], font=("Calibri", 12), width=20).grid(row=2)
    Button(atm_mode_screen, text="Withdraw", command = lambda:[witd(), atm_mode_screen.destroy()], font=("Calibri", 12), width=20).grid(row=3)
    Button(atm_mode_screen, text="Balance Check", command = lambda:[stat(), atm_mode_screen.destroy()] , font=("Calibri", 12), width=20).grid(row=4, sticky=N)

# exit mode
def exit():
    sys.exit()

# main screen

master = Tk()
master.title("Banking App")

master.state('zoomed')
# master.eval(f'tk::PlaceWindow . center')
# master.attributes('-fullscreen', True)
master.resizable(False, False)  # This code helps to disable windows from resizing

window_height = 500
window_width = 900

screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


# Main page #

# image
img = Image.open("pyBank_logo.png")
img = img.resize((250, 250))
img = ImageTk.PhotoImage(img)

# Labels
Label(master, text = "Automatic Teller Machine", font=('Calibri', 14)).grid(row=0, sticky=N, pady=10)
Label(master, image = img).grid(row=1, sticky=N, pady=15)

# Buttons
Button(master, text="Register", font=('Calibri', 12), width=20, command=register).grid(row=3)
Button(master, text="Atm Mode", font=('Calibri', 12), width=20, command=atm).grid(row=4)
Button(master, text="Exit", font=('Calibri', 12), width=20, command=exit).grid(row=5, sticky=N)

master.columnconfigure(0, weight=1)
master.rowconfigure(0, weight=0)

master.mainloop()