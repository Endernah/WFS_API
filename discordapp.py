import flightsmanager
import discord, asyncio, json, datetime, time
from discord import app_commands, Embed
from discord.ext import ipc

class InitClient(discord.Client):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.ipc = ipc.Server(self,secret_key = str(open('ipc.txt', 'r').read()))

    async def on_ready(self):
        """Called upon the READY event"""
        print("Bot is ready.")

    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        print("Ipc server is ready.")

    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""
        print(endpoint, "raised", error)

client = InitClient(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    global ready
    await tree.sync(guild=discord.Object(id=1160373156134015058))
    print(f'Ready {client.user}')

@tree.command(name = "flights", description = "Gets the current flights", guild=discord.Object(id=1160373156134015058))
async def command_flights(interaction):
    flights = flightsmanager.getFlights()
    embed = Embed(title="Current Flights", description="Here are the current flights:", color=0x5CDBF0)
    for flight, details in flights.items():
        embed.add_field(name=f"{flight} · {details['aircraft']} · <t:{details['time']}>", value=f"", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name = "createflight", description = "Creates new flight", guild=discord.Object(id=1160373156134015058))
async def command_createflight(interaction, callsign: str, time: int, aircraft: str):
    if "1163207937284649151" in f"{interaction.guild.get_member(interaction.user.id).roles}" or "1163207937976705096" in f"{interaction.guild.get_member(interaction.user.id).roles}":
        await interaction.response.send_message(f"Created: {str(flightsmanager.createFlight(callsign, time, aircraft))}")
    else:
        await interaction.response.send_message("You do not have permission to use this command.")

@tree.command(name = "deleteflight", description = "Deletes a flight", guild=discord.Object(id=1160373156134015058))
async def command_deleteflight(interaction, callsign: str):
    if "1163207937284649151" in f"{interaction.guild.get_member(interaction.user.id).roles}" or "1163207937976705096" in f"{interaction.guild.get_member(interaction.user.id).roles}":
        await interaction.response.send_message(f"{str(flightsmanager.deleteFlight(callsign))}")
    else:
        await interaction.response.send_message("You do not have permission to use this command.")

@client.ipc.route()
async def get_guild_ids(user_id, message):
    user = await client.fetch_user(user_id)
    await user.send(message)


def run():
    client.ipc.start()
    client.run(str(open('token.txt', 'r').read()))