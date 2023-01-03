# import a_setup
# import b_create_item_embeds as cde
# import d_open_close_stuff as ocs
# import b_community_server_active as csa
# import discord as dc
#
#
# @a_setup.client.slash_command(name="sell-bazaar", description="Sell a item to the bazaar", guild_ids=a_setup.guild_ids)
# async def sell_bazaar(ctx, price: dc.Option(int), item_number: dc.Option(int)):
#     await ctx.respond("Your message is on it's way...")
#
#     ma = ctx.author.mention.replace("!", "")
#     printed_author = csa.get_printed_author_name(ctx.author)
#     ocs.check_user(ma)
#
#     if price < 0:
#         price = 250
#     elif price > 10000:
#         price = 10000
#
#     try:
#         chosen_item = ocs.data[ma]["inv"][int(item_number) - 1]
#     except IndexError:
#         await ctx.edit(content=f"Invalid item-number, **{printed_author}**!")
#         return
#
#     ocs.data["bazaar"].append([chosen_item, price, ma])
#     del ocs.data[ma]["inv"][int(item_number) - 1]
#
#     item_name = cde.create_item_embed(chosen_item, "get a load of this ratio")[1]
#     await ctx.edit(content=f"**{printed_author}**, you have successfully sold **{item_name}** for **{price}** "
#                            f"{a_setup.kk} to the bazaar!")
#
#
# @a_setup.client.slash_command(name="claim-bazaar", description="Pick up one of your items from the bazaar",
#                               guild_ids=a_setup.guild_ids)
# async def claim_bazaar(ctx, item_number: dc.Option(int)):
#     await ctx.respond("Your message is on it's way...")
#
#     ma = ctx.author.mention.replace("!", "")
#     printed_author = csa.get_printed_author_name(ctx.author)
#
#     try:
#         chosen_item_ls = ocs.data["bazaar"][int(item_number) - 1]
#     except IndexError:
#         await ctx.edit(content=f"Invalid item-number, **{printed_author}**!")
#         return
#
#     if not chosen_item_ls[2] == ma:
#         await ctx.edit(content=f"This is not your item, **{printed_author}**!")
#         return
#
#     del ocs.data["bazaar"][int(item_number) - 1]
#     ocs.data[ma]["inv"].append(chosen_item_ls[0])
#
#     item_name = cde.create_item_embed(chosen_item_ls[0], "ratio???")[1]
#     await ctx.edit(content=f"**{printed_author}**, you have successfully claimed **{item_name}** "
#                            f"from the bazaar!")
#
#
# @a_setup.client.slash_command(name="buy-bazaar", description="Buy something from the bazaar",
#                               guild_ids=a_setup.guild_ids)
# async def buy_bazaar(ctx, item_number: dc.Option(int)):
#     await ctx.respond("Your message is on it's way...")
#
#     ma = ctx.author.mention.replace("!", "")
#     printed_author = csa.get_printed_author_name(ctx.author)
#     ocs.check_user(ma)
#
#     try:
#         chosen_item_ls = ocs.data["bazaar"][int(item_number) - 1]
#     except IndexError:
#         await ctx.edit(content=f"Invalid item-number, **{printed_author}**!")
#         return
#
#     if ocs.data[ma]["kk"] < int(chosen_item_ls[1]):
#         await ctx.edit(content=f"You don't have enough Kjell Crowns to buy this, **{printed_author}**!")
#         return
#
#     ocs.data[ma]["kk"] -= int(chosen_item_ls[1])
#     ocs.data[chosen_item_ls[2]]["kk"] += int(chosen_item_ls[1])
#     del ocs.data["bazaar"][int(item_number) - 1]
#     ocs.data[ma]["inv"].append(chosen_item_ls[0])
#
#     item_name = cde.create_item_embed(chosen_item_ls[0], "ratio")[1]
#
#     if ma == chosen_item_ls[2]:
#         await ctx.edit(content=f"**{printed_author}**, you have bought your own item from the bazaar... "
#                                f"You could've just used **/claim** for that...")
#         return
#
#     await ctx.edit(content=f"**{printed_author}**, you have successfully bought **{item_name}** from "
#                            f"{chosen_item_ls[2]} for **{chosen_item_ls[1]}** {a_setup.kk}!")
#