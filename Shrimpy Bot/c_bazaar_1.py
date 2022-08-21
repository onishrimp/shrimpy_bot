import a_setup
import b_create_item_embeds as cde
import discord as dc
import d_open_close_stuff as ocs
import b_community_server_active as csa


@a_setup.slash.slash(description="Take a look at one of the bazaar-items", guild_ids=a_setup.guild_ids)
async def view_bazaar_item(ctx, item_number):

    print(f"{ctx.author.name} used the item_bazaar command")

    await ctx.send("Your message is on it's way...")
    printed_author = csa.get_printed_author_name(ctx.author)
    the_bazaar = ocs.open_bas(ctx)

    try:
        chosen_item = the_bazaar["bazaar"][int(item_number) - 1][0]  # str of the item name

    except IndexError:
        await ctx.message.edit(content=f"Invalid item-number **{printed_author}**!")
        return

    embed_and_item_name = cde.create_item_embed(chosen_item, "Bazaar-item")
    await ctx.message.edit(content=None, embed=embed_and_item_name[0])


@a_setup.slash.slash(description="Get the current bazaar", guild_ids=a_setup.guild_ids)
async def bazaar(ctx):

    print(f"{ctx.author.name} used the bazaar command")

    await ctx.send("Your message is on it's way...")

    the_bazaar = ocs.open_bas(ctx)

    description = ""
    bazaar_index = 1

    if not the_bazaar["bazaar"]:
        description = "The bazaar is empty!"

    else:
        for d in the_bazaar["bazaar"]:
            if bazaar_index <= 25:
                d_name = cde.create_item_embed(d[0], "das hier ist ein Osterei")[1]
                description += f"**{bazaar_index}** - {d_name} - {d[1]} {a_setup.kk} - von {d[2]}\n"
                bazaar_index += 1

    embed = dc.Embed(title="**The current bazaar**", colour=dc.Colour(0x485885), description=description)
    embed.set_footer(text="Page 1")

    await ctx.message.edit(content=None, embed=embed)
    await ctx.message.add_reaction("◀️")
    await ctx.message.add_reaction("▶️")
    await ctx.message.add_reaction("🔄")
