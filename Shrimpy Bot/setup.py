from discord_slash import SlashCommand
from discord.ext import commands

client = commands.Bot(command_prefix="ratio")
slash = SlashCommand(client=client, sync_commands=True)
guild_ids = ["insert list of int server-ids here"]

# Test Server
token = "insert token"
kk = "insert custom coin emoji (You can just use :coin:)"
bot_id = "<@insert id of your bot>"
bot_owner = "<@insert id of the admin>"
py_file_folder_name = "Shrimpy Bot"
data_file_folder_name = "Data"
