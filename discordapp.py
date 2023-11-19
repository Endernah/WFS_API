import flightsmanager
import communicationmanager
import discord
import time, threading, asyncio
from discord import app_commands, Embed
from discord.ext import ipc

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

async def senddm(callsign, user_id):
    user = client.get_user(user_id)
    if user:
        guild = client.get_guild(1160373156134015058)
        role = discord.utils.get(guild.roles, name=callsign)
        guildmember = guild.get_member(user.id)
        if f"{role.id}" in f"{guildmember.roles}":
            pass
        else:
            embed = discord.Embed(title="Flight Booked", description=f"Hello, {user.display_name}. Your flight, {callsign} has been booked.", color=0x5CDBF0)
            await user.send(embed=embed)
            await guildmember.add_roles(guild.get_role(role.id))

async def checkForRequests():
    while True:
        request = communicationmanager.recieverequests()
        if request:
            if request["function"] == "book":
                await senddm(request["args"]["callsign"], request["args"]["user_id"])
        await asyncio.sleep(0.1)

@client.event
async def on_ready():
    global ready
    await tree.sync(guild=discord.Object(id=1160373156134015058))
    print(f'Ready {client.user}')
    await checkForRequests()

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


def run():
    client.run(str(open('token.txt', 'r').read()))