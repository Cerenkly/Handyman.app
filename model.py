

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    user_address = db.Column(db.Text)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)


    def __repr__(self):
        return f"<User user_id={self.user_id} first_name={self.first_name} last_name= {self.last_name} user_address= {self.user_address} email={self.email} password= {self.password}>"


class Handyman(db.Model):
    """A handyman."""

    __tablename__ = "handymans"

    handyman_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company_name = db.Column(db.String(25))
    zip_code = db.Column(db.Integer)
    radius = db.Column(db.Float)
    price_per_hour = db.Column(db.Integer)
    phone_number = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref=("handyman"), uselist=True)

    def __repr__(self):
        return f"<Handyman handyman_id={self.handyman_id} company_name={self.company_name} zip_code={self.zip_code} radius= {self.radius} price_per_hour{self.price_per_hour} phone_number={self.phone_number}>"


class HandymanService(db.Model):

    __tablename__ = "handyman_service"

    handyman_service_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    handyman_id = db.Column(db.Integer,db.ForeignKey("handymans.handyman_id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.service_id"), nullable= False)

    #handyman = db.relationship("Handyman", uselist= False, backref="handyman_service")
    #user = db.relationship("User", uselist= False, backref="handyman_service")

    def __repr__(self):
        return f"<Handyman_service handyman_service_id={self.handyman_service_id}>"

class Service(db.Model):

    __tablename__ = "service"

    service_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    service_name = db.Column(db.String)

    handyman = db.relationship("Handyman",secondary= "handyman_service", backref="services")

    def __repr__(self):
        return f"<Service service_id={self.service_id} service_name={self.service_name}>"

class Comment(db.Model):

    __tablename__ = "comments"   

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    handyman_id = db.Column(db.Integer,db.ForeignKey("handymans.handyman_id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"))
    comment = db.Column(db.Text)
    created_date = db.Column(db.Text)

    handyman = db.relationship("Handyman", backref="comments")
    user = db.relationship("User", backref="comments")

    def __repr__(self):
        return f"<Comment comment={self.comment} created_date={self.created_date}>"

class Rating(db.Model):


    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    reviews = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    handyman_id = db.Column(db.Integer, db.ForeignKey("handymans.handyman_id"))

    handyman = db.relationship("Handyman", backref="ratings")
    user = db.relationship("User", backref="ratings")

    def __repr__(self):
        return f"<Rating rating_id={self.rating_id} score={self.score} reviews={self.reviews}>"


class Question(db.Model):

    __tablename__ = "questions"

    question_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    handyman_id = db.Column(db.Integer, db.ForeignKey("handymans.handyman_id"))
    question = db.Column(db.Text)
    question_date = db.Column(db.Text)

    user = db.relationship("User", backref="questions")
    handyman = db.relationship("Handyman", backref="questions")

    def __repr__(self):
        return f"<Question question_id={self.question_id} question={self.question}  question_date={self.question_date}>"
 

class Answer(db.Model):

    __tablename__ = "answers"

    answer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    handyman_id = db.Column(db.Integer, db.ForeignKey("handymans.handyman_id"))
    question_id = db.Column(db.Integer, db.ForeignKey("questions.question_id"))
    answer = db.Column(db.Text)
    answer_date = db.Column(db.Text)

    handyman = db.relationship("Handyman", backref="answers")
    question = db.relationship("Question", backref="answers")

    def __repr__(self):
        return f"<Answer answer_id={self.answer_id} answer={self.answer}  answer_date={self.answer_date}>"



def connect_to_db(flask_app, db_uri="postgresql:///handyman", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

def test_models():
    user = User(first_name="Ione", last_name="Axelrod", email="i@poop.com", password="123")
    db.session.add(user)
    db.session.commit()

    handyman = Handyman(company_name="Hackbright", price_per_hour=9.3, user_id=user.user_id)
    service = Service(service_name="Unclog toilet")

    db.session.add(handyman)
    db.session.add(service)
    db.session.commit()
    
    handyman_service = HandymanService(handyman_id=handyman.handyman_id, service_id = service.service_id)
    db.session.add(handyman_service)
    db.session.commit()
    
    print("User Info", User.query.all())    
    print("Handyman Info", Handyman.query.all())
    print("Service Info", Service.query.all())
    print("Handyman Service Info", HandymanService.query.all())



def test_query():
    #sum = 0
    h = Handyman.query.filter(Handyman.handyman_id == 45).first()
    h = Handyman.query.filter(Handyman.company_name == "Test handyman100").first()
    service_name = "cleaning"
    handyman_list = []
    all_handyman = Handyman.query.all()
    for handyman in all_handyman:
        #if not empty list
        if handyman.services:
            for service in handyman.services:
                if service.service_name == service_name:
                    #print("Services:", service_name)
                    #if service_name_result == service_name:
                    handyman_list.append(handyman)
    result = handyman_list
    print(result)

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
    #db.create_all()
    #test_models()
    test_query()
