from discord_slash import SlashCommand
from discord.ext import commands

client = commands.Bot(command_prefix="ratio")
slash = SlashCommand(client=client, sync_commands=True)
guild_ids = ["insert list of int server-ids here"]

token = "insert token"
kk = "insert custom coin emoji (You can just use :coin:)"
bot_id = "<@insert id of your bot>"
bot_owners = ["<@insert id of the admin>", "<@insert id of another admin>"]
py_file_folder_name = "Shrimpy Bot"
data_file_folder_name = "Data"

'''
#-COMMUNITY SERVER MODE OPTIONS-#
The following options should all be turned on if this bot is running on a server with many members.
If the bot is only meant to be used by a small amount of people, it is probably more convenient 
to leave all of those options turned off.
            I
            I
            V
'''
name_mentions_active = False  # implemented
give_box_active = False  # not implemented yet
bazaar_confirmation_active = False  # not implemented yet
