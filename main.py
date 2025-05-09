import discord
import os
from dotenv import load_dotenv
import random
import requests  # Add this import for downloading files
import json
import csv
import math
import asyncio

# Function to fetch Pokémon data from PokeAPI
def download_poke_data(pokidex_entrie, wipe=False):
    if wipe == True and os.path.exists(os.path.join("pokemon", "poke.json")):
        os.remove(os.path.join("pokemon", "poke.json"))
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokidex_entrie.lower() if isinstance(pokidex_entrie, str) else pokidex_entrie}")
    if response.status_code != 200:
        print(f"Error: Pokemon not found. Status code: {response.status_code}")
        return False
    
    with open(os.path.join("pokemon", "poke_species.json"), "wb") as file:
        file.write(json.dumps(response.json(), indent=4).encode("utf-8"))
    
    url = f"https://pokeapi.co/api/v2/pokemon/{pokidex_entrie.lower() if isinstance(pokidex_entrie, str) else pokidex_entrie}"
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error: Pokemon not found. Status code: {response.status_code}")
        return False
    try:
        poke_info = response.json()
        with open(os.path.join("pokemon", "poke.json"), "wb") as file:
            file.write(json.dumps(poke_info, indent=4).encode('utf-8'))
        return True
    except requests.exceptions.JSONDecodeError:
        print(f"Error: Could not parse JSON response for {pokidex_entrie}")
        return False
    
def download_url(url):
    respons = requests.get(url)
    with open(os.path.join("pokemon", "url.json"), "wb") as file:
        file.write(json.dumps(respons.json(), indent=4).encode("utf-8"))

def get_poke_data(field, catagory="poke"):
    if catagory == "poke":
        with open(os.path.join("pokemon", "poke.json"), "r") as file:
            data = json.load(file)
            if field in data:
                return data[field]
            else:
                print(f"Field '{field}' not found in Pokemon data")
                return None
    if catagory == "species":
        with open(os.path.join("pokemon", "poke_species.json"),"r") as file:
            data = json.load(file)
            if field in data:
                return data[field]
            else:
                print(f"Field '{field}' not found in Pokemon species data")
                return None
    if catagory == "url":
        with open(os.path.join("pokemon", "url.json")) as file:
            data = json.load(file)
            if field in data:
                return data[field]
            else:
                print(f"Field '{field}' not found in url.json")

download_url(get_poke_data("evolution_chain", "species")["url"])
try:
    if get_poke_data("chain", "url")["species"]["name"] != None:
        print(get_poke_data("chain", "url")["species"]["name"])
        try:
            if get_poke_data("chain", "url")["evolves_to"][0]["species"]["name"] != None:
                print(get_poke_data("chain", "url")["evolves_to"][0]["species"]["name"])
                try:
                    if get_poke_data("chain", "url")["evolves_to"][0]["evolves_to"][0]["species"]["name"] != None:
                        print(get_poke_data("chain", "url")["evolves_to"][0]["evolves_to"][0]["species"]["name"])
                except IndexError:
                    print("No Third Evolution")
        except IndexError:
            print("No Second Evolution")
except IndexError:
    print("No First Evolution")


meme = True
mining_users = set()
auto_mining = set()
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
    print(f"Bots are in these servers: {[guild.name for guild in client.guilds]}")
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
    
    # ------------------------------
    # - Car command
    # ------------------------------
    if message.content.startswith("!car"):
        parts = message.content.split()
        if len(parts) > 1 and parts[1]:
            random_number = int(parts[1])
        else:
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
        # os.remove(local_filename)
    global meme
    if meme == True:
        if "money" in message.content.lower():
            await message.channel.send(file=discord.File(os.path.join("mems", "Mr. Krabs - Money.mp4")))
        if "10" in message.content.lower():
            await message.channel.send(file=discord.File(os.path.join("mems", "yakuza-nishikiyama.gif")))
        if "baby" in message.content.lower():
            await message.channel.send(file=discord.File(os.path.join("mems", "dust_baby.jpg")))
        if "591" in message.content:
            download_poke_data(591)
            embed = discord.Embed(title="pokemon")
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
            embed.add_field(name="Speed:", value=get_poke_data("stats")[5]["base_stat"])
            embed.set_thumbnail(url=get_poke_data("sprites")["front_default"])
            await message.channel.send(embed=embed)
            os.remove(os.path.join("pokemon", "poke.json"))
        if "kiwami" in message.content.lower():
            parts = message.content.split()
            # Default to sending the gif once
            send_count = 1
            
            # Check if any part is a number to determine how many times to send
            for part in parts:
                try:
                    count = int(part)
                    if 1 < count < 15:  # Limit to reasonable range
                        send_count = count
                        break
                except ValueError:
                    continue
            
            # Send the gif the specified number of times
            for _ in range(send_count):
                await message.channel.send("https://tenor.com/view/vengeance-has-consumed-you-black-panther-vengeance-black-panther-vengeance-kiwami-gif-6881560972906644645")
                # Add a small delay to prevent rate limiting
                if send_count > 1:
                    pass
    # ------------------------------
    # - Pokemon command
    # ------------------------------
    if message.content.startswith("!poke"):
        parts = message.content.split()
        if len(parts) > 1:
            try:
                if isinstance(int(parts[1]), int):
                    if int(parts[1]) <= 1025:
                        success = download_poke_data(parts[1])
                    else:
                        success = download_poke_data(random.randint(1,1025))
                        await message.channel.send(f"Pokemon number {parts[1]} is out of range. Showing a random Pokemon instead.")
                else:
                    success = download_poke_data(random.randint(1,1025))
            except ValueError:
                if len(parts[1]) > 1:
                    success = download_poke_data(parts[1])
                    if not success:
                        await message.channel.send(f"Error: Pokemon '{parts[1]}' not found.")
                        return
                else:
                    success = download_poke_data(random.randint(1,1025))
        else:
            # No Pokemon specified, show random
            success = download_poke_data(random.randint(1,1025))
        
        if not success:
            return
            
        embed = discord.Embed(title="Pokemon", color=discord.Colour.blue())
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
        download_url(get_poke_data("evolution_chain", "species")["url"])
        try:
            if get_poke_data("chain", "url")["evolves_to"][0]["evolves_to"][0]["species"]["name"] != None:
                embed.add_field(name="Chain Evolution:", value=f"**{str(get_poke_data("chain", "url")["species"]["name"]).capitalize()}** -> **{str(get_poke_data("chain", "url")["evolves_to"][0]["species"]["name"]).capitalize()}->{str(get_poke_data("chain", "url")["evolves_to"][0]["evolves_to"][0]["species"]["name"]).capitalize()}**")
            elif get_poke_data("chain", "url")["evolves_to"][0]["species"]["name"] != None:
                embed.add_field(name="Chain Evolution:", value=f"**{str(get_poke_data("chain", "url")["species"]["name"]).capitalize()}** -> **{str(get_poke_data("chain", "url")["evolves_to"][0]["species"]["name"]).capitalize()}**")
            elif get_poke_data("chain", "url")["species"]["name"] != None:
                embed.add_field(name="Chain Evolution:", value=f"**{str(get_poke_data("chain", "url")["species"]["name"])}**")
        except IndexError:
            pass
        for i in range(len(get_poke_data("flavor_text_entries","species"))):
            if get_poke_data("flavor_text_entries","species")[i]["language"]["name"] == "en":
                embed.add_field(name="Descrition:", value=str(get_poke_data("flavor_text_entries","species")[i]["flavor_text"]))
                break
        embed.set_thumbnail(url=get_poke_data("sprites")["front_default"])
        await message.channel.send(embed=embed)
        os.remove(os.path.join("pokemon", "poke.json"))
    if message.content == "!meme" and message.author.id == 394213071381463040 :
        if meme == False:
            await message.channel.send("Meme commands have been turned on")
            meme = True
        else:
            await message.channel.send("Meme commands have been turned Off")
            meme = False
    elif message.content == "!meme" and message.author.id != 394213071381463040:
        await message.author.send("Sorry, only the bot owner can use the command !meme")
    # ------------------------------
    # - BCG+ commands
    # ------------------------------
    
    if message.content.startswith("!bcg"):
        parts = message.content.split()
        if len(parts) > 1:
            print(parts[1])
            try:
                if isinstance(int(parts[1]), int):
                    print(f"input is an interger")
                    dex_search = f"{"0"*(4-len(parts[1]))}{parts[1]}"
                    if dex_search[0] != "#":
                        dex_search = "#" + dex_search
            except ValueError:
                print(f"input is not an integer")
                download_poke_data(parts[1])
                dex_search = get_poke_data("id")
                dex_search = f"{"0"*(4-len(str(dex_search)))}{dex_search}"
                if dex_search[0] != "#":
                    dex_search = "#" + dex_search
            print(dex_search)
        else:
            await message.channel.send("You need to specify a pokemon")
        
        found_pokemon = False
        with open(os.path.join("pokemon", "BCG+.csv"), "r") as file:
            for row in csv.DictReader(file):
                if dex_search[0] == "#":
                    pass
                else:
                    if row["Pokemon"] == dex_search:
                        dex_search = row["Dex"]
                if row["Dex"] == dex_search:
                    download_poke_data(parts[1])
                    found_pokemon = True
                    embed = discord.Embed(title="Bigchadguys+ Pokemon")
                    embed.add_field(name="Name", value=row["Pokemon"])
                    embed.add_field(name="Gen", value=row["Gen #"])
                    embed.add_field(name="Primary Type", value=row["Primary Type"])
                    if row["Light"] != "Any":
                        embed.add_field(name="Light", value=row["Light"])
                    if row["Time"] != "Any":
                        embed.add_field(name="Time", value=row["Time"])
                    if row["Weather"] != "Any":
                        embed.add_field(name="Weather", value=row["Weather"])
                    if row["Secondary Type"] != "-----":
                        embed.add_field(name="Secondary Type", value=row["Secondary Type"])
                    download_url(get_poke_data("evolution_chain", "species")["url"])
                    try:
                        if get_poke_data("chain", "url")["evolves_to"][0]["evolves_to"][0]["species"]["name"] != None:
                            embed.add_field(name="Chain Evolution:", value=f"**{str(get_poke_data("chain", "url")["species"]["name"]).capitalize()}** -> **{str(get_poke_data("chain", "url")["evolves_to"][0]["species"]["name"]).capitalize()}->{str(get_poke_data("chain", "url")["evolves_to"][0]["evolves_to"][0]["species"]["name"]).capitalize()}**")
                        elif get_poke_data("chain", "url")["evolves_to"][0]["species"]["name"] != None:
                            embed.add_field(name="Chain Evolution:", value=f"**{str(get_poke_data("chain", "url")["species"]["name"]).capitalize()}** -> **{str(get_poke_data("chain", "url")["evolves_to"][0]["species"]["name"]).capitalize()}**")
                        elif get_poke_data("chain", "url")["species"]["name"] != None:
                            embed.add_field(name="Chain Evolution:", value=f"**{str(get_poke_data("chain", "url")["species"]["name"])}**")
                    except IndexError:
                        pass
                    embed.add_field(name="Biomes", value=row["Biomes (Wiki)"])
                    if row["Anti-Biomes (Wiki)"] != "":
                        embed.add_field(name="Anti-Biomes", value=row["Anti-Biomes (Wiki)"])
                    embed.add_field(name="Rarity", value=row["Rarity"])
                    embed.add_field(name="Spawn Weight", value=row["Spawn Weight"])
                    embed.add_field(name="Spawn Level", value=row["Level"])
                    if row["Sky"] != "Any":
                        embed.add_field(name="Sky", value=row["Sky"])
                    embed.add_field(name="Context", value=row["Context"])
                    if row["Nearby Blocks"] != "":
                        embed.add_field(name="Nearby Blocks", value=row["Nearby Blocks"])
                    if row["Base Blocks"] != "":
                        embed.add_field(name="Base Blocks", value=row["Base Blocks"])
                    if row["Anti-Structures"] != "":
                        embed.add_field(name="Anti Structures", value=row["Anti-Structures"])
                    if row["Structures"] != "":
                        embed.add_field(name="Structures", value=row["Structures"])
                    embed.set_thumbnail(url=get_poke_data("sprites")["front_default"])
                    await message.channel.send(embed=embed)
            
            if not found_pokemon:
                if download_poke_data(parts[1]) != False:
                    get_poke_data("name")
                    if get_poke_data("name") != None:
                        await message.channel.send(f"Pokemon **{str(get_poke_data('name')).capitalize()}** not found in BCG+ database\nPokemon may not have been added yet or is not a naturaly spawning pokemon")
                    if get_poke_data("evolves_from_species", "species")["name"] != None:
                        await message.channel.send(f"Pokemon does have pre-evolution **{str(get_poke_data("evolves_from_species", "species")["name"]).capitalize()}**")
                        download_poke_data(get_poke_data("evolves_from_species", "species")["name"])
                        with open(os.path.join("pokemon", "BCG+.csv"), "r") as file:
                            dex_search = f"{"0"*(4-len(str(get_poke_data("id"))))}{get_poke_data("id")}"
                            if dex_search[0] != "#":
                                dex_search = "#" + dex_search
                            for row in csv.DictReader(file):
                                if row["Dex"] == dex_search:
                                    await message.channel.send(f"Pre-evolution **{str(get_poke_data("name")).capitalize()}** found in BCG+ database")
                                    break
    
    # ------------------------------
    # - User data system
    # ------------------------------
    with open("User_data.json", "r") as file:
        try:
            user_data = json.load(file)
        except json.JSONDecodeError:
            user_data = {}

    user_id = str(message.author.id)
    if user_id not in user_data:
        user_data[user_id] = {"username": message.author.name, "xp": 0, "level": 1, "coins": 100, "inventory": {}}
    # Ensure inventory key exists for all users
    if "inventory" not in user_data[user_id]:
        user_data[user_id]["inventory"] = {}

    user_data[user_id]["xp"] += 1
    # level up
    if user_data[user_id]["xp"] >= 4 * math.sqrt(user_data[user_id]["level"]):
        user_data[user_id]["xp"] = 0
        user_data[user_id]["level"] += 1

    with open("User_data.json", "w") as file:
        json.dump(user_data, file, indent=4)
    
    if message.content.startswith("!xp") and message.author.id == 394213071381463040:
        parts = message.content.split()
        user_id= message.author.id
        await message.channel.send(f"Xp set to {int(parts[1])}")
        with open("User_data.json", "r") as file:
            user_data = json.load(file)
            user_data[user_id]["xp"] = int(parts[1])
        with open("User_data.json", "w") as file:
            json.dump(user_data, file, indent=4)
    if message.content.startswith("!level"):
        parts = message.content.split()
        user_id= message.author.id
        await message.channel.send(f"Level set to {int(parts[1])}")
        print("ssss")
        with open("User_data.json", "r") as file:
            user_data = json.load(file)
            user_data[user_id]["level"] = int(parts[1])
        with open("User_data.json", "w") as file:
            json.dump(user_data, file, indent=4)
    # ------------------------------
    # - Slot machine command
    # ------------------------------
    if message.content.startswith("!slots"):
        parts = message.content.split()
        embed = discord.Embed(title="Slots 🎰")
        if len(parts) == 1:
            embed.add_field(name="Insturctions", value=f"Do !slots [number] to bet a that amount")
            embed.add_field(name="Coins:", value=f"{user_data[user_id]["coins"]}", inline=False)
        if len(parts) == 2:
            if int(parts[1]) > user_data[user_id]["coins"]:
                embed.add_field(name="", value=f"Your missing {int(parts[1])-int(user_data[user_id]["coins"])} coins")
            else:
                bet = parts[1]
                choices = ["⭐", "👽", "😈", "🤡", "🍒", "🍋", "💎", "7️⃣", "🎰", "🍀"]
                choice_1 = random.choice(choices)
                choice_2 = random.choice(choices)
                choice_3 = random.choice(choices)

                if choice_1 == choice_2 == choice_3:
                    embed.add_field(name="Result", value=f"{choice_1} | {choice_2} | {choice_3}")
                    embed.add_field(name="Coins:", value=f"{int(user_data[user_id]["coins"])+(int(bet)*10)}", inline=False)
                    embed.add_field(name="Jackpot", value=f":{int(bet)*10}")
                    user_data[user_id]["coins"] += int(bet)*10
                elif choice_1 == choice_2 or choice_2 == choice_3 or choice_3 == choice_1:
                    embed.add_field(name="Result", value=f"{choice_1} | {choice_2} | {choice_3}")
                    embed.add_field(name="Coins:", value=f"{int(user_data[user_id]["coins"])+(int(bet)*4)}", inline=False)
                    embed.add_field(name="Win", value=f":{int(bet)*4}")
                    user_data[user_id]["coins"] += int(bet)*4
                else:
                    embed.add_field(name="Result", value=f"{choice_1} | {choice_2} | {choice_3}")
                    embed.add_field(name="Coins:", value=f"{int(user_data[user_id]["coins"])-int(bet)}", inline=False)
                    user_data[user_id]["coins"] -= int(bet)
                    embed.add_field(name="Lost", value=int(bet))
                with open("User_data.json", "w") as file:
                    json.dump(user_data, file, indent=4)
        await message.channel.send(embed=embed)
    # ------------------------------
    # - mining system
    # ------------------------------
    resources = {
        "Stone": {"value": 5, "weight": 35},
        "Coal": {"value": 10, "weight": 25},
        "Iron": {"value": 25, "weight": 15},
        "Copper": {"value": 30, "weight": 10},
        "Gold": {"value": 50, "weight": 5},
        "Silver": {"value": 40, "weight": 5},
        "Emerald": {"value": 75, "weight": 2},
        "Ruby": {"value": 80, "weight": 1},
        "Sapphire": {"value": 85, "weight": 1},
        "Diamond": {"value": 100, "weight": 0.5},
        "Platinum": {"value": 120, "weight": 0.3},
        "Ancient Debris": {"value": 150, "weight": 0.2}
    }
    if message.channel.name == "the-mine" and message.content == "!mine" and not message.author.id in auto_mining:
    
        if "inventory" not in user_data[user_id]:
            user_data[user_id]["inventory"] = {}
            with open("User_data.json", "w") as file:
                    json.dump(user_data, file, indent=4)
        if message.author.id not in mining_users:
            mining_users.add(message.author.id)
            for i in range(random.randint(3,10)):
                embed = discord.Embed(title="Miner")
                embed.add_field(name="", value=f"Progress: .")
                if i == 0:
                    sent_message = await message.channel.send(embed=embed)
                else:
                    sent_message = await sent_message.edit(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(title="Miner")
                embed.add_field(name="", value=f"Progress: ..")
                sent_message = await sent_message.edit(embed=embed)
                await asyncio.sleep(1)
                embed = discord.Embed(title="Miner")
                embed.add_field(name="", value=f"Progress: ...")
                sent_message = await sent_message.edit(embed=embed)
                await asyncio.sleep(1)
            # Pick a random resource based on its weight
            resource_names = list(resources.keys())
            resource_weights = [resources[name]["weight"] for name in resource_names]
            found = random.choices(resource_names, weights=resource_weights, k=1)[0]
            embed = discord.Embed(title="Miner")
            embed.add_field(name="Result!", value=f"You found a {found} Worth {resources[found]["value"]}$")
            sent_message = await sent_message.edit(embed=embed)
            if found in user_data[user_id]["inventory"]:
                user_data[user_id]["inventory"][found] += 1
            else:
                user_data[user_id]["inventory"][found] = 1
            with open("User_data.json", "w") as file:
                    json.dump(user_data, file, indent=4)
            mining_users.remove(message.author.id)
        else:
            print(f"{message.author.name} is already mining")
    elif message.author.id in auto_mining and message.content == "!mine":
        await message.channel.send("You are currently automining, please disable automining before entering the mine")
    if message.channel.name == "the-mine" and message.content == "!inventory": 
        embed = discord.Embed(title="Inventory")
        if not user_data[user_id]["inventory"]:
            embed.add_field(name="Empty", value="Your inventory is empty.")
        else:
            for resource, count in user_data[user_id]["inventory"].items():
                embed.add_field(name=resource, value=str(count))
        # Calculate total worth of inventory items
        total_worth = sum(resources[resource]["value"] * count for resource, count in user_data[user_id]["inventory"].items())
        embed.add_field(name="Total Worth", value=f"{total_worth} coins")
        await message.channel.send(embed=embed)
    if message.channel.name == "the-mine" and message.content == "!sell": 
        embed = discord.Embed(title="Sell Resources")
        
        if not user_data[user_id]["inventory"]:
            embed.add_field(name="No Items", value="Your inventory is empty. Nothing to sell.")
        else:
            # Calculate total value of all items
            total_value = 0
            items_sold = []
            
            for resource, count in user_data[user_id]["inventory"].items():
                value = resources[resource]["value"] * count
                total_value += value
                items_sold.append(f"{count} {resource} for {value} coins")
            
            # Add value to user's coins
            user_data[user_id]["coins"] += total_value
            
            # Create the embed with sold items info
            embed.add_field(name="Items Sold", value="\n".join(items_sold), inline=False)
            embed.add_field(name="Total Earnings", value=f"{total_value} coins", inline=False)
            embed.add_field(name="New Balance", value=f"{user_data[user_id]['coins']} coins", inline=False)
            
            # Clear inventory
            user_data[user_id]["inventory"] = {}
            
            # Save updated user data
            with open("User_data.json", "w") as file:
                json.dump(user_data, file, indent=4)
        
        await message.channel.send(embed=embed)
    if message.channel.name == "the-mine" and message.content == "!automine":
        if message.author.id not in auto_mining:
            print(f"{message.author.id} added to Automining")
            auto_mining.add(message.author.id)
            embed = discord.Embed(title="Automining")
            embed.add_field(name="Mode", value="On")
            await message.channel.send(embed=embed)

            async def auto_mine_task(user_id):
                while user_id in auto_mining:
                    if user_id not in mining_users:
                        mining_users.add(user_id)
                        await asyncio.sleep(random.randint(1, 2))
                        resource_names = list(resources.keys())
                        resource_weights = [resources[name]["weight"] for name in resource_names]
                        found = random.choices(resource_names, weights=resource_weights, k=1)[0]
                        # Update user's inventory
                        print(f"{message.author.id} found {found}")
                        if found in user_data[str(user_id)]["inventory"]:
                            user_data[str(user_id)]["inventory"][found] += 1
                        else:
                            user_data[str(user_id)]["inventory"][found] = 1
                        with open("User_data.json", "w") as file:
                            json.dump(user_data, file, indent=4)
                        mining_users.remove(user_id)
            asyncio.create_task(auto_mine_task(message.author.id))
    # ------------------------------
    # - User info command
    # ------------------------------
    if message.content.startswith("!user"):
        parts = message.content.split()
        if len(parts) > 1:
            user_id = int(parts[1].strip("<@!>"))
            user = await client.fetch_user(user_id)
        else:
            user = message.author
        embed = discord.Embed(title="User Info", color=discord.Color.blue())
        embed.add_field(name="Username", value=user.name, inline=False)
        if user.discriminator == 0:
            embed.add_field(name="Discriminator", value=f"#{user.discriminator}", inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        with open("User_data.json", "r") as file:
            user_data = json.load(file)
            embed.add_field(name="Level", value=user_data[str(user_id)]["level"])
        embed.add_field(name="Coins", value=f"{(user_data[str(user_id)]["coins"])}", inline=False)
        embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
        await message.channel.send(embed=embed)
       

if __name__ == "__main__":
    print("Starting bot...")
    client.run(TOKEN)