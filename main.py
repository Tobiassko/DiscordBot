import discord
import os
from dotenv import load_dotenv
import random
import requests  # Add this import for downloading files

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
    """All the commands"""
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
    if "money" in message.content.lower():
        await message.channel.send(file=discord.File(os.path.join("mems\Mr. Krabs - Money.mp4")))
    if "10" in message.content.lower():
        await message.channel.send("https://www.youtube.com/watch?v=brZyXHO1N6Q")
    if "baby" in message.content.lower():
        await message.channel.send(file=discord.File(os.path.join("mems", "dust_baby.jpg")))

    

if __name__ == "__main__":
    print("Starting bot...")
    client.run(TOKEN)