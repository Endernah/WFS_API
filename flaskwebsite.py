import flightsmanager, json, os
from flask import Flask, redirect, url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from datetime import datetime

app = Flask(__name__)

app.secret_key = b"random bytes to crack in jaydens mother in her basement"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

app.config["DISCORD_CLIENT_ID"] = 1162221005901660240    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = str(open('secret.txt', 'r').read())
app.config["DISCORD_REDIRECT_URI"] = "https://wingedflights.com/callback"
app.config["DISCORD_BOT_TOKEN"] = str(open('token.txt', 'r').read())

discord = DiscordOAuth2Session(app)

@app.route("/")
def index():
    return '''
    <html>
        <head>
            <meta name='verify-v1' content='unique-string'>
            <title>Winged Flights</title>
            <script>
                setTimeout(function(){
                    window.location.href = "/login";
                }, 1000);
            </script>
        </head>
        <body>
            <a>Redirecting...</a>
        </body>
    </html>
    '''

@app.route("/login")
def login():
    return discord.create_session(scope=['identify'])

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("/"))

@app.route("/callback")
def callback():
    discord.callback()
    return redirect(url_for("flights"))

@app.route("/flights")
def flights():
    user = discord.fetch_user()
    flightsRespond = ''
    flights = flightsmanager.getFlights()
    for flight, details in flights.items():
        time = datetime.utcfromtimestamp(details['time']).strftime('%Y-%m-%d %H:%M UTC')
        flightsRespond += f"{flight} · {details['aircraft']} · {time}<br>"
    return f"Hello, {user.name}. <br>Flights:<br> {flightsRespond}"

def run():
    app.run(host="0.0.0.0", port=80, debug=False)