from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
import os
import requests
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""
    """
    if "email" in session:
        user_email = session["email"]
    else:
        user_email = session["email"] = {}
    """
    #return render_template("homepage.html", user_email = user_email)
    return render_template("homepage.html")

@app.route("/logout")
def logout():
    session["email"] = {}
    session["company_name"] = {}
    #return render_template("homepage.html")
    return redirect("/")

@app.route("/users", methods=["POST"])
def register_user():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    user_address = request.form.get("user_address")
    email = request.form.get("email")
    session["email"] = email
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password,user_address)
        db.session.add(user)
        db.session.commit()
        #flash("Account created! Please log in.")

    return redirect("/")   

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user.handyman:
        company_name = user.handyman[0].company_name

    #return render_template("test.html", test=company_name)
    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["email"] = user.email
        #flash(f"Welcome back, {user.email}!")
    if user.handyman:
        session["company_name"] = company_name

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
        handyman = crud.create_handyman(company_name, price_per_hour, radius, zip_code, user.user_id)
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
        return render_template("handyman_profile.html", company_name=company_name, price_per_hour=price_per_hour, service_names=service_names)


@app.route("/handyman_profile")
def goto_handyman_profile():
    return render_template("handyman_profile.html", company_name=session["company_name"], price_per_hour=session["price_per_hour"], service_names=session["service_names"])

@app.route("/search_result")
def api_call():
    search_input = request.args.get("search")
    #return render_template("test.html", test=search_input)
    handyman_list = []
    headers = {'Authorization': f"Bearer {os.environ['YELP_MASTER_KEY']}"}
    url='https://api.yelp.com/v3/businesses/search'
    payload = {'location' : '92110',
                'radius' : 20000,
                'categories' : 'handyman, homecleaning, movers, painters, All',
                'term' : search_input}

    response = requests.get(url, params=payload, headers=headers)
    #print(response.url)
    data = response.json()
    #print(data)
    if '_embedded' in data:
        result = data['_embedded']['handyman']
    else:
        result = []
    #print(result)
    #print(data["businesses"])
    for dict in data["businesses"]:
        handyman_list.append(dict["name"])
        #print(dict["name"])
        #for key in dict:
        #    print(key)
    #print(handyman_list)
    return render_template("search_results.html", handyman_list_html=handyman_list)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    #db.create_all()
