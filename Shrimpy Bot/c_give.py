import a_setup
import d_open_close_stuff as ocs
import b_create_item_embeds as cie


@a_setup.slash.slash(description="Gift something, only usable by the administrator", guild_ids=a_setup.guild_ids)
async def admin_give(ctx, gift, addressee):

    print(f"{ctx.author.name} used the admin_give command on {addressee}")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")
    addressee = addressee.replace("!", "")

    if message_author not in a_setup.bot_owners:
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

        await ctx.message.edit(content=f"You have successfully gifted {addressee} **{gift}** {a_setup.kk}, master!")

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

        item_name = cie.create_item_embed(gift, "whatever, this value won't be needed anyway")[1]

        await ctx.message.edit(content=f"You have successfully gifted {addressee} **{item_name}**, master!")


@a_setup.slash.slash(description="Give someone your crowns", guild_ids=a_setup.guild_ids)
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
        await ctx.message.edit(content=f"This addressee **doesn't exist** or **never possessed crowns**, "
                                       f"**{ctx.author.name}**!")
        return

    if users_crowns[message_author] < crown_quantity:
        await ctx.message.edit(content=f"You don't have **enough Kjell Crowns** to pay someone that much, "
                                       f"**{ctx.author.name}**!")
        return

    users_crowns[message_author] -= crown_quantity
    users_crowns[addressee] += crown_quantity

    ocs.close_crowns(ctx, users_crowns)

    await ctx.message.edit(content=f"**{ctx.author.name}**, you have successfully payed {addressee} "
                                   f"**{crown_quantity}** {a_setup.kk}!")


@a_setup.slash.slash(description="Give someone an item of your inventory", guild_ids=a_setup.guild_ids)
async def give(ctx, item_number, addressee):

    print(f"{ctx.author.name} used the give command on {addressee}")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")
    addressee = addressee.replace("!", "")

    inventories = ocs.open_inv(ctx)

    try:
        item_number = int(item_number)

    except ValueError:
        await ctx.message.edit(content=f"Invalid input, **{ctx.author.name}**!")
        return

    try:
        chosen_item = inventories[message_author][item_number - 1]
        inventories[addressee].append(chosen_item)
        del inventories[message_author][item_number - 1]

    except IndexError:
        await ctx.message.edit(content=f"Invalid item-number **{ctx.author.name}**!")
        return

    item_name = cie.create_item_embed(chosen_item, "whatever, this value won't be needed anyway")[1]

    await ctx.message.edit(content=f"**{ctx.author.name}**, you have successfully gifted **{item_name}** to "
                                   f"{addressee}!")
