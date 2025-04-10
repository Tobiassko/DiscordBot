import discord
import os
from dotenv import load_dotenv
import random
import requests  # Add this import for downloading files
import json
# Function to fetch Pokémon data from PokeAPI
def download_poke_data(pokidex_entrie, wipe=False):
    if wipe == True:
        os.remove("pokemon\poke.json")
    url = f"https://pokeapi.co/api/v2/pokemon/{pokidex_entrie}"
    response = requests.get(url)
    poke_info = response.json()
    with open(os.path.join("pokemon", "poke.json"), "wb") as file:
        file.write(json.dumps(poke_info, indent=4).encode('utf-8'))

def get_poke_data(field):
    with open(os.path.join("pokemon", "poke.json"), "r") as file:
        data = json.load(file)
        if field in data:
            return data[field]
        else:
            print(f"Field '{field}' not found in Pokemon data")
            return None

meme = True

# load Token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Called when successfully connects"""
    print(f"Test successful! Logged in as {client.user}")
    print(f"Bot is in {len(client.guilds)} servers")
    print(f"Bot is Ready!")

baned_ids = [
1359822255437119610,
# 414451002217988097
]

@client.event
async def on_message(message):
    """All the on message commands"""
    if message.author == client.user:
        return
    if message.author.id in baned_ids:
        return
    if message.content == "!" or message.content == "!help":
        await message.channel.send(
"""**Here are all the commands**:

📜 **!help** - Displays this list of commands.
✅ **!test** - Checks if the bot is operational.
🏃 **ran** - Sends an emoji of a man running.
🎲 **rand** - Generates a random number between 1 and 1000.
🚗 **!car** - Sends a video of a car from awesomecars.neocities.org.
👤 **!user** - Fetches your information or details of a specific user.
"""
        )
    if message.content == "!test":
        await message.channel.send("Bot is working!")
    if message.content == "!ran":
        await message.channel.send("🏃‍♂️‍➡️")
    if message.content == "!rand":
        await message.channel.send(f"Here is a random number:{random.randint(0,1000)}")
    
    if message.content.startswith("!user"):
        parts = message.content.split()
        if len(parts) > 1:
            user_id = int(parts[1].strip("<@!>"))
            user = await client.fetch_user(user_id)
            embed = discord.Embed(title="User Info", color=discord.Color.blue())
            embed.add_field(name="Username", value=user.name, inline=False)
            embed.add_field(name="Discriminator", value=f"#{user.discriminator}", inline=False)
            embed.add_field(name="ID", value=user.id, inline=False)
            embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
            await message.channel.send(embed=embed)
        else:
            user = message.author
            embed = discord.Embed(title="Your Info", color=discord.Color.green())
            embed.add_field(name="Username", value=user.name, inline=False)
            embed.add_field(name="Discriminator", value=f"#{user.discriminator}", inline=False)
            embed.add_field(name="ID", value=user.id, inline=False)
            embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
            await message.channel.send(embed=embed)
    if message.content.startswith("!car"):
        parts = message.content.split()
        if len(parts) > 1 and parts[1]:
            print("Choosing specific car")
            random_number = int(parts[1])
        else:
            print("Choosing random car")
            random_number = random.randint(1, 2579)
        url = f"https://awesomecars.neocities.org/ver2/{random_number}.mp4"
        car_folder = "Car"
        os.makedirs(car_folder, exist_ok=True)  # Ensure the Car folder exists
        local_filename = os.path.join(car_folder, f"car_{random_number}.mp4")

        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        with open(local_filename, 'wb') as file:
            file.write(response.content)
        
        await message.channel.send(file=discord.File(local_filename))
        os.remove(local_filename)
    global meme
    if meme == True:
        if "money" in message.content.lower():
            await message.channel.send(file=discord.File(os.path.join("mems\Mr. Krabs - Money.mp4")))
        if "10" in message.content.lower():
            await message.channel.send(file=discord.File("mems\yakuza-nishikiyama.gif"))
        if "baby" in message.content.lower():
            await message.channel.send(file=discord.File(os.path.join("mems", "dust_baby.jpg")))
        if "591" in message.content:
            download_poke_data(591)
            embed = discord.Embed(title="pokemon", )
            embed.add_field(name="Name:", value=str(get_poke_data("name")).capitalize())
            embed.add_field(name="Id:", value=get_poke_data("id"))
            if len(get_poke_data("types")) > 1:
                    embed.add_field(name=f"Types:", value=(f"{str(get_poke_data("types")[0]["type"]["name"]).capitalize()} and {str(get_poke_data("types")[1]["type"]["name"]).capitalize()}"))
            else:
                embed.add_field(name="Type:", value=get_poke_data("types")[0]["type"]["name"])
            if len(get_poke_data("abilities")) > 1:
                embed.add_field(name="Ability", value=str(get_poke_data("abilities")[0]["ability"]["name"]).replace("-", " ").capitalize())
                embed.add_field(name="Hidden Ability", value=str(get_poke_data("abilities")[1]["ability"]["name"]).replace("-", " ").capitalize())
            else:
                embed.add_field(name="Ability", value=str(get_poke_data("abilities")[0]["ability"]["name"]).replace("-", " ").capitalize())
            embed.add_field(name="Hp:", value=get_poke_data("stats")[0]["base_stat"], inline=False)
            embed.add_field(name="Attack:", value=get_poke_data("stats")[1]["base_stat"])
            embed.add_field(name="Special Attack:", value=get_poke_data("stats")[3]["base_stat"])
            embed.add_field(name="Defense:", value=get_poke_data("stats")[2]["base_stat"])
            embed.add_field(name="Special Defense:", value=get_poke_data("stats")[4]["base_stat"])
            embed.add_field(name="Speed:", value=get_poke_data("stats")[5]["base_stat"])
            embed.set_thumbnail(url=get_poke_data("sprites")["front_default"])
            await message.channel.send(embed=embed)
            os.remove(os.path.join("pokemon", "poke.json"))
    if message.content.startswith("!poke"):
        parts = message.content.split()
        if len(parts) > 1 and int(parts[1]) <= 1025:
            download_poke_data(parts[1])
        else:
            download_poke_data(random.randint(1,1025))
        embed = discord.Embed(title="pokemon", color=discord.Colour.blue())
        embed.add_field(name="Name:", value=str(get_poke_data("name")).capitalize())
        embed.add_field(name="Id:", value=get_poke_data("id"))
        if len(get_poke_data("types")) > 1:
                embed.add_field(name=f"Types:", value=(f"{str(get_poke_data("types")[0]["type"]["name"]).capitalize()} and {str(get_poke_data("types")[1]["type"]["name"]).capitalize()}"))
        else:
            embed.add_field(name="Type:", value=get_poke_data("types")[0]["type"]["name"])
        if len(get_poke_data("abilities")) > 1:
            embed.add_field(name="Ability", value=str(get_poke_data("abilities")[0]["ability"]["name"]).replace("-", " ").capitalize())
            embed.add_field(name="Hidden Ability", value=str(get_poke_data("abilities")[1]["ability"]["name"]).replace("-", " ").capitalize())
        else:
            embed.add_field(name="Ability", value=str(get_poke_data("abilities")[0]["ability"]["name"]).replace("-", " ").capitalize())
        embed.add_field(name="Hp:", value=get_poke_data("stats")[0]["base_stat"], inline=False)
        embed.add_field(name="Attack:", value=get_poke_data("stats")[1]["base_stat"])
        embed.add_field(name="Special Attack:", value=get_poke_data("stats")[3]["base_stat"])
        embed.add_field(name="Defense:", value=get_poke_data("stats")[2]["base_stat"])
        embed.add_field(name="Special Defense:", value=get_poke_data("stats")[4]["base_stat"])
        embed.add_field(name="Speed:", value=get_poke_data("stats")[5]["base_stat"])
        embed.set_thumbnail(url=get_poke_data("sprites")["front_default"])
        await message.channel.send(embed=embed)
        os.remove(os.path.join("pokemon", "poke.json"))
    if message.content == "!meme" and message.author.id == 394213071381463040:
        if meme == False:
            await message.channel.send("Meme commands have been turned on")
            meme = True
        else:
            await message.channel.send("Meme commands have been turned Off")
            meme = False
    elif message.content == "!meme" and message.author.id != 394213071381463040:
        await message.author.send("Sorry, only the bot owner can use the command !meme")

    

if __name__ == "__main__":
    print("Starting bot...")
    client.run(TOKEN)