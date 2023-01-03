import a_setup
import b_create_item_embeds as cde
import d_open_close_stuff as ocs
import b_generate_random_items as gri
import b_community_server_active as csa


@a_setup.client.slash_command(description="Gamble for 200 Kjell Crowns", guild_ids=a_setup.guild_ids)
async def gamble(ctx):
    await ctx.respond("Your message is on it's way...")

    ma = ctx.author.mention.replace("!", "")
    printed_author = csa.get_printed_author_name(ctx.author)
    ocs.check_user(ma)

    if not ocs.data[ma]["kk"] >= 200:
        await ctx.edit(content=f"**{printed_author}**, you don't have enough {a_setup.kk} to gamble!")
        return
    ocs.data[ma]["kk"] -= 200

    chosen_item = gri.gri([90, 50, 40, 15, 1], 1, 4)[0]

    try:
        chosen_item = int(chosen_item)
        await ctx.edit(content=f"Wow! Congratulations **{printed_author}**! You pulled **600** "
                               f"{a_setup.kk} instead of an item!")
        ocs.data[ma]["kk"] += chosen_item

    except TypeError:
        ocs.data[ma]["inv"].append(chosen_item)
        embed_and_item_name = cde.create_item_embed(chosen_item, f"Property of {printed_author}")

        await ctx.edit(content=None, embed=embed_and_item_name[0])
        await ctx.channel.send(f"Congratulations! You pulled **{embed_and_item_name[1]}**!")
