from discord.ext import commands


client = commands.Bot()
guild_id = int()
guild_ids = [guild_id]

token = "Your token"
kk = ":coin:"
bot_id = "<@id>"
bot_owners = ["<@id>"]
command_channel_id = int()
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
bazaar_ownership_active = False  # not implemented yet
