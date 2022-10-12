import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, request, render_template, session, url_for


ENV_FILE = find_dotenv()
if ENV_FILE:
	load_dotenv(ENV_FILE)
	
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
	"auth0",
	client_id=env.get("AUTH0_CLIENT_ID"),
	client_secret=env.get("AUTH0_CLIENT_SECRET"),
	client_kwargs={
		"scope": "openid profile email",
	},
	server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

stays = []

@app.route("/login")
def login():
	return oauth.auth0.authorize_redirect(
		redirect_uri=url_for("callback", _external=True)
	)

@app.route("/callback", methods=["GET", "POST"])
def callback():
	token = oauth.auth0.authorize_access_token()
	session["user"] = token
	return redirect("/")

@app.route("/logout")
def logout():
	session.clear()
	return redirect(
		"https://" + env.get("AUTH0_DOMAIN")
		+ "/v2/logout?"
		+ urlencode(
			{
				"returnTo": url_for("home", _external=True),
				"client_id": env.get("AUTH0_CLIENT_ID"),
			},
			quote_via=quote_plus,
		)
	)

@app.route("/")
def home():
	return render_template("home.html", session=session.get('user'), stays=stays)

@app.post("/addStay")
def addStay():
	obj = {
		"title": request.form.get("title"),
		"location": request.form.get("location"),
		"status": "Available",
		"owner": {
			"email": session.get("user")["userinfo"]["email"],
			"nickname": session.get("user")["userinfo"]["nickname"]
		}
	}
	stays.append(obj)
	return redirect(url_for("home"))

@app.get("/reserveStay")
def reserveStay():
	for i in range(len(stays)):
		# Make sure stay is available before reserving
		if stays[i]["title"] == request.args.get("title") and stays[i]["status"] == "Available":
			stays[i]["guest"] = {
				"name": session.get("user")["userinfo"]["nickname"],
				"email": session.get("user")["userinfo"]["email"]
			}	
			stays[i]["status"] = "Unavailable"
			break
	return redirect(url_for("home"))

@app.get("/deleteStay")
def deleteStay():
	for i in range(len(stays)):
		#make sure that the requester is also the owner of the stay
		if stays[i]["title"] == request.args.get("title") and session.get("user")["userinfo"]["email"] == stays[i]["owner"]["email"]:
			del stays[i]
			break
	return redirect(url_for("home"))

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=env.get("PORT", 3000))