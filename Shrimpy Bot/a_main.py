import asyncio
import atexit
import datetime
import a_setup
import c_general
import c_gamble
import c_info
import c_crowns
import c_inventory
import c_bazaar_1
import c_bank
import c_give
import c_shop
import c_fight_1
import d_open_close_stuff as ocs


@a_setup.client.event
async def on_ready():
    print("The bot is online")
    while True:
        # auto save
        await asyncio.sleep(3600)  # 3600
        ocs.save_data()

        # weekly ranked rewards
        if datetime.date.weekday(datetime.datetime.now(datetime.timezone.utc)) == 6 and \
                not ocs.data["last_dis"] == str(datetime.date.today()):
            gtp = c_fight_1.get_top_players()
            for t in gtp[1]:
                ocs.data[t[0]]["kk"] += t[1]

            for k, _ in ocs.data.items():
                if not k in ["bazaar", "shop", "last_dis"]:
                    ocs.data[k]["rank"] = 0

            ocs.data["last_dis"] = str(datetime.date.today())
            channel = a_setup.client.get_channel(a_setup.command_channel_id)
            await channel.send(f"The **weekly ranked rewards** have been **distributed!**\n\n"
                               f"**Top Players:**\n"
                               f"{gtp[0]}")

@atexit.register
def save():
    ocs.save_data()


a_setup.client.run(a_setup.token)
