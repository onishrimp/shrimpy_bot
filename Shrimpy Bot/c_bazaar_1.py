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
async def bazaar(ctx, starting_page):

    print(f"{ctx.author.name} used the bazaar command")

    await ctx.send("Your message is on it's way...")

    the_bazaar = ocs.open_bas(ctx)
    printed_author = csa.get_printed_author_name(ctx.author)

    description = ""

    try:
        page = int(starting_page)
    except ValueError:
        ctx.message.edit(f"Invalid starting page, {printed_author}")
        return

    if page < 1:
        page = 1

    if not the_bazaar["bazaar"]:
        description = "The bazaar is empty!"

    else:
        item_range = 25 * (page - 1)
        bazaar_index = item_range + 1

        for d in range(item_range, item_range + 25):
            try:
                tb = the_bazaar["bazaar"][d]
                description += f"**{bazaar_index}** - {cde.create_item_embed(tb[0], None)[1]} - " \
                               f"{tb[1]} {a_setup.kk} - von {tb[2]}\n"
            except IndexError:
                break
            bazaar_index += 1

    embed = dc.Embed(title="**The current bazaar**", colour=dc.Colour(0x485885), description=description)
    embed.set_footer(text="Page 1")

    await ctx.message.edit(content=None, embed=embed)
    await ctx.message.add_reaction("◀️")
    await ctx.message.add_reaction("▶️")
    await ctx.message.add_reaction("🔄")
