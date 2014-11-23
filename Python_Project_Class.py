import sqlite3
from wsgiref.simple_server import make_server
import cgi
import cgitb
from collections import OrderedDict
from datetime import datetime

form_vals={}
name=""

##This class handles all database operations
class Database:
    conn = sqlite3.connect("zoo.sqlite")
    cursor = conn.cursor()
    def database(self,subject,k):
        if(k=='s'):
            x=self.getStudentDetails()
                
        
        elif(k=='q'):
            x=self.getQuestions(subject)
        else:
            x=self.getResult()
        
        
        return x


    def writeData(self,x):
        table_exists="select name from sqlite_master where type='table' and name='Student_Results'"
        print(table_exists)
        if not self.cursor.execute(table_exists).fetchone():
            self.cursor.execute("create table 'Student_Results'(name text,subject text,score text,date date)")
            print("Table created")
        if(len(x)!=0):
            
            self.cursor.execute("insert into Student_Results(name,subject,score,date) values('"+x[0]+"','"+x[1]+"','"+x[2]+"','"+str(datetime.now())+"')")
            self.conn.commit()
        
    def getStudentDetails(self):
        table_exists="select name from sqlite_master where type='table' and name='Student_Details'"
        print(table_exists)
        if not self.cursor.execute(table_exists).fetchone():
            self.cursor.execute("create table 'Student_Details'(studentName text,password1 text,parentName text,password2 text)")
            print("Table Student_Details created")
                
        
        x=self.cursor.execute("select * from 'Student_Details'").fetchall()
        if(len(x)==0):
            students=[('Sam','Sam@1','Jessy','Jessy@1'),('Mounica','Mouni@1','Lakshmi','Lakshmi@1'),('Ganesh','Gani@1','Raj','Raj@1'),('Gula','gula@1','Abc','Abc@1'),('Sri','sri@1','Raj','Raj@1'),('Sruthi','Sruthi@1','Ishu','Ishu@1'),('John','John@1','Smith','Smith@1'),('Dennis','Dennis@1','Klemenz','Klemenz@1'),('Kevin','Kevin@1','Peter','Peter@1'),('campbell','Campbell@1','Smith','Smith@1')]
            insert="insert into Student_Details(studentName,password1,parentName,password2) values(?,?,?,?)"
            self.cursor.executemany(insert,students)
            print("Rows inserted")
        return x
    
    def getQuestions(self,subject):
        table_exists="select name from sqlite_master where type='table' and name='"+subject+"'"
        print(table_exists)
        if not self.cursor.execute(table_exists).fetchone():
            self.cursor.execute("create table '"+subject+"'(Question text,Answer text)")
            print("Table created")
        x=self.cursor.execute("select * from '"+subject+"'").fetchall()
        if(len(x)==0):
            if(subject=="Maths"):
                questions=[('what is the value of 2+3','5'),('what is the value of 5+8','13'),('what is the value of 9*9','81'),('what is the value of 6/2','3'),('what is the value of 6%2','0'),('what is the value of 7*9','63'),('what is the value of 20*8','160'),('what is the value of 8-5','3'),('what is the value of 56-10','46'),('what is the value of 40*2','80')]
                insert="insert into Maths(Question,Answer) values(?,?)"
                self.cursor.executemany(insert,questions)
                print("Rows inserted")
                self.conn.commit()
            if(subject=="Science"):
                questions=[('What is the instrument used to measure temperature?','Thermometer'),('True or false? Ice sinks in water?','False'),('What is the fastest land animal in the world?','Zebra'),('What is the other name of tidal wave?','Tsunami'),('What is the biggest planet in our solar system?','Jupiter')]
                insert="insert into Science(Question,Answer) values(?,?)"
                self.cursor.executemany(insert,questions)
                print("Rows inserted")
                self.conn.commit()
        return x
    
    def getResult(self):
        table_exists="select name from sqlite_master where type='table' and name='Student_Results'"
        print(table_exists)
        if not self.cursor.execute(table_exists).fetchone():
            x=None
        else:
            print("Table exists")
            x=self.cursor.execute("select * from Student_Results where name=(select studentName from Student_Details where parentName='"+name+"')").fetchall()
            print(x)
        return x



##function that performs the web service
def student_test_app(environ,start_response):
    try:
        print("Im in web service")
        global first
        global studentList
        global name
        global exam
        global counter
        #counter=0
        d=Database()
        message=""#<head><style>body{background-color:#b0c4de;}.container {width: 500px;clear: both;}.container input { width: 100%; clear: both; }</style></head>"
        status='200 OK'
        headers=[('Content-type','text/html; charset=utf-8')]
        start_response(status,headers)
        x=""
        global k
        k=k+1
    
        if(k==0):
            studentList=d.database(" ",'s')
            message+="<H1>Login</H1>"
            
            message+="<div class='container'><form method='POST'><br><br>Please enter your login name<input name=name>"
            message+="<br><br>Please enter password              <input name=password>"
        
            message+="<br><br><input type='submit' value='login' name='submit1'></form></div>"
            first=0
    
    
        elif(k==1):
        
            print("entered")
            if(first==0):
                print("enterd into first")
                request_body_size = int(environ['CONTENT_LENGTH']) 
                request_body = environ['wsgi.input'].read(request_body_size) 
                form_vals = get_form_vals(request_body)
                print(form_vals)
                subject=[]
                for item in form_vals.items():
                    subject.append(item)
                subject.sort()
                name=subject[0][1]
                password=subject[1][1]
                first+=1
                for item in studentList:
                    if(name==item[0] and password==item[1]):
                        counter=1
                        break
        
            
            if(counter==1):
                
                message+="<H1>GOOD LUCK</H1>"
                message+="<form method='POST'>"
                message+="<br><br>Please enter subject<input name=subject>"
                message+="<br><br><input type='submit' value='submit' name='submit1'></form>"
            else:
                for item in studentList:
                    if(name==item[2] and password==item[3]):
                        counter=2
                        break
                studentResult=d.getResult()
                print(studentResult)
                message+="<H1>Welcome</H1>"
                message+="<form method='POST'><br><br>"
                i=0
                for item in studentResult:
                    i+=1
                    if(i==1):
                        message+="<br><br>Student Name :"+item[0]
                    message+="<br><br>Subject     :"+item[1]
                    message+="<br><br>Marks out of 10:  "+item[2]
                    message+="<br><br>Date when test taken:  "+item[3]
                message+="</form>"
            
        elif(k==2):
            request_body_size = int(environ['CONTENT_LENGTH']) 
            request_body = environ['wsgi.input'].read(request_body_size) 
            form_vals = get_form_vals(request_body)
            print(form_vals)
            x=list(form_vals)
            subject=[]
            for item in form_vals.items():
                subject.append(item)
            #i+=1
            subject.sort()
            print(subject)
        #name=subject[0][1]
            global subjectChosen
            subjectChosen=subject[0][1]
        
            print("subject is  "+subjectChosen)
        
            queriesList=d.database(subjectChosen,'q')
            exam=queriesList
            message+="<H1>TEST</H1>"
            message+="<form method='POST'><br><br>"
            i=0
            for item in queriesList:
                message+="<br>"+item[0]+"<input name=question"+str(i)+"<br>"
                message+="<br><br>"
                i=i+1
            
            message+="<br><br><input type='submit' value='submit' name='submit1'></form>"
        
        elif(k==3):
            print(exam)
            result=0
            request_body_size = int(environ['CONTENT_LENGTH']) 
            request_body = environ['wsgi.input'].read(request_body_size) 
            form_vals=get_form_vals(request_body)
            i=0
        
            form_vals=OrderedDict(sorted(form_vals.items(), key=lambda t: t[0]))
            print(form_vals)
            for key in form_vals.items():
                if(exam[i][1]==key[1]):
            
                    result+=1
                    print("result "+str(result))
                i=i+1
            print(result)
            message+="<form method='post'><H1>Congrats </H1>"+name
            message+="<br><br>your result is <br><br>"+str(result)
            message+="<br><br><input type='submit' value='Take another test' name='take another test'></form>"
      
            x=[name,subjectChosen,str(result)]
            print(x)
            d.writeData(x)
        elif(k==4):
            k=0
            
            request_body_size = int(environ['CONTENT_LENGTH']) 
            request_body = environ['wsgi.input'].read(request_body_size) 
            form_vals=get_form_vals(request_body)
            form_vals=OrderedDict(sorted(form_vals.items(), key=lambda t: t[0]))
            print(form_vals)
            message+="<form method='Post'><input type='submit' value='please click here' name='clickhere'></form>"
    except:
        message+="<font color='red'>Invalid navigation!! Please refresh the screen</red>"
        k=-1
        counter=0
        
    return[bytes(message,'utf-8')]

    
                                      


def get_form_vals(post_str):
       
        i=0
        form_vals.clear();
        for item in post_str.decode().split("&"):
                i=i+1
                
                if(item.split("=")[0]!="submit1" and item.split("=")[0]!="submit"):
                        
                         x1=item.split("=")[0]
                         x2=item.split("=")[1]
                         form_vals[x1] = x2
             
        return form_vals


    
    

httpd = make_server('', 8000, student_test_app)
print("Serving on port 8000...")
exam=[]
studentList=[]
subjectChosen=""
k=-1
first=0
counter=0

httpd.serve_forever()
Database().conn.close()
        
