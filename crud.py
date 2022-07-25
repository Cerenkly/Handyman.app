from model import db, User, Handyman, HandymanService, Service, Rating, Comment, Question, Answer, connect_to_db

def create_user(first_name, last_name, email, password, user_address):
    """Create and return a new user."""

    user = User(
        first_name= first_name, 
        last_name=last_name, 
        email=email, 
        password=password, 
        user_address= user_address
        #profile_pic= profile_pic
        )

    return user


def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()    

def create_handyman(company_name, price_per_hour, radius, zip_code, phone_number, user_id): 

    handyman = Handyman(
        company_name=company_name,
        price_per_hour=price_per_hour,
        radius=radius,
        zip_code=zip_code,
        phone_number= phone_number,
        user_id=user_id
    )

    return handyman    

def create_yelp_handyman(company_name, zip_code): 

    handyman = Handyman(
        company_name=company_name,
        radius=160000,
        zip_code=zip_code,
    )

    return handyman    


def get_handymans():

     return Handyman.query.all()

def get_company_by_service_name(service_name):
    """Return company name by service name"""
    company_list = []
    all_handyman = get_handymans()
    for handyman in all_handyman:
        #if not empty list
        if handyman.services:
            service_name_result = handyman.services[0].service_name
            #print("Services:", service_name)
            if service_name_result == service_name:
                company_list.append(handyman.company_name)
    return company_list


def get_handyman_by_service_name(service_name):

    handyman_list = []
    all_handyman = get_handymans()
    for handyman in all_handyman:
        #if not empty list
        if handyman.services:
            for service in handyman.services:
                if service.service_name == service_name:
                    #print("Services:", service_name)
                    #if service_name_result == service_name:
                    handyman_list.append(handyman)
    return handyman_list



def get_handyman_by_name(company_name):

    return Handyman.query.filter(Handyman.company_name == company_name).first()  


def get_handyman_by_id(handyman_id):
    """Return a handyman by primary key."""

    return Handyman.query.get(handyman_id)


def create_rating(user_id, handyman_id, reviews, score):
    """Create and return a new rating."""

    #rating = Rating(user=user, score=score, handyman=handyman)
    rating = Rating(user_id=user_id, handyman_id=handyman_id, reviews=reviews, score=score)

    return rating

def create_question(user_id, handyman_id, question):
    """Create and return a new question."""

    question = Question(user_id=user_id, handyman_id=handyman_id, question=question)

    return question

def create_answer(handyman_id, question_id, answer):
    """Create and return a new answer."""

    answer = Answer(handyman_id=handyman_id, question_id=question_id, answer=answer)

    return answer

def get_rating_by_handyman_id(handyman_id):
    rating = Rating.query.filter(Rating.handyman_id == handyman_id).all()
    return rating


def update_rating(rating_id, new_score):
    """ Update a rating given rating_id and the updated score. """
    rating = Rating.query.get(rating_id)
    rating.score = new_score     


def create_service(service_name):
    service = Service(service_name=service_name)
    return service

def get_service_by_name(service_name):
    service_obj = Service.query.filter(Service.service_name == service_name).first()
    return service_obj

def create_handyman_service(handy_id, service_id):
    handyman_service = HandymanService(handyman_id=handy_id, service_id=service_id)
    return handyman_service

def get_handymanid_by_serviceid(service_id):
    HandymanService.query.filter()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)