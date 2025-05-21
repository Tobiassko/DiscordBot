# DiscordBot

## Overview
DiscordBot is a custom bot designed to enhance your Discord server experience. It includes a variety of features such as a slot machine game, user data tracking, meme commands, and Pokémon information retrieval.

## Features
- **Economy System**: Users can earn coins through various activities and commands. The bot tracks user XP and levels, allowing for a competitive environment.
- **Slot Machine**: Play a fun slot machine game with the `!slots` command. Earn coins and win rewards based on the results.
- **User Data Tracking**: Tracks user XP, levels, and coins. Automatically updates user data in `User_data.json`.
- **Meme Commands**: Responds to specific keywords with memes, images, or videos.
- **Pokémon Commands**: Fetch Pokémon data using the `!poke` command, including stats, abilities, and evolution chains.
- **Car Videos**: Retrieve random car videos with the `!car` command.

## Commands
- `!help`: Displays a list of available commands.
- `!test`: Checks if the bot is operational.
- `!slots`: Play the slot machine game.
- `!poke <id/name>`: Fetch Pokémon data by ID or name.
- `!car`: Retrieve a random car video.
- `!user`: Fetch user information.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd DiscordBot
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your Discord bot token:
   ```env
   DISCORD_TOKEN=your-bot-token
   ```
5. Run the bot:
   ```bash
   python main.py
   ```

## File Structure
- `main.py`: Main bot logic.
- `User_data.json`: Stores user data such as XP, levels, and coins.
- `Car/`: Contains car video files.
- `mems/`: Contains meme images and videos.
- `pokemon/`: Contains Pokémon-related data files.

## Requirements
- Python 3.8 or higher
- Discord.py
- Requests

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Feel free to submit issues or pull requests to improve the bot.
