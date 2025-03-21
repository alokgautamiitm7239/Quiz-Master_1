from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Entity 1: User Info
class User_Info(db.Model):
    __tablename__ = "user_info"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.Integer, default=1)
    full_name = db.Column(db.String(), nullable=False)
    qualification = db.Column(db.String(), nullable=False)
    dob = db.Column(db.Date, nullable=False) 
    scores = db.relationship("Score", cascade="all,delete", backref="user_info", lazy=True)

# Entity 2: Subject
class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    chapters = db.relationship("Chapter", cascade="all,delete-orphan", backref="subject", lazy=True)

# Entity 3: Chapter
class Chapter(db.Model):
    __tablename__ = "chapter"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False, index=True)
    quizzes = db.relationship("Quiz", cascade="all,delete", backref="chapter", lazy=True)

# Entity 4: Quiz
class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration_minutes = db.Column(db.Integer, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False, index=True)
    remark = db.Column(db.String(), nullable=True ,default="No remark")
    questions = db.relationship("Question", cascade="all,delete", backref="quiz", lazy=True)
    scores = db.relationship("Score", cascade="all,delete", backref="quiz", lazy=True)

# Entity 5: Question
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False, index=True)
    question_statement = db.Column(db.String(), nullable=False)
    option1 = db.Column(db.String(), nullable=False)
    option2 = db.Column(db.String(), nullable=False)
    option3 = db.Column(db.String(), nullable=False)
    option4 = db.Column(db.String(), nullable=False)
    correct_option = db.Column(db.String(), nullable=False)

# Entity 6: Score
class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False, index=True)
    time_stamp_of_attempt = db.Column(db.DateTime, nullable=False)
    total_scored = db.Column(db.Integer, nullable=False)
