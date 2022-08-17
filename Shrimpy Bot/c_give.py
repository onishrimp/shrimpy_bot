import setup
import open_close_stuff as ocs


@setup.slash.slash(description="Gift something, only usable by the administrator", guild_ids=setup.guild_ids)
async def give(ctx, gift, addressee):

    print(f"{ctx.author.name} used the give command on {addressee}")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")
    addressee = addressee.replace("!", "")

    if not message_author == setup.bot_owner:
        await ctx.message.edit(content=f"**YOU ARE NOT MY MASTER 👺**")
        return

    try:
        gift = int(gift)
        crowns = True

    except ValueError:
        crowns = False

    if crowns:
        users_crowns = ocs.open_crowns(ctx)

        if addressee not in users_crowns:
            users_crowns[addressee] = 300

        users_crowns[addressee] += gift
        ocs.close_crowns(ctx, users_crowns)

        await ctx.message.edit(content=f"You have successfully gifted {addressee} **{gift}** {setup.kk}, master!")

    else:
        inventories = ocs.open_inv(ctx)
        items = ocs.open_items()

        if gift not in items:
            await ctx.message.edit(content=f"Unknown item, master.")
            return

        if addressee not in inventories:
            inventories[addressee] = []

        inventories[addressee].append(gift)
        ocs.close_inv(ctx, inventories)

        await ctx.message.edit(content=f"You have successfully gifted {addressee} an item, master!")


@setup.slash.slash(description="Give someone crowns", guild_ids=setup.guild_ids)
async def pay(ctx, crown_quantity, addressee):

    print(f"{ctx.author.name} used the pay command on {addressee}")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")
    addressee = addressee.replace("!", "")

    try:
        crown_quantity = int(crown_quantity)

    except ValueError:
        await ctx.message.edit(content=f"Invalid crown quantity, **{ctx.author.name}**!")
        return

    users_crowns = ocs.open_crowns(ctx)

    if addressee not in users_crowns:
        await ctx.message.edit(content=f"This addressee **doesn't exist** or **never possessed crowns**, **{ctx.author.name}**!")
        return

    if users_crowns[message_author] < crown_quantity:
        await ctx.message.edit(content=f"You don't have **enough Kjell Crowns** to pay someone that much, **{ctx.author.name}**!")
        return

    users_crowns[message_author] -= crown_quantity
    users_crowns[addressee] += crown_quantity

    ocs.close_crowns(ctx, users_crowns)

    await ctx.message.edit(content=f"**{ctx.author.name}**, you have succesfully payed {addressee} **{crown_quantity}** {setup.kk}!")
