import discord as dc
import d_open_close_stuff as ocs


def create_item_embed(item_base_name_and_stats, title):

    rarities = {
        "common": [0x777777, "A common dinosaur!", ":white_circle:"],
        "uncommon": [0x359b15, "An uncommon dinosaur!", ":green_circle:"],
        "rare": [0x1e72e6, "A rare dinosaur!", ":blue_circle:"],
        "epic": [0x8227da, "An epic dinosaur!", ":purple_circle:"],
        "legendary": [0xc0b838, "A legendary dinosaur!", ":star:"],
        "specialrank": [0xa13316, "A very special dinosaur!", ":secret:"]
    }

    items = ocs.open_items()

    item_features = items[item_base_name_and_stats[0]]
    item_name = item_base_name_and_stats[0] + f" {rarities[item_features[0]][2]}"

    attack_defense = [item_base_name_and_stats[1][0], item_base_name_and_stats[1][1]]
    stat_desc = f"{attack_defense[0]} ⚔  {attack_defense[1]} 💟"

    stat_max = ""
    if attack_defense == [item_features[3][0][1], item_features[3][1][1]]:
        stat_max = " (maxed)"

    embed = dc.Embed(title=title, colour=dc.Colour(rarities[item_features[0]][0]),
                     description=rarities[item_features[0]][1])
    embed.set_image(url=item_features[1])
    embed.add_field(name=item_name, value=item_features[2])
    embed.add_field(name=f"Statistics{stat_max}", value=stat_desc)

    return [embed, item_name]
