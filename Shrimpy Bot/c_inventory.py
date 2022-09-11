import a_setup
import b_create_item_embeds as cde
import discord as dc
import d_open_close_stuff as ocs
import b_community_server_active as csa


@a_setup.slash.slash(description="Take a look at one of your items", guild_ids=a_setup.guild_ids)
async def view_inventory_item(ctx, item_number):

    print(f"{ctx.author.name} used the item command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")
    printed_author = csa.get_printed_author_name(ctx.author)

    inventories = ocs.open_inv(ctx)

    try:
        chosen_item = inventories[message_author][int(item_number) - 1]  # str name des items

    except IndexError:
        await ctx.message.edit(content=f"Invalid item-number **{printed_author}**!")
        return

    embed_and_item_name = cde.create_item_embed(chosen_item, f"Property of {printed_author}")
    await ctx.message.edit(content=None, embed=embed_and_item_name[0])


@a_setup.slash.slash(description="Take a look at your inventory", guild_ids=a_setup.guild_ids)
async def inventory(ctx, starting_page):

    print(f"{ctx.author.name} used the inventory command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")
    printed_author = csa.get_printed_author_name(ctx.author)
    inventories = ocs.open_inv(ctx)

    description = ""

    try:
        page = int(starting_page)
    except ValueError:
        ctx.message.edit(f"Invalid starting page, {printed_author}")
        return

    if page < 1:
        page = 1

    if message_author not in inventories:
        description = "You have never possessed any items!"

    elif not inventories[message_author]:
        description = "Your inventory is empty!"

    else:

        item_range = 25 * (page - 1)
        inventory_index = item_range + 1

        for d in range(item_range, item_range + 25):
            try:
                description += f"**{inventory_index}** - " \
                               f"{cde.create_item_embed(inventories[message_author][d], None)[1]}\n"
            except IndexError:
                break
            inventory_index += 1

        if description == "":
            description = "Theres nothing on this page!"

    embed = dc.Embed(title=f"**Inventory of {printed_author}**", colour=dc.Colour(0x485885), description=description)
    embed.set_footer(text=f"Page {page}")

    await ctx.message.edit(content=None, embed=embed)
    await ctx.message.add_reaction("◀️")
    await ctx.message.add_reaction("▶️")
    await ctx.message.add_reaction("🔄")
