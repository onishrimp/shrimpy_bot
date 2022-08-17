import discord as dc
import open_close_stuff as ocs


def create_item_embed(item_base_name, title):

    rarities = {
        "common": [0x777777, "A common dinosaur!", ":white_circle:"],
        "uncommon": [0x359b15, "A uncommon dinosaur!", ":green_circle:"],
        "rare": [0x1e72e6, "A rare dinosaur!", ":blue_circle:"],
        "epic": [0x8227da, "An epic dinosaur!", ":purple_circle:"],
        "legendary": [0xc0b838, "A legendary dinosaur!", ":star:"],
        "specialrank": [0xa13316, "A very special dinosaur!", ":secret:"]
    }

    items = ocs.open_items()

    item_features = items[item_base_name]
    item_name = item_base_name + f" {rarities[item_features[0]][2]}"

    embed = dc.Embed(title=title, colour=dc.Colour(rarities[item_features[0]][0]),
                     description=rarities[item_features[0]][1])
    embed.set_image(url=item_features[1])
    embed.add_field(name=item_name, value=item_features[2])

    return [embed, item_name]
