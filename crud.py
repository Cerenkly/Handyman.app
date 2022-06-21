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

def create_handyman(company_name, price_per_hour, radius, zip_code): 

    handyman = Handyman(
        company_name=company_name,
        price_per_hour=price_per_hour,
        radius=radius,
        zip_code=zip_code,
    )

    return handyman    

def get_handymans():

     return Handyman.query.all()


def get_handyman_by_id(handyman_id):
    """Return a handyman by primary key."""

    return Handyman.query.get(handyman_id)


def create_rating(user, movie, score):
    """Create and return a new rating."""

    #rating = Rating(user=user, score=score, handyman=handyman)
    rating = Rating(user=user, score=score)

    return rating


def update_rating(rating_id, new_score):
    """ Update a rating given rating_id and the updated score. """
    rating = Rating.query.get(rating_id)
    rating.score = new_score     


if __name__ == "__main__":
    from server import app
    connect_to_db(app)