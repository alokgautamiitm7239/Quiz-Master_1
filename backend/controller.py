from flask import Flask , render_template, request, url_for, redirect, Response
from .models import *
from flask import current_app as app
from datetime import datetime,date,timezone
#for the charts
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')


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
        elif usr and usr.role==1:
            return redirect(url_for("user_dashboard",id=id))
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

#route for que option
@app.route("/admin_que/<que_id>/<id>")
def que_opt(que_id,id):
    question=Question.query.filter_by(id=que_id).first()
    return render_template("admin_option.html",id=id ,question=question)

#Route for user managment
@app.route("/admin_user/<id>")
def usr(id):
    users=User_Info.query.all()
    return render_template("admin_usr.html" ,id=id ,users=users)

#Route for delete user
@app.route("/delete_user")
def delete_user():
    id=request.args.get('id')
    user_id=request.args.get('user_id')
    user = User_Info.query.get(user_id) 
    db.session.delete(user)
    db.session.commit()
    users = User_Info.query.all() 
    return render_template("admin_usr.html",id=id,users=users)


#Route for admin search
@app.route("/search/<id>", methods=["GET","POST"])
def search(id):
    if request.method=="POST":
        search_txt=request.form.get("search_txt")
        by_subject=search_by_subject(search_txt)
        by_quiz=search_by_quiz(search_txt)
        by_user=search_by_user(search_txt)
        if by_subject:
            return render_template("admin.html",id=id,subjects=by_subject)

        elif by_quiz:
            return render_template("admin_quiz.html",id=id,quizzes=by_quiz)
        
        else:
            return render_template("admin_usr.html",id=id,users=by_user)
    
    return render_template("admin.html" ,id=id)


#Edit subject
@app.route("/edit_subject/<sub_id>/<id>", methods=["GET","POST"])
def edit_sub(sub_id,id):
    subject=Subject.query.get(sub_id)
    if request.method=="POST": #For register new theatre
        subject.name=request.form.get("name")
        subject.description=request.form.get("description")
        db.session.commit()
        return render_template("edit_subject.html",msg="Edit successfully" ,id=id)
    return render_template("edit_subject.html" ,id=id,sub_id=sub_id)

#Delete subject
@app.route("/delete_subject")
def delete_sub():
    id=request.args.get('id')
    sub_id=request.args.get('sub_id')
    subject = Subject.query.get(sub_id) 
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('admin_dashboard',id=id)) 

#Edit quiz
@app.route("/edit_quiz/<quiz_id>/<id>", methods=["GET","POST"])
def edit_quiz(quiz_id,id):
    quiz=Quiz.query.get(quiz_id)
    quizzes=get_quiz()
    chapters=get_chapter()

    if request.method=="POST":
        quiz.chapter_id=request.form.get("name")
        str_date=request.form.get("date")
        quiz.date_of_quiz= datetime.strptime(str_date, "%Y-%m-%d").date()
        quiz.time_duration_minutes=request.form.get("duration")
        db.session.commit()
        return render_template("edit_quiz.html",msg="Edit successfully" ,id=id)
    return render_template("edit_quiz.html",id=id,quiz_id=quiz_id,quizzes=quizzes,chapters=chapters)

#Delete quiz
@app.route("/delete_quiz")
def delete_quiz():
    id=request.args.get('id')
    quiz_id=request.args.get('quiz_id')
    quiz = Quiz.query.get(quiz_id)  
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('admin_quiz',id=id))

#Edit chapter
@app.route("/edit_chapter/<sub_id>/<chap_id>/<id>", methods=["GET","POST"])
def edit_chapter(sub_id,id,chap_id):
    chapter=Chapter.query.get(chap_id)
    if request.method=="POST":
        chapter.name=request.form.get("name")
        chapter.description=request.form.get("description")
        chapter.subject_id=request.form.get("id")
        db.session.commit()
        return render_template("edit_chapter.html",msg="Edit successfully" ,id=id,sub_id=sub_id)
    return render_template("edit_chapter.html" ,id=id,sub_id=sub_id,chap_id=chap_id)

#Delete chapter
@app.route("/delete_chapter")
def delete_chap():
    id=request.args.get('id')
    chap_id=request.args.get('chapter_id')
    chapter = Chapter.query.get(chap_id)  
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for('admin_dashboard',id=id))

#Edit Question
@app.route("/edit_que/<quiz_id>/<que_id>/<id>",methods=["GET","POST"])
def edit_que(id,quiz_id,que_id):
    question=Question.query.get(que_id)
    if request.method=="POST":
        question.question_statement=request.form.get("que_st")
        question.option1=request.form.get("opt1")
        question.option2=request.form.get("opt2")
        question.option3=request.form.get("opt3")
        question.option4=request.form.get("opt4")
        question.correct_option=request.form.get("crt")
        quiz_id=request.form.get("id")
        db.session.commit()
        return render_template("edit_question.html",msg="Edit successfully" ,id=id)
    return render_template("edit_question.html",id=id,quiz_id=quiz_id,que_id=que_id)

#Delete question
@app.route("/delete_question")
def delete_que():
    id=request.args.get('id')
    que_id=request.args.get('question_id')
    question = Question.query.get(que_id)  
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('admin_quiz',id=id)) 

    
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

def search_by_user(search_txt):
    users=User_Info.query.filter(User_Info.full_name.ilike(f"%{search_txt}%")).all()
    return users

def search_by_subject(search_txt): 
    subjects=Subject.query.filter(Subject.name.ilike(f"%{search_txt}%")).all() #ilike--> i use for case sensation and like for random filter
    return subjects

def search_by_quiz(search_txt):
    quizzes=Quiz.query.filter(Quiz.id.ilike(f"%{search_txt}%")).all()
    return quizzes

#Admin routes are done here Start User routes

# User route for home
@app.route("/user/<id>")
def user_dashboard(id):
    msg = request.args.get('msg')
    quizzes=get_quiz()
    return render_template("user.html",id=id,quizzes=quizzes,msg=msg)

#Route for view quiz
@app.route("/view_quiz/<chapter_id>/<id>")
def view_quiz(id,chapter_id):
    chapter=Chapter.query.filter_by(id=chapter_id).first()
    subject=Subject.query.filter_by(id=chapter.subject_id).first()

    return render_template("view_quiz.html" ,id=id,chapter=chapter,subject=subject)

#Route for Start quiz and submitted the exam 
@app.route("/start_quiz/<quiz_id>/<id>", methods=["GET","POST"])
def start_quiz(id,quiz_id):
    quiz=Quiz.query.filter_by(id=quiz_id).first() #for the tiem validation
    questions=Question.query.filter_by(quiz_id=quiz_id).all()
    
    if request.method=="POST":
        timestamp=datetime.now(timezone.utc)
        score = 0
        count=0
        for question in questions:
            count+=1
            user_answer = request.form.get(f'{question.id}')
            if user_answer == question.correct_option:
                score += 1
        submit=Score(quiz_id=quiz_id,user_id=id,total_scored=score,time_stamp_of_attempt=timestamp)
        db.session.add(submit)
        db.session.commit()
        t_score=f"{score}"+"/"+f"{count}"
        return redirect(url_for("user_dashboard",id=id,msg="Thank you! Quiz Submission Successfully Your Score : "+t_score))

    elif quiz.date_of_quiz==date.today():
     return render_template("start_quiz.html" ,id=id,questions=questions,quiz_id=quiz_id) 
    
    else:
        return redirect(url_for("user_dashboard",id=id,msg="Quiz not started yet"))



# Route for score
@app.route("/score/<id>")
def score(id):
    score=Score.query.filter_by(user_id=id).all()
    return render_template("score.html",id=id,scores=score)


#Summary for admin
@app.route("/summary/<id>")
def ad_summary(id):
    subjects = Subject.query.all()
    subject_names = []
    top_scores = []
    attempt_counts = []
    for subject in subjects:
        subject_names.append(subject.name)
        max_score = 0
        attempts = 0
        for chapter in subject.chapters:
            for quiz in chapter.quizzes:
                # Count attempts
                attempts += len(quiz.scores)
                # Find max score
                for score in quiz.scores:
                    if score.total_scored > max_score:
                        max_score = score.total_scored
        top_scores.append(max_score)
        attempt_counts.append(attempts)

        
    plt.figure(figsize=(7, 5))
    plt.bar(subject_names,top_scores)
    plt.ylabel('Scores')
    plt.title('Subject wise top score')
    plt.savefig("static/bar.png")
    plt.close #remove the chart from the memory

#Pie chart 
    plt.figure(figsize=(6, 6))
    plt.pie(attempt_counts, 
            labels=subject_names, 
            autopct='%1.1f%%')
    plt.title('Quiz Attempts by Subject')
    plt.savefig("static/pie.png")
    plt.close()
    return render_template("admin_summary.html",id=id)

#for user dash board
@app.route("/u_summary/<user_id>")
def u_summary(user_id):
    quiz_data = db.session.query(
        Quiz.id,
        Quiz.date_of_quiz,
        Score.total_scored
    ).join(
        Score, Quiz.id == Score.quiz_id
    ).filter(
        Score.user_id == user_id
    ).all()

    quiz_names = [f"Quiz {q.id}" for q in quiz_data] 
    scores = [q.total_scored for q in quiz_data]
    
    plt.figure(figsize=(10, 5))
    plt.bar(quiz_names,scores)
    plt.ylabel('Quiz score')
    plt.title('Quiz wise scores')
    plt.savefig("static/u_bar.png")
    plt.close()

    return render_template("user_summary.html",id=user_id)



