import setup
import create_item_embeds as cde
import discord as dc
import open_close_stuff as ocs
import datetime
import create_shop as cs


@setup.slash.slash(description="Take a look at the current shop", guild_ids=setup.guild_ids)
async def shop(ctx):

    print(f"{ctx.author.name} used the shop command")

    await ctx.send("Your message is on it's way...")

    today = str(datetime.date.today())
    description = cs.cs(ctx)

    embed = dc.Embed(title=f"**The current shop**", colour=dc.Colour(0x485885), description=description)
    embed.set_footer(text=f"Shop - {today}")

    await ctx.message.edit(content=None, embed=embed)
    await ctx.message.add_reaction("🔄")


@setup.slash.slash(description="Take a look at the current shop", guild_ids=setup.guild_ids)
async def item_shop(ctx, item_number):

    print(f"{ctx.author.name} used the item_shop command")

    await ctx.send("Your message is on it's way...")

    shop_data = ocs.open_shop(ctx)
    today = str(datetime.date.today())

    try:
        chosen_item = shop_data[today][int(item_number) - 1][0]  # str of the item name

    except IndexError:
        await ctx.message.edit(content=f"Invalid item-number **{ctx.author.name}**!")
        return

    except KeyError:
        await ctx.message.edit(content=f"**Check out the shop** before you use that, **{ctx.author.name}**!")
        return

    embed_and_item_name = cde.create_item_embed(chosen_item, "Shop-item")
    await ctx.message.edit(content=None, embed=embed_and_item_name[0])


@setup.slash.slash(description="Take a look at the current shop", guild_ids=setup.guild_ids)
async def buy_shop(ctx, item_number):

    print(f"{ctx.author.name} used the buy command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")

    inventories = ocs.open_inv(ctx)
    users_crowns = ocs.open_crowns(ctx)
    shop_data = ocs.open_shop(ctx)
    today = str(datetime.date.today())

    try:
        chosen_item_ls = shop_data[today][int(item_number) - 1]
    except IndexError:
        await ctx.message.edit(content=f"Invalid item-number, **{ctx.author.name}**!")
        return

    except KeyError:
        await ctx.message.edit(content=f"**Check out the shop** before you use that, **{ctx.author.name}**!")
        return

    if shop_data[today][int(item_number) - 1][2] == "sold":
        await ctx.message.edit(content=f"Someone has **already bought** that item, **{ctx.author.name}**!")
        return

    if users_crowns[message_author] < int(chosen_item_ls[1]):
        await ctx.message.edit(content=f"You don't have enough Kjell Crowns to buy this, **{ctx.author.name}**!")
        return

    users_crowns[message_author] -= int(chosen_item_ls[1])
    shop_data[today][int(item_number) - 1][2] = "sold"
    inventories[message_author].append(chosen_item_ls[0])

    ocs.close_inv(ctx, inventories)
    ocs.close_crowns(ctx, users_crowns)
    ocs.close_shop(ctx, shop_data)

    item_name = cde.create_item_embed(chosen_item_ls[0], "ratioooo")[1]

    await ctx.message.edit(content=f"**{ctx.author.name}**, you have successfully bought **{item_name}** from "
                                   f"**the shop** for **{chosen_item_ls[1]}** {setup.kk}!")
