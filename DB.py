#!/usr/bin/env python3
# Import libraries
import re
from pyfiglet import Figlet
from datetime import datetime
import uuid

# DataBase code
class DB:
    def __init__(self):
        pass
        self.d = dict()
        self.ids = []

    def inup(self):  # initialize and update
        '''This method does initializing and updating the database and the main dictionary and the files.
        '''
        f = open("schema.txt", "r")
        q = None
        z = []
        data_cond = dict()    # Conditons and types of datas in tables
        for x in f:
            z.append(x)
        s = z[0].strip()
        q = open(s+".txt", "a")
        #self.file2dict(s+".txt")
        data_cond[s] = []
        file_names = [s+".txt"]
        for i in range(1, len(z)):
            b = z[i].strip()
            if (len(b.split()) == 1):
                s = b
                file_name = z[i].strip() + ".txt"
                q = open(file_name, "a")
                file_names.append(file_name)
                data_cond[s] = []
            elif(b != ""):
                data_cond[s].append(DB.attrs(b))
        f.close()
        self.data_cond = data_cond # attributes of tables and condtions of them
        self.data_types = data_cond
        for fn in file_names:
            title = file_name[:-4]
            self.file2dict(fn)
        return(data_cond)


    def file2dict(self, file_name,data_cond = None):
        """This method gets a file name and then update the main dictionry with information the file that gets.
		Args:
			file_name: file name with this pattern table_name.txt
		Return:
			self.d : The main dictionary that saved all information of files(Database)
		"""

        f = open(file_name, "r")
        z = []
        for x in f:
            z.append(x)

        title = file_name[:-4]
        self.d[title] = []
        if(len(z)):
            for i in range(len(z)):
                v = z[i].strip().split()
                c = Command(self,title,v)
                if(c.type_checker()):
                    self.d[title].append(v)
        return self.d

    def dict2file(self,table_name):
        """This method gets a table_name and make the file_name by the pattern(file_name.txt) and then update the file with the main dictionary.
		Args:
			table_name
		Return:
			-
		"""
        file_name = table_name + ".txt"
        f = open(file_name,"w")
        string = ""
        l = self.d[table_name]
        for ll in l:
            z = ""
            for lll in ll:
                z += str(lll) + " "
            string += z[:-1] + "\n"
        f.write(string)
        f.close()


    def attrs(l): ## l is a list
        l = l.split()
        cond = []
        for ll in l:
            if(ll[:4] == "CHAR"):
                end = ll.find(')')
                ln = int(ll[5:end])   # len CHAR
                cond.append(("str",ln))
            elif(ll == "INTEGER"):
                cond.append("int")
            elif(ll == "BOOLEAN"):
                cond.append("bool")
            elif(ll == "TIMESTAMP"):
                cond.append("timestamp")
            else:
                cond.append(ll)
        return cond

class Query:
    def __init__(self,db,query):
        self.db = db
        self.query = query
    ################
    ################
    ################ PARSING #####################
    def parsing(self):
        '''This method parses the sring query and then run it with commands!
		Arg:
			self: Query Object
		Return:
			- 
		'''
        splited = self.query.split()
        if(Query.syntax_checker(splited)):
            cmd = splited[0].upper()
            if(cmd == "UPDATE"):
                table = splited[1]
            else:
                table = splited[2]
            if(splited[1] == "*"):
                table = splited[3].strip(";")
            ll = self.db.d[table]
            dc = self.db.data_cond[table]
            index_attr = []
            for i in range(len(dc)):
                index_attr.append([dc[i][0],i])
            if(cmd == "INSERT"):
                vals = splited[4][1:-2].split(",")
                for i in range(len(vals)):
                    vals[i] = vals[i].strip('"')
                c = Command(self.db,table,vals)
                c.insert()
            elif(cmd == "SELECT"):
                cond = self.make_cond(index_attr,splited,4)
                c = Command(self.db,table,None,cond)
                return(c.select())

            elif(cmd == "UPDATE"):
                s = ""
                m = splited.index("VALUES")
                spc = splited[:m]
                table = splited[1]
                spc[-1] += ";"
                vals = splited[m+1][1:-2].split(",")
                for i in range(len(vals)):
                    vals[i] = vals[i].strip('"')
                cond = self.make_cond(index_attr,spc,3)
                c = Command(self.db,table,vals,cond)
                c.update()
            elif(cmd == "DELETE"):
                cond = self.make_cond(index_attr,splited,4)
                c = Command(self.db,table,None,cond)
                c.delete()
            return("OK")
        else:
           print("isn't ok")

        pass
    def make_cond(self,index_attr,splited,flag):
        '''This method 
        Args:
			self :
			index_attr :
			splited :
            flag :
		Return: 
			s :
			
        '''
        s = ""
        if(splited[1] == "*"):
            return ("True==True")
        for i in range(flag,len(splited)):
            s += " " +splited[i]

        s = s[:-1]
        s = "(" + s[1:] + ")"
        s = re.sub("OR","or",s)
        s = re.sub("AND","and",s)
        mew = re.findall(r'\w+(?=[!=]=)',s)
        for i in range(len(mew)):
            for j in index_attr:
                if(mew[i] == j[0]):
                    s = s.replace(j[0],"fd[i]" +  "[" + str(j[1]) + "]")    # bug age value ba title yeki bashe replace mishe baz
        return s
    # Syntax checker
    def syntax_checker(sq):
        '''
		This method check the syntax of query
		Arg:
			sq : The splited of query 
		Return:
			True or False : If syntax was OK and without error returns True otherwise return False.
		'''
        if (sq[0].upper() != "INSERT" and sq[0].upper() != "SELECT" and sq[0].upper() != "UPDATE" and sq[0].upper() != "DELETE"):
            print("Command not found!\n You should use of these keywords for starting your query: INSERT, SELECT, DELETE, UPDATE")
            return False
        elif(sq[-1][-1] != ";"):
            print("Synatx Error: You didn't use ; at the end of your query. :)")
            return False
        return True


# Commands section
class Command:
    def __init__(self,db,table_name,val,cond = None):
        self.db = db
        self.table_name = table_name
        self.val = val
        self.cond = cond
        self.types = db.data_types
        self.fd = self.db.d  #All data that saved in this dictioanry

    def insert(self):
        '''
		Arg:
			self : A Command instance
		Return:
			-
		'''
        uid = int(uuid.uuid1())
        if(self.type_checker()):
            z = []
            for v in self.val:
                z.append(v)
            z.append(str(uid))
            self.db.d[self.table_name].append(z)
            self.db.dict2file(self.table_name)
            #self.db.inup()

    def select(self):
        '''
		Arg:
			self : A Command instance
		Return:
			- 
		'''
        z = []
        fd = self.fd[self.table_name]
        for i in range(len(fd)):
            if(eval(self.cond)):
                z.append(fd[i])

        return z

    def delete(self):
        '''
		Arg:
			self : A Command instance
		Return:
			-
		'''
        fd = self.fd[self.table_name]
        tt = []
        for i in range(len(fd)):
            if(not(eval(self.cond))):
               tt.append(fd[i])
        self.db.d[self.table_name] = tt
        ##
        self.db.dict2file(self.table_name)
        ##
        return self.db.d

    def update(self):
        '''
		Arg:
		
		'''
        counter = 0
        fd = self.fd[self.table_name]
        tt = []
        if(self.type_checker(0)):
            for i in range(len(fd)):
                if(eval(self.cond)):
                    counter += 1
                    fd[i][:-1] = self.val
            self.db.d[self.table_name] = fd
            self.db.dict2file(self.table_name)
            self.db.inup()
            if(counter == 0):
                return("No ITEMS with this condition!")
            return self.db.d

        
        return ("Done")



    def type_checker(self, q = 1): ## data_cond is types of datas and that limitation about types
        '''This method checks the types of values that given in a query.
		Arg:
			self : Command object
		Reutrn:
			True or False : When types are matched it gives us True otherwise returns False.
		
		'''
        data_cond = self.types
        a = data_cond[self.table_name]
        li = self.db.d[self.table_name]
        for i in range(len(a)):
            try:
                tt = a[i][-1]

                v = self.val[i]
                if(type(tt) == str):
                    if(tt == "int"):
                        self.val[i] = int(self.val[i])
                    elif(tt == "bool"):
                        self.val[i] = bool(self.val[i])
                    elif(tt == "timestamp"):
                        self.val[i] = datetime.strptime(self.val[i], '%d/%m/%y|%H:%M:%S')## we suppose we get some string like this : '18/09/19|01:55:19'
                        self.val[i] = self.val[i].strftime('%d/%m/%y|%H:%M:%S')
                else:
                    self.val[i] = str(self.val[i])
                    l = len(self.val[i])
                    if(l > tt[1]):
                        raise Exception("Your value size of " + a[i][0] + " is larger than I want!")
                if(a[i][1] == "UNIQUE"):
                    for x in li:
                        if(x[i] == v and q):
                            print(q)
                            raise Exception("Unique constraint!",a[i])

            except Exception as e:
                print(e)
                print("EROR")
                print(type(e))
                return False
        return True



if(__name__ == "__main__"):
    db = DB()
    db.inup()
    f = Figlet(font='slant')
    print(f.renderText('DataBase'))
    i = 1
    for key in db.data_cond.keys():
                print("(Table" + str(i) + ")" ,key, "-", db.data_cond[key])
                i += 1
    while(True):
        str_query = input("> ")
        if(str_query == "help"):
            print('''There are four commands you can use here:
            1- INSERT
                Syntax:  INSERT INTO <table_name> VALUES (<field1_value>,<field2_value>,<field3_value>);
                Example: INSERT INTO User VALUES ("Ali","0033",passwd,"09121113344","example@gmail.com","12/02/22|07:08:04");
            2- SELECT
                Syntax:  SELECT FROM <table_name> WHERE <field1_name>==<field_value> OR <field2_name>!=<field2_value>;
                Example: SELECT FROM User WHERE name=="Ali" OR national_code!="0044";
            3- DELETE
                Syntax:  DELETE FROM <table_name> WHERE <field1_name>==<field_value> OR <field2_name>!=<field2_value>;
                Example: DELETE FROM User WHERE name=="Ali" and national_code=="0033";
            4- UPDATE
                Syntax:  UPDATE <table_name> WHERE <field1_name>==<field_value> OR <field2_name>!=<field2_value> VALUES (<field1_value>,<field2_value>,<field3_value>);
                Example: UPDATE User WHERE name=="Hossein" VALUES ("Ali","0033",passwd,"09121113344","alaki@gmail.com","12/02/22|07:08:04");
            ''')
        elif(str_query == "exit"):
            break
        else:
            query = Query(db,str_query)
            print(query.parsing())
