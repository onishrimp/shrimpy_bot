import create_item_embeds as cde
import setup
import discord as dc
import datetime
import create_shop as cs
import open_close_stuff as ocs


@setup.client.event
async def on_reaction_add(reaction, user):

    message_author = user.mention.replace("!", "")

    if message_author == setup.bot_id:
        return

    if not (reaction.emoji == "▶️") and not (reaction.emoji == "◀️") and not (reaction.emoji == "🔄"):
        return

    embed_list = reaction.message.embeds

    if not embed_list:
        return

    inventory_requested = False
    bazaar_requested = False
    shop_requested = False

    # reaction to what?
    if embed_list[0].title == f"**Inventory of {user.name}**":
        inventory_requested = True
    elif embed_list[0].title == "**The current bazaar**":
        bazaar_requested = True
    elif embed_list[0].title == "**The current shop**":
        shop_requested = True
    else:
        return

    if inventory_requested or bazaar_requested:

        page_int = 1
        if reaction.emoji == "◀️":
            page_int = -1
        elif reaction.emoji == "🔄":
            page_int = 0
        page = int(embed_list[0].footer.text.split(" ", maxsplit=1)[1]) + page_int
        if page <= 0:
            page = 1

        item_range = 25 * (page - 1)

    description = ""

    if inventory_requested:

        inventory_index = 1
        user_items = []
        title = f"Property of {user.name}"
        inventories = ocs.open_inv(reaction.message)

        if message_author not in inventories:
            description = "You haven't possessed anything yet!"

        elif not inventories[message_author]:
            description = "Your inventory is empty!"

        else:
            for d in inventories[message_author]:
                user_items.append(f"**{inventory_index}** - {cde.create_item_embed(d, title)[1]}\n")
                inventory_index += 1

            for d in range(0, 25):
                try:
                    d += item_range
                    description += user_items[d]
                except IndexError:
                    break

        if description == "":
            description = "Theres nothing on this page!"

        embed_title = f"**Inventory of {user.name}**"
        footer = f"Page {page}"

    elif bazaar_requested:
        bazaar_index = 1
        bazaar_items = []

        the_bazaar = ocs.open_bas(reaction.message)

        if not the_bazaar["bazaar"]:
            description = "The bazaar is empty!"

        else:
            for d in the_bazaar["bazaar"]:
                d_name = cde.create_item_embed(d[0], "The current bazaar")[1]
                bazaar_items.append(f"**{bazaar_index}** - {d_name} - {d[1]} {setup.kk} - von {d[2]}\n")
                bazaar_index += 1

        for d in range(1, 26):
            try:
                d += item_range
                description += bazaar_items[d - 1]
            except IndexError:
                break

        if description == "":
            description = "Theres nothing on this page!"

        embed_title = "**The current bazaar**"
        footer = f"Page {page}"

    elif shop_requested:

        today = str(datetime.date.today())

        description = cs.cs(reaction.message)
        embed_title = "**The current shop**"
        footer = f"Shop - {today}"

    embed = dc.Embed(title=embed_title, colour=dc.Colour(0x485885), description=description)
    embed.set_footer(text=footer)

    await reaction.remove(user)
    await reaction.message.edit(embed=embed)
