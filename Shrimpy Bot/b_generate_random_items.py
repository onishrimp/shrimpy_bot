import d_open_close_stuff as ocs
import random


def gri(prob_list, absolute_amount, prob_crowns):

    items = ocs.open_items()

    common = []
    uncommon = []
    rare = []
    epic = []
    legendary = []

    for k, v in items.items():
        if v[0] == "common":
            common.append(k)
        if v[0] == "uncommon":
            uncommon.append(k)
        if v[0] == "rare":
            rare.append(k)
        if v[0] == "epic":
            epic.append(k)
        if v[0] == "legendary":
            legendary.append(k)

    letter_translation_dict = {
        "A": "common",
        "B": "uncommon",
        "C": "rare",
        "D": "epic",
        "E": "KKs",
        "F": "legendary"
    }

    probabilities = ("A" * prob_list[0]) + ("B" * prob_list[1]) + ("C" * prob_list[2]) + ("D" * prob_list[3]) + \
                    ("E" * prob_crowns) + ("F" * prob_list[4])

    final_items = []

    for i in range(0, absolute_amount):
        chosen_letter = random.choice(probabilities)
        if chosen_letter == "E":
            chosen_item = 600
        else:
            chosen_rarity = letter_translation_dict[chosen_letter]
            chosen_item_raw = eval(chosen_rarity)  # transform to one of the lists above
            chosen_item = random.choice(chosen_item_raw)  # item name
        final_items.append(chosen_item)

    return final_items
