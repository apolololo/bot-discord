import discord
from discord.ext import commands
from discord import app_commands
import requests
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}!')

@bot.tree.command(name="joke")
async def joke(interaction: discord.Interaction):
    response = requests.get("https://v2.jokeapi.dev/joke/Any")
    joke = response.json()
    if joke["type"] == "single":
        await interaction.response.send_message(joke["joke"])
    else:
        await interaction.response.send_message(f'{joke["setup"]}\n{joke["delivery"]}')

@bot.tree.command(name="weather")
async def weather(interaction: discord.Interaction, city: str):
    api_key = os.getenv('WEATHER_API_KEY')
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
    data = response.json()
    if data["cod"] != 200:
        await interaction.response.send_message(f"City {city} not found.")
    else:
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        await interaction.response.send_message(f"The weather in {city} is {weather_desc} with a temperature of {temp}°C.")

@bot.tree.command(name="quote")
async def quote(interaction: discord.Interaction):
    response = requests.get("https://api.quotable.io/random")
    quote = response.json()
    await interaction.response.send_message(f'"{quote["content"]}" - {quote["author"]}')

bot.run(os.getenv('DISCORD_TOKEN'))
