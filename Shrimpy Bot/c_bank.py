import setup
import create_item_embeds as cde
import open_close_stuff as ocs


@setup.slash.slash(description="Sell a item to the bank", guild_ids=setup.guild_ids)
async def sell_bank(ctx, item_number):

    print(f"{ctx.author.name} used the sell_bank command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")

    inventories = ocs.open_inv(ctx)
    users_crowns = ocs.open_crowns(ctx)
    items = ocs.open_items()

    bank_prices = {
        "common": 40,
        "uncommon": 60,
        "rare": 90,
        "epic": 220,
        "legendary": 800,
    }

    try:
        chosen_item = inventories[message_author][int(item_number) - 1]  # str name of the item
        del inventories[message_author][int(item_number) - 1]

    except IndexError:
        await ctx.message.edit(content=f"Invalid item-number **{ctx.author.name}**!")
        return

    if items[chosen_item][0] not in bank_prices:
        await ctx.message.edit(content=f"You can't sell this item, **{ctx.author.name}**")
        return

    crown_reward = bank_prices[items[chosen_item][0]]
    users_crowns[message_author] += crown_reward
    item_name = cde.create_item_embed(chosen_item, "this string won't be used L")[1]

    ocs.close_crowns(ctx, users_crowns)
    ocs.close_inv(ctx, inventories)

    await ctx.message.edit(content=f"**{ctx.author.name}**, you have successfully sold **{item_name}** for "
                                   f"**{crown_reward}** {setup.kk}!")
