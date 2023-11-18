import flightsmanager, json, os, asyncio, nest_asyncio, multiprocessing
import discordapp
from flask import Flask, redirect, url_for, request
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from datetime import datetime
from discordapp import send_dm, client, run
from discord.ext import ipc

def run_discord():
    discordapp.run()
discord_process = multiprocessing.Process(target=run_discord)
discord_process.start()

app = Flask(__name__)
ipc_client = ipc.Client(secret_key = str(open('ipc.txt', 'r').read()))

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
    return index()

@app.route("/callback")
def callback():
    discord.callback()
    return redirect(url_for("flights"))

nest_asyncio.apply()

@app.route("/book")
def book():
    callsign = request.args.get('callsign')
    user_id = request.args.get('user_id')
    flight = flightsmanager.getFlight(callsign)
    if flight != "Flight not found.":
        return f'Flight {callsign} booked!'
    else:
        return 'No flight found.', 400

@app.route("/flights")
def flights():
    user = discord.fetch_user()
    flightsRespond = ''
    flights = flightsmanager.getFlights()
    for flight, details in flights.items():
        time = datetime.utcfromtimestamp(details['time']).strftime('%Y-%m-%d %H:%M UTC')
        flightsRespond += f'''
        {flight} · {details['aircraft']} · {time}<br>
        <form action="/book?callsign={flight}" method="get">
            <input type="hidden" name="callsign" value="{flight}">
            <input type="submit" value="Book this flight">
        </form>
        <br>
        '''
    return f'''
    <head>
        <meta name='verify-v1' content='unique-string'>
        <title>Winged Flights</title>
    </head>
    <body>
        <a>Hello, {user.name}. <br>Flights:<br> {flightsRespond}</a>
    </body>
    '''

app.run(host="0.0.0.0", port=80, debug=False)