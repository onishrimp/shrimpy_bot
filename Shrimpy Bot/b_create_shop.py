import datetime
import random
import b_generate_random_items as gri
import json
import a_setup
import d_open_close_stuff as ocs
import b_create_item_embeds as cde


def cs(ctx):

    with open(f"{a_setup.data_file_folder_name}/{ctx.channel.guild.id}/shop.json", mode="r") as shop_load:
        shop_data = json.load(shop_load)

    items = ocs.open_items()
    today = str(datetime.date.today())

    # will the shop be reset today?
    if today not in shop_data:
        shop_data = {
            today: []
        }

        new_daily_shop_items = gri.gri([90, 50, 38, 18, 4], 3, 0)  # change the second argument to modify the amount

        for item in new_daily_shop_items:
            costs = {
                "common": random.choice([160, 180, 200, 220, 260]),
                "uncommon": random.choice([250, 270, 300, 320, 370]),
                "rare": random.choice([360, 370, 390, 400, 410]),
                "epic": random.choice([1000, 1050, 1100, 1150, 1200]),
                "legendary": random.choice([5500, 6000, 6300, 6500, 7000])
            }

            price = costs[items[item][0]]
            shop_data[today].append([item, price, "fresh"])

        ocs.close_shop(ctx, shop_data)

    # now just send a message with the shop
    item_number = 1
    item_showcase = ""
    for d in shop_data[today]:
        if d[2] == "sold":
            item_showcase += f"~~{item_number} - {d[0]} - {d[1]}~~ sold out!\n"
        else:
            full_item_name = cde.create_item_embed(d[0], "empty")[1]
            item_showcase += f"**{item_number}** - {full_item_name} - {d[1]} {a_setup.kk}\n"
        item_number += 1

    description = f"**Items**\n" \
                  f"{item_showcase}\n" \
                  f"**Badges**\n" \
                  f"*coming soon*"

    return description
