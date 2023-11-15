import flightsmanager, json, datetime, os
from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

app = Flask(__name__)

app.secret_key = b"random bytes to crack in jaydens mother in her basement"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

app.config["DISCORD_CLIENT_ID"] = 1162221005901660240    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = str(open('secret.txt', 'r').read())
app.config["DISCORD_REDIRECT_URI"] = "http://localhost/callback"
app.config["DISCORD_BOT_TOKEN"] = str(open('token.txt', 'r').read())

discord = DiscordOAuth2Session(app)

@app.route("/")
def index():
    return discord.create_session(scope=["identify"])

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("/"))

@app.route("/callback")
def callback():
    discord.callback()
    return redirect(url_for(".flights"))

@app.route("/flights")
def flights():
    user = discord.fetch_user()
    return f"Hello, {user.name}. Flights: {flightsmanager.getFlights()}"

def run():
    app.run(host="0.0.0.0", port=80, debug=False)