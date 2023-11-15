import flaskwebsite
import discordapp
import multiprocessing

def run_flask():
    flaskwebsite.run()

def run_discord():
    discordapp.run()

if __name__ == '__main__':
    discord_process = multiprocessing.Process(target=run_discord)
    discord_process.start()

    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()