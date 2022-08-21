import a_setup
import b_create_item_embeds as cde
import d_open_close_stuff as ocs
import b_generate_random_items as gri
import b_community_server_active as csa


@a_setup.slash.slash(description="Gamble for 200 Kjell Crowns", guild_ids=a_setup.guild_ids)
async def gamble(ctx):

    print(f"{ctx.author.name} used the gamble command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")
    printed_author = csa.get_printed_author_name(ctx.author)

    users_crowns = ocs.open_crowns(ctx)
    inventory = ocs.open_inv(ctx)

    if not users_crowns[message_author] >= 200:
        await ctx.message.edit(content=f"**{printed_author}**, you don't have enough {a_setup.kk} to gamble!")
        return

    users_crowns[message_author] -= 200

    if message_author not in inventory:
        inventory[message_author] = []

    chosen_item = gri.gri([90, 50, 40, 15, 1], 1, 4)[0]

    try:
        chosen_item = int(chosen_item)
        await ctx.message.edit(content=f"Wow! Congratulations **{printed_author}**! You pulled **600** "
                               f"{a_setup.kk} instead of an item!")
        users_crowns[message_author] += chosen_item

    except ValueError:
        inventory[message_author].append(chosen_item)
        embed_and_item_name = cde.create_item_embed(chosen_item, f"Property of {printed_author}")

        await ctx.message.edit(content=None, embed=embed_and_item_name[0])
        await ctx.channel.send(f"Congratulations! You pulled **{embed_and_item_name[1]}**!")

    ocs.close_crowns(ctx, users_crowns)
    ocs.close_inv(ctx, inventory)
