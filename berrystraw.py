"""
    BerryStraw by Arianne
    Self-bots are not allowed on Discord. Use this at your own risks.
"""
# Builtin dependencies
import os
import json
import sys
import signal

# Dependencies that need to be installed
from dotenv import load_dotenv
import discord
from discord.ext import commands
from colorama import Fore, Style

# Handle CTRL-C exit
def keyboard_interrupt_handler(signal, frame):
    print(f"{Fore.RED}{Style.BRIGHT}bye!{Style.RESET_ALL}")
    sys.exit(0)
signal.signal(signal.SIGINT, keyboard_interrupt_handler)

# Load .env configuration
load_dotenv()
TOKEN = os.getenv('USER_TOKEN')
PREFIX = os.getenv('PREFIX')
with open('info.json', 'r') as f:
    info_json = json.load(f)
    VERSION = info_json['version']

client = commands.Bot(command_prefix=PREFIX, self_bot=True, chunk_guilds_at_startup=False)

async def load_bot_extensions(): # Dynamically detects extensions and loads them
    print(f"{Fore.RED}Loading extensions...{Style.RESET_ALL}")

    for extension in [f for f in os.listdir('./extensions') if f.endswith('.py')]:
        try:
            extension = extension.replace('.py', '')
            await client.load_extension(f"extensions.{extension}")
            print(f"{Fore.RED}> Loaded {extension}{Style.RESET_ALL}")
        except (
            discord.ext.commands.ExtensionNotFound,
            discord.ext.commands.ExtensionAlreadyLoaded,
            discord.ext.commands.NoEntryPointError,
            discord.ext.commands.ExtensionFailed
        ) as e:
            print(f"{Fore.RED}Error loading {extension}: {e}{Style.RESET_ALL}")

@client.event
async def on_ready():
    print(f"\n{'='*75}\n")
    print(f"\n{Fore.RED}{Style.BRIGHT}Logged in as {client.user}{Style.RESET_ALL}")

    await load_bot_extensions()

    print(f"{Fore.RED}{Style.BRIGHT}Ready!{Style.RESET_ALL}")
    print(f"{Fore.RED}{Style.BRIGHT}Prefix: '{PREFIX}'{Style.RESET_ALL}")

if __name__ == "__main__":
    print(
        rf"""{Fore.RED}{Style.BRIGHT}
______ ___________________   _______ ___________  ___  _    _ 
| ___ \  ___| ___ \ ___ \ \ / /  ___|_   _| ___ \/ _ \| |  | |
| |_/ / |__ | |_/ / |_/ /\ V /\ `--.  | | | |_/ / /_\ \ |  | |
| ___ \  __||    /|    /  \ /  `--. \ | | |    /|  _  | |/\| |
| |_/ / |___| |\ \| |\ \  | | /\__/ / | | | |\ \| | | \  /\  /
\____/\____/\_| \_\_| \_| \_/ \____/  \_/ \_| \_\_| |_/\/  \/  v{VERSION}{Style.RESET_ALL}"""
    )
    print(f"\n{'='*75}\n")
    try:
        client.run(TOKEN)
    except (discord.errors.LoginFailure, discord.errors.ConnectionClosed) as e:
        print(f"\n{e}\nExiting.")
        sys.exit(1)
