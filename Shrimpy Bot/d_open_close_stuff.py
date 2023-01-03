import json
import yaml
import a_setup


def open_items():
    with open(f"{a_setup.py_file_folder_name}/a_items.yaml", mode="r", encoding="utf-8") as item_file:
        items = yaml.safe_load(item_file)
        return items


with open(f"{a_setup.data_file_folder_name}/{a_setup.guild_id}/data.json", mode="r") as data_raw:
    data = json.load(data_raw)


def save_data():
    with open(f"{a_setup.data_file_folder_name}/{a_setup.guild_id}/data.json", mode="w") as data_raww:
        json.dump(data, data_raww)


def check_user(user_mention):  # is <@1234567890> already in data?
    if user_mention not in data:
        data[user_mention] = {"kk": 300, "daily_matches": "0-0-0", "daily_kk": "0-0-0", "streak": 0,
                              "inv": [], "rank": 0, "color": 4741253}
