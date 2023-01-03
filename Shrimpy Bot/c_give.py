import a_setup
import d_open_close_stuff as ocs
import b_create_item_embeds as cie
import discord as dc


@a_setup.client.slash_command(name="admin-give", description="Gift something, only usable by the administrator",
                              guild_ids=a_setup.guild_ids)
async def admin_give(ctx, gift: dc.Option(description="Crowns or an item"),
                     addressee: dc.Option(description="To whom?"),
                     attack: dc.Option(int, required=False, description="Required if it's an item"),
                     defence: dc.Option(int, required=False, description="Required if it's an item")):

    print(f"{ctx.author.name} used the admin_give command on {addressee}")
    await ctx.respond("Your message is on it's way...", ephemeral=True)

    ma = ctx.author.mention.replace("!", "")
    addressee = addressee.replace("!", "")

    if ma not in a_setup.bot_owners:
        await ctx.edit(content=f"**YOU ARE NOT MY MASTER 👺**")
        return

    ocs.check_user(ma)
    ocs.check_user(addressee)

    try:
        gift = int(gift)
        crowns = True

    except ValueError:
        crowns = False

    if crowns:
        ocs.data[addressee]["kk"] += gift
        await ctx.edit(content=f"You have successfully gifted {addressee} **{gift}** {a_setup.kk}, master!")

    else:
        items = ocs.open_items()

        if gift not in items:
            await ctx.edit(content=f"Unknown item, master.")
            return

        if attack is None:
            attack = 50
        if defence is None:
            defence = 100

        full_gift = [gift, [int(attack), int(defence)]]
        ocs.data[addressee]["inv"].append(full_gift)
        item_name = cie.create_item_embed(full_gift, "whatever, this value won't be needed anyway")[1]

        await ctx.edit(content=f"You have successfully gifted {addressee} **{item_name}**, master!")


@a_setup.client.slash_command(description="Give someone your crowns", guild_ids=a_setup.guild_ids)
async def pay(ctx, crown_quantity: dc.Option(int, description="How many crowns?"),
              addressee: dc.Option(description="To whom?")):
    print(f"{ctx.author.name} used the pay command on {addressee}")
    await ctx.respond("Your message is on it's way...")

    ma = ctx.author.mention.replace("!", "")
    addressee = addressee.replace("!", "")

    ocs.check_user(addressee)
    ocs.check_user(ma)

    if ocs.data[ma]["kk"] < crown_quantity:
        await ctx.edit(content=f"You don't have **enough Kjell Crowns** to pay someone that much, "
                               f"**{ma}**!")
        return

    if crown_quantity < 0:
        await ctx.edit(content=f"Invalid amount, **{ma}**!")
        return

    ocs.data[ma]["kk"] -= crown_quantity
    ocs.data[addressee]["kk"] += crown_quantity

    if ma == addressee:
        message_content = f"**{ma}**, you have successfully payed {addressee} " \
                        f"**{crown_quantity}** {a_setup.kk}! Why tho"

    else:
        message_content = f"**{ma}**, you have successfully payed {addressee} " \
                                   f"**{crown_quantity}** {a_setup.kk}!"

    await ctx.edit(content=message_content)


@a_setup.client.slash_command(description="Give someone an item of your inventory", guild_ids=a_setup.guild_ids)
async def give(ctx, item_number: dc.Option(int, description="Number from your inventory"), addressee: dc.Option(description="To whom?")):
    print(f"{ctx.author.name} used the give command on {addressee}")
    await ctx.respond("Your message is on it's way...")

    ma = ctx.author.mention.replace("!", "")
    addressee = addressee.replace("!", "")
    ocs.check_user(ma)
    ocs.check_user(addressee)

    try:
        chosen_item = ocs.data[ma]["inv"][item_number - 1]
        ocs.data[addressee]["inv"].append(chosen_item)
        del ocs.data[ma]["inv"][item_number - 1]

    except IndexError:
        await ctx.edit(content=f"Invalid item-number **{ma}**!")
        return

    item_name = cie.create_item_embed(chosen_item, "whatever, this value won't be needed anyway")[1]
    await ctx.edit(content=f"**{ma}**, you have successfully gifted **{item_name}** to "
                           f"{addressee}!")
