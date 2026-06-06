from flask import Flask,render_template,url_for,request,redirect,flash
import mysql.connector

app=Flask(__name__)

#mysql connection
con=mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_pass",
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
        flash("Employee Added")
        return redirect(url_for('home'))
    return render_template('add.html')

#update employee
@app.route('/update/<string:id>',methods=['GET','POST'])
def update(id):
    if request.method=='POST':
       name=request.form['name']
       department=request.form['department']
       salary=request.form['salary']
       city=request.form['city'] 
       res=con.cursor(dictionary=True)
       sql="update employee set name=%s,department=%s,salary=%s,city=%s where id=%s"
       value=(name,department,salary,city,id)
       res.execute(sql,value)
       con.commit()
       flash("Employee Updated")
       return redirect(url_for('home'))
    
    res=con.cursor(dictionary=True)
    sql="select * from employee where id=%s"
    value=(id,)
    res.execute(sql,value)
    result=res.fetchone()
    return render_template("update.html",datas=result)

#delete Employee
@app.route('/delete/<string:id>',methods=['GET','POST'])
def delete(id):
    res=con.cursor(dictionary=True)
    sql="delete from employee where id = %s"
    value=(id,)
    res.execute(sql,value)
    con.commit()
    flash("Employee Deleted")
    return redirect(url_for('home'))

#search by Employee Names
@app.route('/search',methods=['GET','POST'])
def search():
    keyword=request.args.get('search')
    res=con.cursor(dictionary=True)
    sql='select * from employee where name like %s'
    value=('%'+keyword+'%',)
    res.execute(sql,value)
    result=res.fetchall()
    return render_template('home.html',datas=result)


if(__name__=="__main__"):
    app.secret_key="ajith@123"
    app.run(debug=True,port=9000)