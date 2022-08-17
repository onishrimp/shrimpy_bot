import a_setup
import d_on_reaction_add
import c_general
import c_gamble
import c_info
import c_crowns
import c_inventory
import c_bazaar_1
import c_bazaar_2
import c_bank
import c_give
import c_shop


@a_setup.client.event
async def on_ready():
    print("The bot is online")


a_setup.client.run(a_setup.token)
