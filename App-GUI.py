#!/usr/bin/env python3
# Librariye
import uuid
from datetime import datetime
import threading
import time
import os

from functools import partial
from tkinter import *
from DB import *
# Application code


class App:
    def __init__(self, db):
        self.db = db
        usr = db.d["User"]
        self.users = []
        self.logedin = None
        self.acc = None  ## The bank account that is using in acc_menu.
       # self.admin = Admin("Admin","3248","admin","09370548316","admin@yandex.com",None)
        pass

    def register_new_user(self, name, national_code, password, phone_num, email,top):
        name, national_code, password, phone_num, email = name.get(), national_code.get(), password.get(), phone_num.get(), email.get()

        now = datetime.now()
        joined_at = now.strftime("%d/%m/%y|%H:%M:%S")

        self.users.append(User(name, national_code, password, phone_num, email,joined_at))
        val = [name, national_code, password, phone_num, email,joined_at]
        q = "INSERT INTO User VALUES (" + name + "," + national_code + "," + password + "," + phone_num + "," + email + "," + joined_at + ");"
        query = Query(self.db, q)
        query.parsing()

        top.destroy()

    def login(self, nc, password,top):
        nc = nc.get()
        password = password.get()
        q = 'SELECT FROM User WHERE national_code=='+ '"' + nc + '"' + ';'
        query = Query(self.db, q)
        f = query.parsing()
        if(len(f)):
            f = f[0]
            if(f[2] == password):
                print("You Logged in!")
                top.destroy()
                self.logedin = User(f[0],f[1],f[2],f[3],f[4],f[5])
                self.user_menu()
            else:
                x = "Wrong password!"
                lb = Label(top, text = x ).pack()
        else:
            x = "There is no account with this national code. :) "
            lb = Label(top, text = x ).pack()
        return False

        pass



    #####
    #####
    #####MAIN MENU
    def main_menu(self):
        ####
        root = Tk()
        root.title("GNUBank")
        main_frame = LabelFrame(root,text = "Main Menu")
        main_frame.pack()
        ######
        ######Functions for options
        ######
        def op1():
            #### l in variables means label
            #### e in variables means entry
            #### for example lnc is lable for nc
            top = Toplevel()
            top.title("Login as user")
            print("Please enter your national code and password:")
            lnc = Label(top, text = "National Code: ").pack()
            enc = Entry(top)
            enc.pack()
            lpassword = Label(top, text = "Password: ").pack()
            epassword = Entry(top, show = "*")
            epassword.pack()

            logbtn = Button(top, text = "Login!",command = partial(self.login, enc, epassword,top)).pack()

            #user = app.login(nc,password)
            #if(user):
            #    self.user_menu() '''
            top.mainloop()
        def op2():

            top = Toplevel()
            top.title("Sign up")



            lname = Label(top, text = "Name: ").pack()
            ename = Entry(top)
            ename.pack()

            lnc = Label(top, text = "National Code: ").pack()
            enc = Entry(top)
            enc.pack()

            lpassword = Label(top, text = "Password: ").pack()
            epassword = Entry(top, show = "*")
            epassword.pack()

            lphone = Label(top, text = "Phone Number: ").pack()
            ephone = Entry(top)
            ephone.pack()

            lemail = Label(top, text = "Email: ").pack()
            eemail = Entry(top)
            eemail.pack()

            signbtn = Button(top, text = "Sign Up!",command = partial(app.register_new_user,ename,enc,epassword,ephone,eemail,top)).pack()


        def op3():
            password = input("Please enter your password: ")
            if(password == self.admin.password):
                print("Dear Admin!\t You successfully logged in!")
                self.admin_menu()
            else:
                print("Wrong password!\t Don't try more if you're not the admin dude!")


        but1 = Button(main_frame, text ="Login as user", pady = 50 , width = 30, command = op1)
        but1.pack()
        but2 = Button(main_frame, text ="Sign up", pady = 50 , width = 30 , command = op2 )
        but2.pack()
        but3 = Button(main_frame, text ="Login as admin", pady = 50 , width = 30, command = op3 )
        but3.pack()
        but4 = Button(main_frame, text ="Exit", pady = 50 , width = 30 , command = exit )
        but4.pack()
        
        
        root.mainloop()

    ########
    ########
    ########USER MENU
    ########
    ########
    def user_menu(self):
        ###
        root = Tk()
        root.title("User Panel")
        user_frame = LabelFrame(root,text = "User Menu")
        user_frame.pack()
        ######
        ######Functions for options
        ######
        def op1():
            #### l in variables means label
            #### e in variables means entry
            #### for example lnc is lable for nc
            top = Toplevel()
            top.title("Open new account")

            lb = Label(top, text = "Please enter a password and alias for your account:").pack()
            lpass = Label(top, text = "Password").pack()
            epass = Entry(top, show = "*")
            epass.pack()
            lalias = Label(top, text = "Alias").pack()
            ealias = Entry(top)
            ealias.pack()
            btn = Button(top, text = "Done!",command = partial(self.logedin.opening_acc, epass, ealias,top)).pack()
            top.mainloop()

        def op2():
            top = Toplevel()
            top.title("Show & Use my accounts")
            self.logedin.show_acc(top,self.logedin)
            top.mainloop()

        def op3():
            top = Toplevel()
            top.title("Favorites accounts")
            lb = Label(top, text = "Please enter an acount number and type an alias for that: ").pack()

            lac = Label(top, text = "Account Number").pack()
            eac = Entry(top, show = "*")
            eac.pack()
            lal = Label(top, text = "Alias").pack()
            eal = Entry(top)
            eal.pack()

            btn = Button(top, text = "Done!",command = partial(self.logedin.fav_acc,eac,eal,top)).pack()

            top.mainloop()

        def op4():
            self.logedin = None
            root.destroy()
            
        but1 = Button(user_frame, text ="Open new account", pady = 50 , width = 30, command = op1)
        but1.pack()
        but2 = Button(user_frame, text ="Show & Use my accounts", pady = 50 , width = 30 , command = op2 )
        but2.pack()
        but3 = Button(user_frame, text ="Favorites accounts", pady = 50 , width = 30, command = op3 )
        but3.pack()
        but4 = Button(user_frame, text ="Logout", pady = 50 , width = 30 , command = op4 )
        but4.pack()
        
        root.mainloop()
    
    #######
    #######
    #######ACC MENU
    #######
    def acc_menu(self):
        ###
        root = Tk()
        root.title("Bank Account Panel")
        user_frame = LabelFrame(root,text = "Bank Account Menu")
        user_frame.pack()
        ######
        ######Functions for options
        ######

        def op1():
            top = Toplevel()
            top.title("Transfer Money")

            lb = Label(top, text = "Please enter the account number of reciever or the alias you choosed before and the amount of money you want to transfer:").pack()
            

            lalias = Label(top, text = "Alias").pack()
            ealias = Entry(top)
            ealias.pack()

            lacc = Label(top, text = "Account Number").pack()
            eacc = Entry(top)
            eacc.pack()

            lmoney = Label(top, text = "Money").pack()
            emoney = Entry(top)
            emoney.pack()


            lpass = Label(top, text = "Password").pack()
            epass = Entry(top, show = "*")
            epass.pack()

            btn = Button(top, text = "Done!",command =partial(self.acc.transfer,eacc,emoney,ealias,epass,top)).pack()


        def op2():

            self.acc.show_transaction()


        def op3():
            top = Toplevel()
            top.title("Bill Payment")


            lbill_pay = Label(top, text = "Bill number").pack()
            ebill_pay = Entry(top)
            ebill_pay.pack()

            lpay_num = Label(top, text = "Paymnet Number").pack()
            epay_num = Entry(top)
            epay_num.pack()

            lbill_amount = Label(top, text = "Amount of bill(Be Honest Please!)").pack()
            ebill_amount = Entry(top)
            ebill_amount.pack()

            btn = Button(top, text = "Done!",command =partial(self.acc.pay_bill,ebill_amount,top)).pack()
 

        def op4():
            top = Toplevel()
            top.title("Apply for loan")

            lmoney = Label(top, text = "How much money you want to request for the lone:").pack()
            emoney = Entry(top)
            emoney.pack()
            btn = Button(top, text = "Done!",command =partial(self.acc.active_loan,emoney,top)).pack()
            top.mainloop()

        def op5():
            self.acc.close_acc()

            root.destroy()
        def op6():
            self.acc = None
            root.destroy()

        but1 = Button(user_frame, text ='Transfer money', pady = 50 , width = 30, command = op1)
        but1.pack()
        but2 = Button(user_frame, text ='Show Transaction', pady = 50 , width = 30 , command = op2 )
        but2.pack()
        but3 = Button(user_frame, text ='Bill payment', pady = 50 , width = 30, command = op3 )
        but3.pack()
        but4 = Button(user_frame, text ='Apply for loan', pady = 50 , width = 30 , command = op4 )
        but4.pack()
        but5 = Button(user_frame, text ='Close account', pady = 50 , width = 30, command = op5 )
        but5.pack()
        but6 = Button(user_frame, text ='Back', pady = 50 , width = 30 , command = op6 )
        but6.pack()
        
        pass

    ######
    ######
    ######ADMIN MENU
    ######
    ######
    def admin_menu(self):
        menu_options = {1: 'Show users information', 2: 'Edit users information', 3: 'Change bank account balances', 4: 'Open a bank account', 5: 'Close a bank account', 6: 'Logout'}
        while(True):
            for key in menu_options.keys():
                print(key, "-", menu_options[key])
            try:
                option = int(input("Please type the number of option: "))
            except:
                print("You should enter a number!")
            if(option == 1):
                name = input("Name: ")
                nc = input("National Code: ")
                password = input("Password: ")
                phone = input("Phone: ")
                email = input("Email: ")
                joined_at = input("Joined at(in this formnat '%d/%m/%y|%H:%M:%S'): ")
                l = [name, nc , password, phone, email, joined_at]
                attr = ["name", "national_code", "password", "phone", "email", "joined_at"]
                self.admin.show_users(l,attr)

            elif(option == 2):
                nc = input("Please enter the national code of the user you want to edit: ")
                print("Now complete these infromations(or if you want don't want change a part leave it blank): ")
                name = input("Name: ")
                ncc = input("National Code: ")
                password = input("Password: ")
                phone = input("Phone: ")
                email = input("Email: ")
                joined_at = input("Joined at(in this formnat '%d/%m/%y|%H:%M:%S'): ")
                l = [name, ncc , password, phone, email, joined_at]
                attr = ["name", "national_code", "password", "phone", "email", "joined_at"]
                self.admin.edit_users(nc,l)


            elif(option == 3):
                ac = input("Please enter the account number you want to change the balance: ")
                bl = input("Type the balance you want: ")
                self.admin.change_balance(ac,bl)

            elif(option == 4):
                nc = input("Please enter the national code of the person you want to open an account for him/her: ")
                password = input("Enter a password for account: ")
                alias = input("Enter an alias for account: ")
                self.admin.opening_acc(nc,password,alias)
                pass
            elif(option == 5):
                a = input("Please enter the account number you want to close: ")
                self.admin.close_acc(a)

            elif(option == 6):
                self.logedin = None
                break
        return 0
        pass
        pass

class User:
    def __init__(self,name, national_code, password, phone_num, email,joined_at):
        self.name = name
        self.national_code = national_code
        self.password = password
        self.phone_num = phone_num
        self.email = email
        self.joined_at = joined_at
        self.idd = None
        self.db = db
        global app
        self.app = app
        self.ba = []  # list of bank accounts user have

    def opening_acc(self,password,alias,top = None):
        password = password.get()
        alias = alias.get()
        acc = str(uuid.uuid4().int)[:16]
        q = "INSERT INTO Bank_acc VALUES (" + acc + "," + str(0) + "," + self.national_code + "," + password + "," + alias + ");"
        query = Query(db, q)
        query.parsing()
        top.destroy()
        pass
    def show_acc(self,top = None,logedin = None):

        def set_acc(en):
            self.app.acc = Bank_acc(accs[int(en.get())-1][0],accs[int(en.get())-1][1],accs[int(en.get())-1][2],accs[int(en.get())-1][3],accs[int(en.get())-1][4])
            top.destroy()
            self.app.acc_menu()
            
        q = "SELECT FROM Bank_acc WHERE owner_nc==" + '"' + self.national_code + '"' + ";"
        query = Query(self.db, q)
        accs = query.parsing()

        if(len(accs) == 0):
            lb = Label(top, text = "You don't have any account. You should open an account :)").pack()
            btn = Button(top, text = "Back",command = top.destroy).pack()
        else:
            for i in range(len(accs)):
                lb = Label(top, text = "----------" + str(i+1) + "--------").pack()
                
                lb = Label(top, text = "Account Number:" + str(accs[i][0])).pack()
                lb = Label(top, text = "Balance: " + str(accs[i][1])).pack()
                lb = Label(top, text = "Alias: " + str(accs[i][4])).pack()
                lb = Label(top, text = "------------------").pack()

            ln = Label(top, text = "Enter the number of account you want to work with: ").pack()
            en = Entry(top)
            en.pack()

            btn = Button(top, text = "Done!",command = partial(set_acc,en)).pack()

        top.mainloop()
    def fav_acc(self,ac,al,top):
        ac = ac.get()
        al = al.get()
        q = "INSERT INTO Fav_acc VALUES (" + self.national_code + "," + str(ac) + "," + al + ");"
        query = Query(self.db, q)
        query.parsing()
        print("Successfulyy added to your favorite list!")
        top.destroy()

    def __repr__(self):
        return("Name" + ":" + self.name + self.national_code + self.password + self.phone_num + self.email)

class Admin(User):
    def __init__(self,name, national_code, password, phone_num, email,joined_at):
        User.__init__(self,name, national_code, password, phone_num, email,joined_at)
        #super().__init__()
    def show_users(self,l,attr):
        cond = []
        for i in range(len(l)):
            if(l[i] != ""):
                cond.append(attr[i] + "==" + '"' + l[i] +'"')
        sc = " AND ".join(cond) # string of conditions
        if(sc ==""):
            sc = "True==True;"
        else:
            sc = sc + ";"
        q = "SELECT FROM User WHERE " + sc
        print(q)
        query = Query(self.db, q)

        users = query.parsing()
        for u in users:
            print("-----------------------")
            print("Name: " + u[0])
            print("National Code: " + u[1])
            print("Password: " + u[2])
            print("Phone Number: " + u[3])
            print("Email: " + u[4])
            print("Joined at: " + u[5])
            print("-----------------------")
    def edit_users(self,nc,l):
        q = "SELECT FROM User WHERE national_code==" + '"' + nc + '"' + ";"
        print(q)
        query = Query(self.db, q)
        a = query.parsing()
        print(a)
        atr = ["acc", "balance", "owner_nc", "password", "alias"]
        z = ""
        if(len(a) == 0):
            print("There isn't any bank account with this national code!")
        elif(len(a) == 1):
            a = a[0]
            print(l)
            for i in range(len(a)-1):
                if(l[i] == ""):
                    z += '"' +  a[i] + '"' + ","
                else:
                    z += '"' +  l[i] + '"' + ","
        v = "(" + z[:-1] + ")"
        nc = '"' + nc + '"'
        q = "UPDATE User WHERE national_code==" + nc + " VALUES " + v + ";"
        query = Query(self.db, q)
        query.parsing()

    def change_balance(self,ac,balance):
        q = "SELECT FROM Bank_acc WHERE acc==" + ac + ";"
        query = Query(self.db, q)
        acc = query.parsing()
        if(len(acc) == 0):
            print("There isn't any bank account with this account number!")
        else:
            acc = acc[0]
            q = "UPDATE Bank_acc WHERE acc==" + ac + " VALUES " + "(" + str(acc[0]) + "," + balance + "," + '"' + acc[2] + '"' + "," + '"' + acc[3] + '"' + "," + '"' + acc[4] + '"' + ");"
            query = Query(self.db, q)
            query.parsing()

    def opening_acc(self,nc,password,alias):

        q = "SELECT FROM User WHERE national_code==" + '"' + nc + '"' + ";"
        query = Query(self.db, q)
        u = query.parsing()
        u = u[0]
        self.logedin = User(u[0],u[1],u[2],u[3],u[4],u[5])
        self.logedin.opening_acc(password,alias)

    def close_acc(self,acc):
        q = "SELECT FORM Bank_acc WHERE acc==" + acc + ";"
        query = Query(self.db, q)
        a = query.parsing()
        a = a[0]
        self.acc = Bank_acc(a[0],a[1],a[2],a[3],a[4])
        if(int(self.acc.balance) == 0):
            q = "DELETE FROM Bank_acc WHERE acc==" + str(self.acc.acc) + ";"
            query = Query(self.db,q)
            query.parsing()
        else:
            reciever = input("Please enter an acount number for transfering your money before close it:\n")
            self.acc.transfer(reciever,int(self.acc.balance))
            q = "DELETE FROM Bank_acc WHERE acc==" +  str(self.acc.acc)  + ";"
            query = Query(self.db,q)
            query.parsing()
        self.acc = None

class Bank_acc:
    def __init__(self,acc,balance,owner_nc,password,alias):
        self.acc = acc
        self.balance = balance
        self.owner_nc = owner_nc
        self.password = password
        self.alias = alias
        self.app = app
        self.db = db
        pass
    def transfer(self,reciever,money,fav = None,password = None,top = None):
        reciever = reciever.get()
        if(type(money) == str):    
            money = int(money)
        else:
            money = int(money.get())

        if(fav != None or fav != ""):
            fav = fav.get()
        if(password != None):
            password = password.get()
        if(password == self.password):

            if(fav != ""):
                q = "SELECT FROM Fav_acc WHERE owner_nc=="  + '"' + str(self.owner_nc) + '"'  + " AND " + "alias==" + '"' + fav + '"' + ";"
                query = Query(self.db,q)
                z = query.parsing()
                reciever = str(z[0][1])

           
            q = "SELECT FROM Bank_acc WHERE acc=="  + reciever  + ";"
            query = Query(self.db,q)
            z = query.parsing()
            if(len(z) == 0):
                x = "There isn't any account with this account number you entered!"
                lb = Label(top, text = x ).pack()
                return 0
            else:
                if(int(self.balance) > int(money)):
                    self.balance = int(self.balance)
                    self.balance -= int(money)
                    q = "UPDATE Bank_acc WHERE acc=="  + str(self.acc)  + " VALUES (" + str(self.acc) + ","+ str(self.balance) + "," + self.owner_nc + "," + self.password + "," + self.alias + ");"
                    query = Query(self.db,q)
                    query.parsing()
                    #######
                    z = z[0]
                    z[1] = str(int(z[1]) + money)
                    q = "UPDATE Bank_acc WHERE acc==" + reciever  + " VALUES (" + str(z[0]) + ","+ str(z[1]) + "," + z[2] + "," + z[3] + "," + z[4] + ");"
                    query = Query(self.db,q)
                    query.parsing()
                    ####Tranaction log
                    ####Tranaction log
                    now = datetime.now()
                    t = now.strftime("%d/%m/%y|%H:%M:%S")
                    q = "INSERT INTO Transaction VALUES (" + str(self.acc) + "," + reciever + "," + str(money) + "," + str(self.balance)  +  "," + t + ");"
                    query = Query(self.db,q)
                    query.parsing()
                    top.destroy()
                else:
                    x = "You Don't have enough money!"
                    lb = Label(top, text = x ).pack()
               

            
        else:
        
            x = "Wrong Password!"
            lb = Label(top, text = x ).pack()

    def pay_bill(self,money,top):
        money = money.get()
        if(self.balance > int(money)):
            self.balance = int(self.balance)
            self.balance -= int(money)
            q = "UPDATE Bank_acc WHERE acc==" + str(self.acc)  + " VALUES (" + str(self.acc) + ","+ str(self.balance) + "," + self.owner_nc + "," + self.password + "," + self.alias + ");"
            print(q)
            query = Query(self.db,q)
            query.parsing()
            ####Tranaction log
            now = datetime.now()
            t = now.strftime("%d/%m/%y|%H:%M:%S")
            q = "INSERT INTO Transaction VALUES (" + str(self.acc) + "," + "666" + "," + str(money) + "," + str(self.balance)  + "," + t + ");"  ### 666 is the code for bill payment
            query = Query(self.db,q)
            query.parsing()
            top.destroy()

        else:
            x = "You don't have enough money!"
            lb = Label(top, text = x ).pack()
            

    def active_loan(self,money,top):
        money = money.get()
        thread = threading.Thread(target = self.loan , args = (money,), daemon = True)
        thread.start()
        top.destroy()


    def loan(self,money,n = 12 , interval = 20):
        self.balance = int(self.balance)
        self.balance += int(money)
        q = "UPDATE Bank_acc WHERE acc==" +  str(self.acc)  + " VALUES (" + str(self.acc) + ","+ str(self.balance) + "," + self.owner_nc + "," + self.password + "," + self.alias + ");"
        query = Query(self.db,q)
        query.parsing()
        ### Transaction log
        now = datetime.now()
        t = now.strftime("%d/%m/%y|%H:%M:%S")
        q = "INSERT INTO Transaction VALUES (" + "333" + "," + str(self.acc) + "," + str(int(money)) + "," + str(self.balance) + "," + t  + ");"  ### 333 is the code for loaning
        query = Query(self.db,q)
        query.parsing()
        for i in range(n):
            self.balance -= int(money)//n
            q = "UPDATE Bank_acc WHERE acc==" + str(self.acc)  + " VALUES (" + str(self.acc) + ","+ str(self.balance) + "," + self.owner_nc + "," + self.password + "," + self.alias + ");"
            time.sleep(20)
            query = Query(self.db,q)
            query.parsing()
            ####Tranaction log
            now = datetime.now()
            t = now.strftime("%d/%m/%y|%H:%M:%S")
            q = "INSERT INTO Transaction VALUES (" + str(self.acc) + "," + "333" + "," + str(int(money)//n) + "," + str(self.balance) + "," + t  + ");"  ### 333 is the code for loaning
            query = Query(self.db,q)
            query.parsing()

    def show_transaction(self):
        top = Toplevel()
        top.title("Transactions")
        q = "SELECT FROM Transaction WHERE sender==" + str(self.acc)  + " OR " + "reciever==" +  str(self.acc)  + ";"
        query = Query(self.db,q)
        l = query.parsing()
        for ll in l:
            if(ll[0] == self.acc):
                if(ll[1] == 666):
                    x = "You with this account number: " +  str(self.acc) + " paid for bill $"  + str(ll[2]) + " in this time: " + str(ll[4]) + " & Your balance: $" + str(ll[3])
                    lb = Label(top, text = x ).pack()
                elif(ll[1] == 333):
                    x = "You with this account number: " +  str(self.acc) + " paid back for loaning $"  + str(ll[2]) + " in this time: " + str(ll[4]) + " & Your balance: $" + str(ll[3])
                    lb = Label(top, text = x ).pack()
                else:
                    x = "You with this account number: " +  str(self.acc) + " sent $"  + str(ll[2])  + " to this account number :" + str(ll[1]) + " in this time: " + str(ll[4]) + " & Your balance: $" + str(ll[3])
                    lb = Label(top, text = x ).pack()
            else:
                if(ll[1] == self.acc):
                    if(ll[0] == 333):
                        x =  "You with this account number: "  +  str(self.acc)  +  " recieved $"   +  str(ll[2]) +  " for your loan request. "  +  " in this time: "  + str(ll[4])  + " & Your balance: $"  + str(ll[3])
                        lb = Label(top, text = x ).pack()
                    else:
                        x = "You with this account number: "  +  str(self.acc)  +  " recieved $"   +  str(ll[2]) +  " from this account number :"  + str(ll[0])  +  " in this time: "  + str(ll[4])  + " & Your balance: $"  + str(ll[3])
                        lb = Label(top, text = x ).pack()
        btn = Button(top, text = "Back",command = top.destroy).pack()
        top.mainloop() 

    def close_acc(self):
        if(int(self.balance) == 0):

            q = "DELETE FROM Bank_acc WHERE acc==" + str(self.acc) + ";"
            query = Query(self.db,q)
            query.parsing()
        else:
            top = Toplevel()
            top.title("Close Account")
            lreciever = Label(top, text = "Please enter an acount number for transfering your money before close it:").pack()
            ereciever = Entry(top)
            ereciever.pack()

            btn = Button(top, text = "Done!",command =partial(self.app.acc.transfer,ereciever,str(self.app.acc.balance),None)).pack()
            #self.transfer(reciever,int(self.balance))
            q = "DELETE FROM Bank_acc WHERE acc==" +  str(self.acc)  + ";"
            query = Query(self.db,q)
            query.parsing()
            top.mainloop()

# Main code
###
if(__name__ == "__main__"):
###########
    bank_acc = None
    db = DB()
    db.inup()
    app = App(db)
    #####
    #####
    #app.main_menu()
    x = threading.Thread(target = app.main_menu , args = ())
    x.start()
