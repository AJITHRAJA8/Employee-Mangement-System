from flask import Flask,render_template,url_for,request,redirect
import mysql.connector

app=Flask(__name__)

#mysql connection
con=mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Ajith@9751",
    database='crud'
)
if con.is_connected:
    print("Connect Successfully")
else:
    print("Error in connection")

@app.route('/')
def home():
    res=con.cursor(dictionary=True)
    sql="select * from employee"
    res.execute(sql)
    result=res.fetchall()
    return render_template("home.html",datas=result)

#add employee
@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=="POST":
        name=request.form['name']
        department=request.form['department']
        salary=request.form['salary']
        city=request.form['city']
        res=con.cursor(dictionary=True)
        sql="insert into employee(name,department,salary,city) values(%s,%s,%s,%s)"
        value=(name,department,salary,city)
        res.execute(sql,value)
        con.commit()
        return redirect(url_for('home'))
    return render_template('add.html')



if(__name__=="__main__"):
    app.run(debug=True)