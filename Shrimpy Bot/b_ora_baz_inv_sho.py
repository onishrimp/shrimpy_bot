import d_open_close_stuff as ocs
import b_create_item_embeds as cie
import a_setup
import datetime
import b_create_shop as cs
import discord as dc


async def create_and_send_embed(embed_title, description, footer, interaction, ma, self):
    ocs.check_user(ma)
    embed = dc.Embed(title=embed_title, colour=dc.Colour(ocs.data[ma]["color"]), description=description)
    embed.set_footer(text=footer)
    await interaction.edit_original_response(embed=embed, view=self)


def get_page_stuff(emoji, embed_list):
    page_int = 1
    if emoji == "◀️":
        page_int = -1
    elif emoji == "🔄":
        page_int = 0
    page = int(embed_list[0].footer.text.split(" ", maxsplit=1)[1]) + page_int
    if page <= 0:
        page = 1
    item_range = 25 * (page - 1)

    return page, item_range


def disable_certain_children(n, children, max_len, left_bool):
    for b in children:
        if b.custom_id == "a_left":
            if left_bool and (n - 2) == 0:
                b.disabled = True
            else:
                b.disabled = False
        if b.custom_id == "a_right":
            if not left_bool and (n + 1) == max_len:
                b.disabled = True
            else:
                b.disabled = False


def inventory_requested(item_range, ma, page, interaction):
    if not ocs.data[ma]["inv"]:
        description = "Your inventory is empty!"
    else:
        description = []
        for d in range(item_range, item_range + 25):
            try:
                description.append(f"**{d + 1}** - {cie.create_item_embed(ocs.data[ma]['inv'][d], None)[1]}\n")
            except IndexError:
                break
        description = "".join(description)
    if description == "":
        description = "Theres nothing on this page!"

    embed_title = f"**Inventory of {interaction.user.name}**"
    footer = f"Page {page}"

    return description, embed_title, footer


def bazaar_requested(item_range, page):
    if not ocs.data["bazaar"]:
        description = "The bazaar is empty!"
    else:
        description = []
        for d in range(item_range, item_range + 25):
            try:
                tb = ocs.data["bazaar"][d]
                description.append(f"**{d + 1}** - {cie.create_item_embed(tb[0], None)[1]} - "
                               f"{tb[1]} {a_setup.kk} - von {tb[2]}\n")
            except IndexError:
                break
        description = "".join(description)

    if description == "":
        description = "Theres nothing on this page!"
    embed_title = "**The current bazaar**"
    footer = f"Page {page}"

    return description, embed_title, footer


def shop_requested():
    today = str(datetime.date.today())
    description = cs.cs()
    embed_title = "**The current shop**"
    footer = f"Shop - {today}"

    return description, embed_title, footer
