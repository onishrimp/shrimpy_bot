import a_setup
import b_create_item_embeds as cde
import d_open_close_stuff as ocs


@a_setup.slash.slash(description="Sell a item to the bazaar", guild_ids=a_setup.guild_ids)
async def sell_bazaar(ctx, price, item_number):

    print(f"{ctx.author.name} used the sell_bazaar command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")

    try:
        price = int(price)
    except ValueError:
        await ctx.message.edit(content=f"Invalid price, **{ctx.author.name}**!")
        return

    if price < 0:
        price = 250
    elif price > 10000:
        price = 10000

    the_bazaar = ocs.open_bas(ctx)
    inventories = ocs.open_inv(ctx)

    try:
        chosen_item = inventories[message_author][int(item_number) - 1]
    except IndexError:
        await ctx.message.edit(content=f"Invalid item-number, **{ctx.author.name}**!")
        return

    the_bazaar["bazaar"].append([chosen_item, price, message_author])
    del inventories[message_author][int(item_number) - 1]

    ocs.close_bazaar(ctx, the_bazaar)
    ocs.close_inv(ctx, inventories)

    item_name = cde.create_item_embed(chosen_item, "get a load of this ratiooo")[1]
    await ctx.message.edit(content=f"**{ctx.author.name}**, you have successfully sold **{item_name}** for **{price}** "
                                   f"{a_setup.kk} to the bazaar!")


@a_setup.slash.slash(description="Pick up one of your items from the bazaar", guild_ids=a_setup.guild_ids)
async def claim(ctx, item_number):

    print(f"{ctx.author.name} used the claim command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")

    the_bazaar = ocs.open_bas(ctx)
    inventories = ocs.open_inv(ctx)

    try:
        chosen_item_ls = the_bazaar["bazaar"][int(item_number) - 1]
    except IndexError:
        await ctx.message.edit(content=f"Invalid item-number, **{ctx.author.name}**!")
        return

    if not chosen_item_ls[2] == message_author:
        await ctx.message.edit(content=f"This is not your item, **{ctx.author.name}**!")
        return

    del the_bazaar["bazaar"][int(item_number) - 1]
    inventories[message_author].append(chosen_item_ls[0])

    ocs.close_bazaar(ctx, the_bazaar)
    ocs.close_inv(ctx, inventories)

    item_name = cde.create_item_embed(chosen_item_ls[0], "ratio???")[1]
    await ctx.message.edit(content=f"**{ctx.author.name}**, you have successfully claimed **{item_name}** "
                                   f"from the bazaar!")


@a_setup.slash.slash(description="Buy something from the bazaar", guild_ids=a_setup.guild_ids)
async def buy_bazaar(ctx, item_number):

    print(f"{ctx.author.name} used the buy command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")

    the_bazaar = ocs.open_bas(ctx)
    inventories = ocs.open_inv(ctx)
    users_crowns = ocs.open_crowns(ctx)

    try:
        chosen_item_ls = the_bazaar["bazaar"][int(item_number) - 1]
    except IndexError:
        await ctx.message.edit(content=f"Invalid item-number, **{ctx.author.name}**!")
        return

    if users_crowns[message_author] < int(chosen_item_ls[1]):
        await ctx.message.edit(content=f"You don't have enough Kjell Crowns to buy this, **{ctx.author.name}**!")
        return

    users_crowns[message_author] -= int(chosen_item_ls[1])
    users_crowns[chosen_item_ls[2]] += int(chosen_item_ls[1])
    del the_bazaar["bazaar"][int(item_number) - 1]
    inventories[message_author].append(chosen_item_ls[0])

    ocs.close_bazaar(ctx, the_bazaar)
    ocs.close_inv(ctx, inventories)
    ocs.close_crowns(ctx, users_crowns)

    item_name = cde.create_item_embed(chosen_item_ls[0], "ratioooo")[1]

    if message_author == chosen_item_ls[2]:
        await ctx.message.edit(content=f"**{ctx.author.name}**, you have bought your own item from the bazaar... "
                                       f"You could've just used **/claim** for that...")
        return

    await ctx.message.edit(content=f"**{ctx.author.name}**, you have successfully bought **{item_name}** from "
                                   f"{chosen_item_ls[2]} for **{chosen_item_ls[1]}** {a_setup.kk}!")
