from flask import Flask , render_template,request,url_for,redirect
from .models import *
from flask import current_app as app
from datetime import datetime


@app.route("/")
def home():
    return render_template("index.html")

# Route for login 
@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST": #For validate user credential
        id=request.form.get("email")
        pwd=request.form.get("password")
        usr=User_Info.query.filter_by(email=id,password=pwd).first()
        if usr and usr.role==0: #Exisiting user and admin
            return redirect(url_for("admin_dashboard",id=id))
            # return render_template("admin.html")
        elif usr and usr.role==1:
            # return redirect(url_for("user_dashboard",name=uname))
            return render_template("student.html")
        else:       #If user doesn't exist
            return render_template("login.html",msg="Invalid User Credential.....")

    return render_template("login.html")

#Route for register
@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method=="POST": #For register new user
        uname=request.form.get("user_name")
        id=request.form.get("email")
        pwd=request.form.get("password")
        qlf=request.form.get("qualification")
        dob_str=request.form.get("dob")
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        usr=User_Info.query.filter_by(email=id).first()
        if usr:
           return render_template("login.html",msg="User is already exist.. try to login")
        new_usr=User_Info(full_name=uname,email=id,password=pwd,qualification=qlf,dob=dob)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg="User registration is successfull try to login...")
    return render_template("Signup.html")

# Admin route for home
@app.route("/admin/<id>")
def admin_dashboard(id):
    subjects=get_subject()
    chapters=get_chapter()
    return render_template("admin.html",id=id,subjects=subjects,chapters=chapters)

# Admin route for Quiz
@app.route("/admin_quiz/<id>")
def admin_quiz(id):
    quizzes=get_quiz()
    chapters=get_chapter()
    return render_template("admin_quiz.html",id=id,quizzes=quizzes,chapters=chapters)

#Route for add_sub
@app.route("/add_subject/<id>",methods=["GET","POST"])
def add_subject(id):
    if request.method=="POST":
        name=request.form.get("name")
        des=request.form.get("description")
        sub=Subject.query.filter_by(name=name).first()
        if sub:
            return render_template("add_subject.html",msg="Subject already exist" ,id=id)
        subject=Subject(name=name,description=des)
        db.session.add(subject)
        db.session.commit()
        return render_template("add_subject.html",msg="Subject added successfully" ,id=id)

    
    return render_template("add_subject.html",id=id)

#Route for add_chapter
@app.route("/add_chapter/<sub_id>/<id>",methods=["GET","POST"])
def add_chapter(sub_id,id):
    if request.method=="POST":
        name=request.form.get("name")
        des=request.form.get("description")
        sub_id=request.form.get("id")
        chap=Chapter.query.filter_by(name=name).first()
        if chap:
            return render_template("add_chapter.html",msg="Chapter already exist" ,id=id)
        chapter=Chapter(name=name,description=des,subject_id=sub_id)
        db.session.add(chapter)
        db.session.commit()
        return render_template("add_chapter.html",msg="Chapter added successfully" ,id=id,sub_id=sub_id)

    
    return render_template("add_chapter.html",id=id,sub_id=sub_id)

#Route for add_Quiz
@app.route("/add_quiz/<id>",methods=["GET","POST"])
def add_quiz(id):
    quizzes=get_quiz()
    chapters=get_chapter()

    if request.method=="POST":
        name=request.form.get("name")
        str_date=request.form.get("date")
        date= datetime.strptime(str_date, "%Y-%m-%d").date()
        duration=request.form.get("duration")
        quiz=Quiz(chapter_id=name,date_of_quiz=date,time_duration_minutes=duration)
        db.session.add(quiz)
        db.session.commit()
        return render_template("add_quiz.html",msg="Quiz added successfully" ,id=id)

    
    return render_template("add_quiz.html",id=id,quizzes=quizzes,chapters=chapters)

#Route for add_que
@app.route("/add_que/<quiz_id>/<id>",methods=["GET","POST"])
def add_que(id,quiz_id):
    if request.method=="POST":
        que_st=request.form.get("que_st")
        opt1=request.form.get("opt1")
        opt2=request.form.get("opt2")
        opt3=request.form.get("opt3")
        opt4=request.form.get("opt4")
        crt_opt=request.form.get("crt")
        quiz_id=request.form.get("id")
                
        que=Question(question_statement=que_st,option1=opt1,option2=opt2,option3=opt3,option4=opt4,correct_option=crt_opt,quiz_id=quiz_id)
        db.session.add(que)
        db.session.commit()
        return render_template("add_question.html",msg="Question added successfully" ,id=id)

    
    return render_template("add_question.html",id=id,quiz_id=quiz_id)

#Complementry function 

def get_subject():
    subjects=Subject.query.all()
    return subjects

def get_chapter():
    chapters=Chapter.query.all()
    return chapters

def get_quiz():
    quizzes=Quiz.query.all()
    return quizzes



