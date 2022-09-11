import b_create_item_embeds as cde
import a_setup
import discord as dc
import datetime
import b_create_shop as cs
import d_open_close_stuff as ocs
import b_community_server_active as csa


@a_setup.client.event
async def on_reaction_add(reaction, user):

    message_author = user.mention.replace("!", "")
    printed_author = csa.get_printed_author_name(user)

    if message_author == a_setup.bot_id:
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
    if embed_list[0].title == f"**Inventory of {printed_author}**":
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

        inventory_index = item_range + 1
        title = f"Property of {printed_author}"
        inventories = ocs.open_inv(reaction.message)

        if message_author not in inventories:
            description = "You haven't possessed anything yet!"

        elif not inventories[message_author]:
            description = "Your inventory is empty!"

        else:
            for d in range(item_range, item_range + 25):
                try:
                    description += f"**{inventory_index}** - " \
                                   f"{cde.create_item_embed(inventories[message_author][d], title)[1]}\n"
                except IndexError:
                    break
                inventory_index += 1

        if description == "":
            description = "Theres nothing on this page!"

        embed_title = f"**Inventory of {printed_author}**"
        footer = f"Page {page}"

    elif bazaar_requested:
        bazaar_index = item_range + 1
        the_bazaar = ocs.open_bas(reaction.message)

        if not the_bazaar["bazaar"]:
            description = "The bazaar is empty!"

        else:
            for d in range(item_range, item_range + 25):
                try:
                    tb = the_bazaar["bazaar"][d]
                    description += f"**{bazaar_index}** - {cde.create_item_embed(tb[0], None)[1]} - " \
                                   f"{tb[1]} {a_setup.kk} - von {tb[2]}\n"
                except IndexError:
                    break
                bazaar_index += 1

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
