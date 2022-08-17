import json
import yaml
import setup


def open_inv(ctx):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/inv.txt", mode="r", encoding="utf-8") as inventory_load:
        inventories = json.load(inventory_load)
        return inventories


def open_bas(ctx):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/bazaar.txt", mode="r", encoding="utf-8") as bas_load:
        the_bazaar = json.load(bas_load)
        return the_bazaar


def open_crowns(ctx):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/kk.txt", mode="r", encoding="utf-8") as users_crowns_load:
        users_crowns = json.load(users_crowns_load)
        return users_crowns


def open_time(ctx):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/dailytime.txt", encoding="utf-8") as daily_time_load:
        daily_time = json.load(daily_time_load)
        return daily_time


def open_streak(ctx):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/streak.txt", mode="r") as streak_load:
        streak = json.load(streak_load)
        return streak


def open_shop(ctx):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/shop.json", mode="r") as shop_load:
        shop_data = json.load(shop_load)
        return shop_data


def open_items():
    with open(f"{setup.py_file_folder_name}/dinosaurs.yaml", mode="r", encoding="utf-8") as item_file:
        items = yaml.safe_load(item_file)
        return items


def close_inv(ctx, inventory):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/inv.txt", mode="w", encoding="utf-8") as inventory_load:
        json.dump(inventory, inventory_load)


def close_crowns(ctx, users_crowns):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/kk.txt", mode="w", encoding="utf-8") as users_crowns_load:
        json.dump(users_crowns, users_crowns_load)


def close_bazaar(ctx, the_bazaar):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/bazaar.txt", mode="w", encoding="utf-8") as bas_load:
        json.dump(the_bazaar, bas_load)


def close_time(ctx, daily_time):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/dailytime.txt", "w") as daily_time_load:
        json.dump(daily_time, daily_time_load)


def close_streak(ctx, streak):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/streak.txt", mode="w") as streak_load:
        json.dump(streak, streak_load)


def close_shop(ctx, shop_data):
    with open(f"{setup.data_file_folder_name}/{ctx.channel.guild.id}/shop.json", mode="w") as shop_load:
        json.dump(shop_data, shop_load)
