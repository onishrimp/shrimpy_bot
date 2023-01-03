import a_setup
import b_create_item_embeds as cde
import d_open_close_stuff as ocs
import b_community_server_active as csa
import discord as dc


@a_setup.client.slash_command(name="sell-bank", description="Sell a item to the bank", guild_ids=a_setup.guild_ids)
async def sell_bank(ctx, item_number: dc.Option(int, description="Number from your inventory")):
    await ctx.respond("Your message is on it's way...")

    ma = ctx.author.mention.replace("!", "")
    printed_author = csa.get_printed_author_name(ctx.author)

    items = ocs.open_items()
    ocs.check_user(ma)

    bank_prices = {
        "common": 40,
        "uncommon": 60,
        "rare": 90,
        "epic": 220,
        "legendary": 800,
    }

    try:
        chosen_item = ocs.data[ma]["inv"][int(item_number) - 1]  # str name of the item
        del ocs.data[ma]["inv"][int(item_number) - 1]

    except IndexError:
        await ctx.edit(content=f"Invalid item-number **{printed_author}**!")
        return

    if items[chosen_item[0]][0] not in bank_prices:
        await ctx.edit(content=f"You can't sell this item, **{printed_author}**")
        return

    crown_reward = bank_prices[items[chosen_item[0]][0]]
    ocs.data[ma]["kk"] += crown_reward
    item_name = cde.create_item_embed(chosen_item, "this string won't be used L")[1]

    await ctx.edit(content=f"**{printed_author}**, you have successfully sold **{item_name}** for "
                           f"**{crown_reward}** {a_setup.kk}!")
