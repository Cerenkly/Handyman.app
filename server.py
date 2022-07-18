# from tkinter import N
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud
import os
import requests
from jinja2 import StrictUndefined
import haversine as hs
from haversine import Unit

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""

    if "email" in session:
        user_email = session["email"]
    else:
        user_email = session["email"] = {}

    #return render_template("homepage.html", user_email = user_email)
    return render_template("homepage.html")

@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/contact")
def contact():

    return render_template("contact.html")

@app.route("/logout")
def logout():
    session["email"] = {}
    session["company_name"] = {}
    #return render_template("homepage.html")
    return redirect("/")

@app.route("/users", methods=["POST"])
def register_user():
    # first_name = request.form.get("first_name")
    # last_name = request.form.get("last_name")
    # user_address = request.form.get("user_address")
    # email = request.form.get("email")
    # password = request.form.get("password")

    first_name = request.get_json().get("first_name")
    last_name = request.get_json().get("last_name")
    user_address = request.get_json().get("address")
    email = request.get_json().get("email")
    session["email"] = email
    password = request.get_json().get("password")
    
    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password,user_address)
        db.session.add(user)
        db.session.commit()
        #flash("Account created! Please log in.")

    return jsonify({"success": True})

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    #return render_template("test.html", test=company_name)
    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["email"] = user.email

        if user.handyman:
            company_name = user.handyman[0].company_name
            price_per_hour = user.handyman[0].price_per_hour
            handyman_id = user.handyman[0].handyman_id
            #service_names = user.handyman[0].services_names

            #phone_number = user.hamdyman[0].phone_number
            #flash(f"Welcome back, {user.email}!")
            session["company_name"] = company_name
            session["price_per_hour"]=price_per_hour
            #session["service_names"]=service_names
            #session["phone_number"]=phone_number


    return redirect("/")

@app.route("/create_account")
def register_page():
    return render_template("create_account.html")

@app.route("/handyman_account")
def handyman_register_page():
    return render_template("handyman_account.html")  

@app.route("/create_handyman", methods=["POST"])
def register_handyman():
    
    company_name = request.form.get("company_name")
    price_per_hour = request.form.get("price_per_hour")
    radius = request.form.get("radius")
    zip_code = request.form.get("zip_code")
    phone_number = request.form.get("phone_number")
    paint_flag = request.form.get("painting")
    clean_flag = request.form.get("cleaning")
    move_flag = request.form.get("moving")


    #paint_service = crud.get_service_by_name(paint_flag)
    #return render_template("test.html", test=paint_service)
    
    handyman = crud.get_handyman_by_name(company_name)

    if session["company_name"]:
        return redirect("/handyman_profile")
    elif handyman:
        flash("Cannot create an account with that name. Try again.")
        return redirect("/handyman_account")
    else:
        service_id = []
        service_names = ""

        if paint_flag is not None:
            paint_service = crud.get_service_by_name(paint_flag)
            service_id.append(paint_service.service_id)
            #service_names.append(paint_service.service_name)
            service_names = service_names + paint_service.service_name + " "
        if clean_flag is not None:
            clean_service = crud.get_service_by_name(clean_flag)
            service_id.append(clean_service.service_id)
            #service_names.append(clean_service.service_name)
            service_names = service_names + clean_service.service_name + " "
        if move_flag is not None:
            move_service = crud.get_service_by_name(move_flag)
            service_id.append(move_service.service_id)
            #service_names.append(move_service.service_name)
            service_names = service_names + move_service.service_name + " "

        #return render_template("test.html", service_id=paint_service.service_name)

        user = crud.get_user_by_email(session["email"])
        handyman = crud.create_handyman(company_name, price_per_hour, radius, zip_code, phone_number, user.user_id)
        db.session.add(handyman)
        db.session.commit()

        handy_obj = crud.get_handyman_by_name(company_name)
        handy_id = handy_obj.handyman_id
        if service_id:
            for s in service_id:
                handy_service = crud.create_handyman_service(handy_id, s)
                db.session.add(handy_service)
            db.session.commit()
        flash("Account created! Please log in.")

        session["company_name"]=company_name
        session["price_per_hour"]=price_per_hour
        session["service_names"]=service_names
        session["phone_number"]=phone_number
        return render_template("handyman_profile.html", company_name=company_name, price_per_hour=price_per_hour, service_names=service_names, phone_number=phone_number)


@app.route("/handyman_profile")
def get_handyman_profile():
    return render_template("handyman_profile.html", company_name=session["company_name"], price_per_hour=session["price_per_hour"], service_names=session["service_names"], phone_number=session["phone_number"])

@app.route("/search_result")
def api_call():
    search_input = request.args.get("search")
    #company_list_db = crud.get_company_by_service_name(search_input)
    #return render_template("test.html", test=company_list_db)

    handyman_list = []
    headers = {'Authorization': f"Bearer {os.environ['YELP_MASTER_KEY']}"}
    url='https://api.yelp.com/v3/businesses/search'
    payload = {'location' : '92110',
                'radius' : 20000,
                'categories' : 'handyman, homecleaning, movers, painters, All',
                'term' : search_input}

    response = requests.get(url, params=payload, headers=headers)
    #print(response.url)
    #data = response.json()
    #return render_template("test.html", test=data["businesses"])
    data = response.json()
    print('\n'*5)
    print(data)
    print('\n'*5)

    #print(data["businesses"])
    #for dict in data["businesses"]:
    #    handyman_list.append(dict["name"])

    #print(handyman_list)
    #handyman_list.extend(company_list_db)
    session["yelp_results"] = data["businesses"]

    all_handymans_in_db= crud.get_handyman_by_service_name(search_input)
    #return render_template("test.html", test=test)

    return render_template("search_results.html", handyman_list_html=data["businesses"], handyman_list_html_db=all_handymans_in_db)

@app.route("/db/search_result", methods=["POST"])
def react_db_call():
    search_input = request.get_json().get("service")
    zip_code = request.get_json().get("zip_code")
    lat, lng = None, None
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={zip_code}&key={os.environ['Google_map_key']}"
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''
        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass
    search_loc = (lat,lng)
    
    # loc1=(28.426846,77.088834)
    # loc2=(28.394231,77.050308)
    # hs.haversine(loc1,loc2,unit=Unit.MILES)

    all_handymans_in_db= crud.get_handyman_by_service_name(search_input)
    dict = {}
    count = 0
    for handyman in all_handymans_in_db:
        hLat, hLng = None, None
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        endpoint = f"{base_url}?address={handyman.zip_code}&key={os.environ['Google_map_key']}"
        r = requests.get(endpoint)
        if r.status_code not in range(200, 299):
            return None, None
        try:
            '''
            This try block incase any of our inputs are invalid. This is done instead
            of actually writing out handlers for all kinds of responses.
            '''
            hResults = r.json()['results'][0]
            hLat = hResults['geometry']['location']['lat']
            hLng = hResults['geometry']['location']['lng']
        except:
            pass
        handyman_loc = (hLat,hLng)
        distance = hs.haversine(search_loc,handyman_loc,unit=Unit.MILES)
        if distance < 100:
            dict[count] = {"name" : handyman.company_name, "id" : handyman.handyman_id, "zip_code" : handyman.zip_code, "radius" : handyman.radius, "lat" : hLat, "lng" : hLng}
            count = count+1

    return dict
    #return jsonify({"success": True})

@app.route("/api/search_result", methods=["POST"])
def react_api_call():
    #search_input = request.args.get("search")
    search_input = request.get_json().get("service")
    zip_code = request.get_json().get("zip_code")

    handyman_list = []
    headers = {'Authorization': f"Bearer {os.environ['YELP_MASTER_KEY']}"}
    url='https://api.yelp.com/v3/businesses/search'
    payload = {'location' : zip_code,
                'radius' : 20000,
                'categories' : 'handyman, homecleaning, movers, painters, All',
                'term' : search_input}

    response = requests.get(url, params=payload, headers=headers)
    data = response.json()
    print('\n'*5)
    print(data)
    print('\n'*5)
    return data
    #return render_template("test.html", test=data["businesses"])

    #print(data["businesses"])
    #for dict in data["businesses"]:
    #    handyman_list.append(dict["name"])

    #print(handyman_list)
    #handyman_list.extend(company_list_db)
    # session["yelp_results"] = data["businesses"]

    # all_handymans_in_db= crud.get_handyman_by_service_name(search_input)

    # return render_template("search_results.html", handyman_list_html=data["businesses"], handyman_list_html_db=all_handymans_in_db)

@app.route("/search_result/<id>")
def show_company_profile(id):
    current_user_email = session["email"]

    if current_user_email:
        current_user_obj = crud.get_user_by_email(current_user_email)
    else:
        current_user_obj = None

    try:
        x = int(id)
        handyman_db = crud.get_handyman_by_id(id)
        yelp = 0
    except ValueError:
        yelp = 1
        handyman_db = 0
        headers = {'Authorization': f"Bearer {os.environ['YELP_MASTER_KEY']}"}
        url='https://api.yelp.com/v3/businesses/' + id

        response = requests.get(url, headers=headers)
        data = response.json()
        session["current_yelp_business"] = data

    
        reviews_url='https://api.yelp.com/v3/businesses/' + id + '/reviews'

        response = requests.get(reviews_url, headers=headers)
        reviews_data = response.json()
        #handyman_company_name = crud.get_handyman_by_id(handyman.handyman_id)
    
  

    #handyman_db = crud.get_handyman_by_id(id)
    if handyman_db:
        #if inside our table
        handyman=handyman_db
    else:
        #otherwise check if company_name is in handyman table
        handyman = crud.get_handyman_by_name(data["name"])
    
   
    average="No rating"
    rating = None
    if handyman:
        rating = crud.get_rating_by_handyman_id(handyman.handyman_id)
    

        if rating:
            sum = 0
            for x in rating:
                sum = sum + x.score
    
            average = round(sum/len(rating), 1)
            #return render_template("test.html", test=average)

    display = 1
    score = -1
    #return render_template("test.html", test=rating)

    if handyman:
        if current_user_obj:
            for user_rating in current_user_obj.ratings:
                if user_rating.handyman.handyman_id == handyman.handyman_id:
                    
                    score = user_rating.score
                    display = 0

    #return render_template("test.html", test=current_user_obj)
    if yelp:
        #return render_template("test.html", test=data)
        return render_template("company_profile.html", handyman=data, rating=average, display=display, score=score, reviews=reviews_data["reviews"], reviews_db=rating)
    else:
        return render_template("company_profile_db.html", handyman=handyman, rating=average, current_user_obj=current_user_obj, display=display, score=score, reviews=rating)

@app.route("/search_result/<id>/reviews")
def show_company_reviews(id):

    try:
        x = int(id)
        handyman_db = crud.get_handyman_by_id(id)
        yelp = 0
    except ValueError:
        yelp = 1
        handyman_db = 0

    headers = {'Authorization': f"Bearer {os.environ['YELP_MASTER_KEY']}"}
    url='https://api.yelp.com/v3/businesses/' + id + '/reviews'

    response = requests.get(url, headers=headers)
    data = response.json()
    session["current_yelp_business"] = data

    
    handyman = crud.get_handyman_by_name(data["text"])


    return redirect(f"/search_result/{id}")


@app.route("/update_rating", methods=["POST"])
def update_rating():
    rating_id = request.json["rating_id"]
    updated_score = request.json["updated_score"]
    crud.update_rating(rating_id, updated_score)
    db.session.commit()

    return "Success"

@app.route("/search_result/<handyman_id>/ratings", methods=["POST"])
def create_rating(handyman_id):
    """Create a new rating for the movie."""

    logged_in_email = session.get("email")
    rating_score = request.form.get("rating")
    reviews = request.form.get("reviews")
    #return render_template("test.html", test=review)
    if logged_in_email is None:
        flash("You must log in to rate a handyman.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
    
        try:
            x = int(handyman_id)
            yelp = 0
            handyman = crud.get_handyman_by_id(handyman_id)
        except ValueError:
            yelp = 1
            yelp_handyman = session.get("current_yelp_business")
            handyman= crud.get_handyman_by_name(yelp_handyman["name"])
            #headers = {'Authorization': f"Bearer {os.environ['YELP_MASTER_KEY']}"}
            #url='https://api.yelp.com/v3/businesses/' + handyman_id

            #response = requests.get(url, headers=headers)
            #handyman = response.json()

        #return render_template("test.html", test=handyman)

        if handyman is None:
            handyman = crud.create_yelp_handyman(yelp_handyman["name"], yelp_handyman["location"]["zip_code"])
            db.session.add(handyman)
            db.session.commit()

            #handyman= crud.get_handyman_by_name(yelp_handyman["name"])

        #return render_template("test.html", test=handyman.user_id)
        rating = crud.create_rating(user.user_id, handyman.handyman_id, reviews, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this handyman {rating_score} out of 5.")

    return redirect(f"/search_result/{handyman_id}")

@app.route("/search_result/<handyman_id>/question", methods=["POST"])
def question(handyman_id):
    logged_in_email = session.get("email")
    question = request.form.get("question")

    if logged_in_email is None:
        flash("You must log in to rate a handyman.")
    else:
        user = crud.get_user_by_email(logged_in_email)

        try:
            x = int(handyman_id)
            yelp = 0
            handyman = crud.get_handyman_by_id(handyman_id)
        except ValueError:
            yelp = 1
            yelp_handyman = session.get("current_yelp_business")
            handyman= crud.get_handyman_by_name(yelp_handyman["name"])

        #if handyman does not exist
        if handyman is None:
            handyman = crud.create_yelp_handyman(yelp_handyman["name"], yelp_handyman["location"]["zip_code"])
            db.session.add(handyman)
            db.session.commit()

        question_obj = crud.create_question(user.user_id, handyman.handyman_id, question)
        db.session.add(question_obj)
        db.session.commit()
        return redirect(f"/search_result/{handyman_id}")

@app.route("/search_result/<handyman_id>/<question_id>/answer", methods=["POST"])
def answer(handyman_id, question_id):
    name = "answer_"+question_id
    answer = request.form.get(name)
    answer_obj = crud.create_answer(handyman_id, question_id, answer)
    db.session.add(answer_obj)
    db.session.commit()
    return redirect(f"/search_result/{handyman_id}")
    #return render_template("test.html", test=answer)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    #db.create_all()
