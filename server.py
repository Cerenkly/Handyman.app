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

    return render_template("homepage.html")

@app.route("/users", methods=["POST"])
def register_user():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    user_address = request.form.get("user_address")
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password,user_address)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")   

@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")

@app.route("/create_account")
def register_page():
    return render_template("create_account.html")

@app.route("/search_result")
def api_call():
    handyman_list = []
    headers = {'Authorization': f"Bearer {os.environ['YELP_MASTER_KEY']}"}
    url='https://api.yelp.com/v3/businesses/search'
    payload = {'location' : '92110',
                'radius' : 2000,
                'categories' : 'handyman, All'}

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
