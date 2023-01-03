import datetime
import random
import b_generate_random_items as gri
import a_setup
import d_open_close_stuff as ocs
import b_create_item_embeds as cde


def cs():
    items = ocs.open_items()
    today = str(datetime.date.today())

    # will the shop be reset today?
    if today not in ocs.data["shop"]:
        shop_data = {
            today: []
        }

        item_amount = 3  # change this to modify the amount of items the shop has :]
        if datetime.date.weekday(datetime.datetime.now(datetime.timezone.utc)) == 4:
            item_amount = 5  # 5 items on fridays

        new_daily_shop_items = gri.gri([90, 54, 38, 18, 0], item_amount, 0)

        for item in new_daily_shop_items:
            costs = {
                "common": random.choice([160, 180, 200, 220, 260]),
                "uncommon": random.choice([250, 270, 300, 320, 370]),
                "rare": random.choice([360, 370, 390, 400, 410]),
                "epic": random.choice([2450, 2500, 2510, 2570, 2700]),
                "legendary": random.choice([8000, 8500, 9000, 9500, 9800])
            }

            price = costs[items[item[0]][0]]
            shop_data[today].append([item, price, "fresh"])

        ocs.data["shop"] = shop_data

    # now just send a message with the shop
    item_number = 1
    item_showcase = ""
    for d in ocs.data["shop"][today]:
        if d[2] == "sold":
            item_showcase += f"~~{item_number} - {d[0][0]} - {d[1]}~~ sold out!\n"
        else:
            full_item_name = cde.create_item_embed(d[0], "empty")[1]
            item_showcase += f"**{item_number}** - {full_item_name} - {d[1]} {a_setup.kk}\n"
        item_number += 1

    description = f"**Items**\n" \
                  f"{item_showcase}\n" \
                  f"**Badges**\n" \
                  f"*coming soon*"

    return description
