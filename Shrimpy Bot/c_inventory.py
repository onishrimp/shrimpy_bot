import a_setup
import b_create_item_embeds as cde
import discord as dc
import d_open_close_stuff as ocs


@a_setup.slash.slash(description="Take a look at one of your items", guild_ids=a_setup.guild_ids)
async def item_inventory(ctx, item_number):

    print(f"{ctx.author.name} used the item command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")

    inventories = ocs.open_inv(ctx)

    try:
        chosen_item = inventories[message_author][int(item_number) - 1]  # str name des items

    except IndexError:
        await ctx.message.edit(content=f"Invalid item-number **{ctx.author.name}**!")
        return

    embed_and_item_name = cde.create_item_embed(chosen_item, f"Property of {ctx.author.name}")
    await ctx.message.edit(content=None, embed=embed_and_item_name[0])


@a_setup.slash.slash(description="Take a look at your inventory", guild_ids=a_setup.guild_ids)
async def inventory(ctx, starting_page):

    print(f"{ctx.author.name} used the inventory command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")
    inventories = ocs.open_inv(ctx)

    description = ""

    try:
        page = int(starting_page)
    except ValueError:
        ctx.message.edit(f"Invalid starting page, {ctx.author.name}")
        return

    if page < 1:
        page = 1

    if message_author not in inventories:
        description = "You have never possessed any items!"

    elif not inventories[message_author]:
        description = "Your inventory is empty!"

    else:

        item_range = 25 * (page - 1)
        user_items = []
        title = f"Property of {ctx.author.name}"
        inventory_index = 1

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

    embed = dc.Embed(title=f"**Inventory of {ctx.author.name}**", colour=dc.Colour(0x485885), description=description)
    embed.set_footer(text=f"Page {page}")

    await ctx.message.edit(content=None, embed=embed)
    await ctx.message.add_reaction("◀️")
    await ctx.message.add_reaction("▶️")
    await ctx.message.add_reaction("🔄")
