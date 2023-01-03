from discord_slash import SlashCommand
from discord.ext import commands

client = commands.Bot(command_prefix="ratio")
slash = SlashCommand(client=client, sync_commands=True)
guild_ids = [888711097119559680]

token = "OTMyOTgzODAyODA3MDc4OTgy.Yea64A.yts6C-xeQLQolh1jyyI1D5-IVmw"
welcome_channel_name = "welcome"
