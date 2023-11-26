import multiprocessing
import discordapp
from flask import Flask, redirect

def run_discord():
    discordapp.run()
discord_process = multiprocessing.Process(target=run_discord)
discord_process.start()

app = Flask(__name__)
@app.route("/")
def index():
    return redirect("https://wingedflights.com/discord")

@app.route("/discord")
def discord():
    return redirect("https://discord.gg/g68vFbMyHK")

app.run(host="0.0.0.0", port=80, debug=False)
