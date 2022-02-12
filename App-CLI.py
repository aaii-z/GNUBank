#!/usr/bin/env python3
### Written by AAII
### UNDER GPL3 License
### GITHUB PAGE : https://github.com/aaii-z
# Librariye
import uuid
from datetime import datetime
import threading
from pyfiglet import Figlet
import time
import os
from DB import *
# Application code

class App:
    def __init__(self, db):
        self.db = db
        usr = db.d["User"]
        self.users = []
        self.logedin = None
        self.acc = None  ## The bank account that is using in acc_menu.
        self.admin = Admin("Admin","3248","admin","09370548316","admin@yandex.com",None)
        for x in usr:
            self.users.append(User(x[0],x[1],x[2],x[3],x[4],x[5]))

        pass

    def register_new_user(self, name, national_code, password, phone_num, email):
        # TEKRARI NABUDN
        
        now = datetime.now()
        joined_at = now.strftime("%d/%m/%y|%H:%M:%S")
        self.users.append(User(name, national_code, password, phone_num, email,joined_at))
        val = [name, national_code, password, phone_num, email,joined_at]
        q = "INSERT INTO User VALUES (" + name + "," + national_code + "," + password + "," + phone_num + "," + email + "," + joined_at + ");"
        query = Query(self.db, q)
        query.parsing()


    def login(self, nc, password):
        
        q = 'SELECT FROM User WHERE national_code=='+ '"' + nc + '"' + ';'
        query = Query(self.db, q)
        f = query.parsing()
        if(len(f)):
            f = f[0]
            if(f[2] == password):
                print("You Logged in!")
                self.logedin = User(f[0],f[1],f[2],f[3],f[4],f[5])
                return(True)
            else:
                print("Wrong password!")
        else:
            print("There is no account with this national code. :) ")
        return False


        pass



    #####
    #####
    #####MAIN MENU
    #####
    #####
    def main_menu(self):
        while(True):
            print("#############################")
            menu_options = {1: 'Login as user', 2: 'Sign up', 3: 'Login as admin', 4: 'Exit'}
            for key in menu_options.keys():
                print(key, "-", menu_options[key])
            print("#############################")
            try:
                option = int(input("Please type the number of option: "))
            except:
                print("You should enter a number!")
            if(option == 1):
                print("Please enter your national code and password:")
                nc = input("National Code: ")
                password = input("Password: ")
                user = app.login(nc,password)
                if(user):
                    self.user_menu()
            elif(option == 2):
                print("Please enter these information:")
                name = input("Name: ")
                nc = input("National Code: ")
                password = input("Password: ")
                confirm_pass = input("Confirm Password: ")
                ## feature confirm password
                phone_num = input("Phone Number: ")
                email = input("Email Adress: ")
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                if(not(re.fullmatch(regex, email))):
                    print("Invalid Email!")
                elif(password != confirm_pass):
                    print("Password didn't match!")
                else:
                    app.register_new_user(name,nc,password,phone_num,email)
            elif(option == 3):
                password = input("Please enter your password: ")
                if(password == self.admin.password):
                    print("Dear Admin!\t You successfully logged in!")
                    self.admin_menu()
                else:
                    print("Wrong password!\t Don't try more if you're not the admin dude!")

            if(option == 4):
                os._exit(1)
        return 0
    ########
    ########
    ########USER MENU
    ########
    ########
    def user_menu(self):
        menu_options = {1: 'Open new account', 2: 'Show & Use my accounts', 3: 'Favorites accounts', 4: 'Logout'}
        while(True):
            print("#############################")
            for key in menu_options.keys():
                print(key, "-", menu_options[key])
            print("#############################")
            try:
                option = int(input("Please type the number of option: "))
            except:
                print("You should enter a number!")
            if(option == 1):
                print("Please enter a password and alias for your account:")
                password = input("Password: ")
                alias = input("Alias: ")
                self.logedin.opening_acc(password,alias)
            elif(option == 2):
                self.acc = self.logedin.show_acc()
                if(self.acc != 0):
                    self.acc_menu()
            elif(option == 3):
                print("Please enter an acount number and type an alias for that: ")
                ac = int(input("Account Number: "))
                al = input("Alias: ")
                self.logedin.fav_acc(ac,al)
            elif(option == 4):
                self.logedin = None
                break
        return 0
        pass
    #######
    #######
    #######ACC MENU
    #######
    def acc_menu(self):
        menu_options = {1: 'Transfer money', 2: 'Show Transaction' ,3: 'Bill payment', 4: 'Apply for loan', 5:  'Close account', 6: 'Back'}
        while(True):
            print("#############################")
            for key in menu_options.keys():
                print(key, "-", menu_options[key])
            print("#############################")
            try:
                option = int(input("Please type the number of option:"))
            except:
                print("You should enter a number!")
            if(option == 1):
                print("Please enter the account number of reciever or the alias you choosed before and the amount of money you want to transfer:")
                ff = input("Do you want use alias of that favorite account numver?(N/y) ")
                fav_al = None
                if(ff =="y"):
                    fav_al = input("Alias of reciever: ")
                else:
                    reciever = input("Reciever: ")
                money = int(input("Money: "))
                password = input("Please enter the password of your account: ")
                if(password == self.acc.password and fav_al == None):
                    self.acc.transfer(reciever,money)
                elif(password == self.acc.password and fav_al != None):
                    self.acc.transfer(None,money,fav_al)
                else:
                    print("Wrong Password!")
            elif(option == 2):
                self.acc.show_transaction()
            elif(option == 3):
                bill_num = int(input("Please enter the bill number: "))
                pay_num = int(input("Please enter the payment number: "))
                bill_amount = int(input("Please enter the amount of bill(Be Honest Please!): "))
                self.acc.pay_bill(bill_amount)
            elif(option == 4):
                money = int(input("How much money you want to request for the lone: "))
                thread = threading.Thread(target = self.acc.loan , args = (money,), daemon = True)
                thread.start()
            elif(option == 5):
                self.acc.close_acc()
                break
            elif(option == 6):
                self.acc = None
                break
        return 0
        pass

    ######
    ######
    ######ADMIN MENU
    ######
    ######
    def admin_menu(self):
        menu_options = {1: 'Show users information', 2: 'Edit users information', 3: 'Change bank account balances', 4: 'Open a bank account', 5: 'Close a bank account', 6: 'Logout'}
        while(True):
            print("#############################")
            for key in menu_options.keys():
                print(key, "-", menu_options[key])
            print("#############################")
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
        self.ba = []  # list of bank accounts user have

    def opening_acc(self,password,alias):
        acc = str(uuid.uuid4().int)[:16]
        q = "INSERT INTO Bank_acc VALUES (" + acc + "," + str(0) + "," + self.national_code + "," + password + "," + alias + ");"
        query = Query(db, q)
        query.parsing()
        pass
    def show_acc(self):
        q = "SELECT FROM Bank_acc WHERE owner_nc==" + '"' + self.national_code + '"' + ";"
        query = Query(self.db, q)
        accs = query.parsing()
        if(len(accs) == 0):
            print("You don't have any account. You should open an account :)")
            return 0
        for i in range(len(accs)):
            print("---------<<" + str(i+1) + ">>----------")
            print("Account Number:", accs[i][0])
            print("Balance: ", accs[i][1])
            print("Alias: ",accs[i][4])
            print("-------------------")
        n = int(input("Enter the number of account you want to work with: "))
        acc = accs[n-1]
        return(Bank_acc(acc[0],acc[1],acc[2],acc[3],acc[4]))

    def fav_acc(self,ac,al):
        q = "SELECT FROM Bank_acc WHERE acc==" + str(ac) + ";"
        query = Query(self.db, q)
        z = query.parsing()
        if(len(z)):
            q = "INSERT INTO Fav_acc VALUES (" + self.national_code + "," + str(ac) + "," + al + ");"
            query = Query(self.db, q)
            query.parsing()
            print("Successfulyy added to your favorite list!")
        else:
            print("There isn't any bank account with this account number!")

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
            ####BANK ACCS
            q = "SELECT FROM Bank_acc WHERE owner_nc==" + '"' + u[1] + '"' + ";"
            query = Query(self.db, q)
            accs = query.parsing()
            print("=========Bank Accouns=======")
            for acc in accs:
                print("=======================")
                print("Account Number: " + str(acc[0]))
                print("Balance: " + str(acc[1]))
                print("Password: " + acc[2])
                print("Alias: " + acc[3])
                print("========================")
            print("==========================")

    def edit_users(self,nc,l):
        q = "SELECT FROM User WHERE national_code==" + '"' + nc + '"' + ";"

        query = Query(self.db, q)
        a = query.parsing()

        atr = ["acc", "balance", "owner_nc", "password", "alias"]
        z = ""
        if(len(a) == 0):
            print("There isn't any bank account with this national code!")
        elif(len(a) == 1):
            a = a[0]

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
        self.db = db
        pass
    def transfer(self,reciever,money,fav = None):
        self.balance = int(self.balance)
        if(self.balance < int(money)):
            print("You don't have enough money")
        else:
            self.balance -= int(money)
            if(fav != None):
                q = "SELECT FROM Fav_acc WHERE owner_nc=="  + '"' + str(self.owner_nc) + '"'  + " AND " + "alias==" + '"' + fav + '"' + ";"
                query = Query(self.db,q)
                z = query.parsing()
                reciever = str(z[0][1])

            q = "UPDATE Bank_acc WHERE acc=="  + str(self.acc)  + " VALUES (" + str(self.acc) + ","+ str(self.balance) + "," + self.owner_nc + "," + self.password + "," + self.alias + ");"
            query = Query(self.db,q)
            query.parsing()
            #######
            q = "SELECT FROM Bank_acc WHERE acc=="  + reciever  + ";"
            query = Query(self.db,q)
            z = query.parsing()
            if(len(z) == 0):
                print("There isn't any account with this account number you entered!")
                return 0

            z = z[0]
            z[1] = str(int(z[1]) + money)
            q = "UPDATE Bank_acc WHERE acc==" + reciever  + " VALUES (" + str(z[0]) + ","+ str(z[1]) + "," + z[2] + "," + z[3] + "," + z[4] + ");"
            query = Query(self.db,q)
            query.parsing()
            ####Tranaction log
            now = datetime.now()
            t = now.strftime("%d/%m/%y|%H:%M:%S")
            q = "INSERT INTO Transaction VALUES (" + str(self.acc) + "," + reciever + "," + str(money) + "," + str(self.balance)  +  "," + t + ");"
            query = Query(self.db,q)
            query.parsing()


    def pay_bill(self,money):

        if(self.balance < int(money)):
            print("You don't have enough money!")
        else:
            self.balance = int(self.balance)
            self.balance -= int(money)
            q = "UPDATE Bank_acc WHERE acc==" + str(self.acc)  + " VALUES (" + str(self.acc) + ","+ str(self.balance) + "," + self.owner_nc + "," + self.password + "," + self.alias + ");"
            query = Query(self.db,q)
            query.parsing()
            ####Tranaction log
            now = datetime.now()
            t = now.strftime("%d/%m/%y|%H:%M:%S")

            q = "INSERT INTO Transaction VALUES (" + str(self.acc) + "," + "666" + "," + str(money) + "," + str(self.balance)  + "," + t + ");"  ### 666 is the code for bill payment
            query = Query(self.db,q)
            query.parsing()


    def loan(self,money,n = 12 , interval = 20):
        self.balance = int(self.balance)
        self.balance += int(money)
        q = "UPDATE Bank_acc WHERE acc==" + '"' + str(self.acc) + '"' + " VALUES (" + str(self.acc) + ","+ str(self.balance) + "," + self.owner_nc + "," + self.password + "," + self.alias + ");"
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
            q = "UPDATE Bank_acc WHERE acc==" + '"' + str(self.acc) + '"' + " VALUES (" + str(self.acc) + ","+ str(self.balance) + "," + self.owner_nc + "," + self.password + "," + self.alias + ");"
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
        q = "SELECT FROM Transaction WHERE sender==" + str(self.acc)  + " OR " + "reciever==" +  str(self.acc)  + ";"
        query = Query(self.db,q)
        l = query.parsing()
        for ll in l:
            if(ll[0] == self.acc):
                if(ll[1] == 666):
                    print("You with this account number: " +  str(self.acc) + " paid for bill $"  + str(ll[2]) + " in this time: " + str(ll[4]) + " & Your balance: $" + str(ll[3]))
                    pass
                elif(ll[1] == 333):
                    print("You with this account number: " +  str(self.acc) + " paid back for loaning $"  + str(ll[2]) + " in this time: " + str(ll[4]) + " & Your balance: $" + str(ll[3]))
                    pass
                else:
                    print("You with this account number: " +  str(self.acc) + " sent $"  + str(ll[2])  + " to this account number :" + str(ll[1]) + " in this time: " + str(ll[4]) + " & Your balance: $" + str(ll[3]))
            else:
                if(ll[1] == self.acc):
                    if(ll[0] == 333):
                        print( "You with this account number: "  +  str(self.acc)  +  " recieved $"   +  str(ll[2]) +  " for your loan request. "  +  " in this time: "  + str(ll[4])  + " & Your balance: $"  + str(ll[3]))
                    else:
                        print( "You with this account number: "  +  str(self.acc)  +  " recieved $"   +  str(ll[2]) +  " from this account number :"  + str(ll[0])  +  " in this time: "  + str(ll[4])  + " & Your balance: $"  + str(ll[3]))
                

    def close_acc(self):
        if(int(self.balance) == 0):
            q = "DELETE FROM Bank_acc WHERE acc==" + str(self.acc) + ";"
            query = Query(self.db,q)
            query.parsing()
        else:
            reciever = input("Please enter an acount number for transfering your money before close it:\n")
            self.transfer(reciever,int(self.balance))
            q = "DELETE FROM Bank_acc WHERE acc==" +  str(self.acc)  + ";"
            query = Query(self.db,q)
            query.parsing()
# Main code
###
if(__name__ == "__main__"):
    db = DB()
    db.inup()
    app = App(db)
    f = Figlet(font='slant')
    print(f.renderText('GNUBank'))
    #####
    #####
    app.main_menu()
    x = threading.Thread(target = app.main_menu , args = ())
    x.start()
