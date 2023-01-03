import a_setup
import b_create_item_embeds as cde
import discord as dc
import d_open_close_stuff as ocs
import datetime
import b_create_shop as cs
import b_ora_baz_inv_sho as orabis


class BuyModal(dc.ui.Modal):
    def __init__(self, *args, **kwargs):
        super(BuyModal, self).__init__(*args, **kwargs)
        self.add_item(dc.ui.InputText(label="Number to buy", placeholder="ex.: 1"))

    async def callback(self, interaction):
        ma = interaction.user.mention.replace("!", "")

        item_number = self.children[0].value
        await interaction.response.edit_message(content=None)
        today = str(datetime.date.today())

        try:
            chosen_item_ls = ocs.data["shop"][today][int(item_number) - 1]
        except IndexError:
            await interaction.channel.send(content=f"Invalid item-number, **{ma}**!")
            return
        except KeyError:
            await interaction.channel.send(content=f"**Check out the shop** before you use that, **{ma}**!")
            return
        except ValueError:
            return
        if ocs.data["shop"][today][int(item_number) - 1][2] == "sold":
            await interaction.channel.send(content=f"Someone has **already bought** that item, **{ma}**!")
            return
        elif ocs.data[ma]["kk"] < int(chosen_item_ls[1]):
            await interaction.channel.send(content=f"You don't have enough Kjell Crowns to buy this, **{ma}**!")
            return

        ocs.data[ma]["kk"] -= int(chosen_item_ls[1])
        ocs.data["shop"][today][int(item_number) - 1][2] = "sold"
        ocs.data[ma]["inv"].append(chosen_item_ls[0])

        item_name = cde.create_item_embed(chosen_item_ls[0], "ratioooo")[1]
        await interaction.channel.send(content=f"**{ma}**, you have successfully bought **{item_name}** from "
                               f"**the shop** for **{chosen_item_ls[1]}** {a_setup.kk}!")


class ShopView(dc.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @dc.ui.button(style=dc.ButtonStyle.blurple, emoji="◀", custom_id="a_left", disabled=True, row=0)
    async def arrow_left_callback(self, button, interaction):
        if not interaction.user == self.ctx.author:
            return
        await interaction.response.edit_message(content=None)

        embed_ls = interaction.message.embeds
        num = int(embed_ls[0].title.split(" ")[0].split("*")[2])
        cs.cs()
        orabis.disable_certain_children(num, self.children, len(ocs.data["shop"][str(datetime.date.today())]), True)

        chosen_item = ocs.data["shop"][str(datetime.date.today())][num - 2][0]
        embed_and_item_name = cde.create_item_embed(chosen_item, f"**{num - 1} - Property of {interaction.user.name}**")
        await interaction.edit_original_response(embed=embed_and_item_name[0], view=self)

    @dc.ui.button(style=dc.ButtonStyle.blurple, emoji="▶", custom_id="a_right", disabled=True, row=0)
    async def arrow_right_callback(self, button, interaction):
        if not interaction.user == self.ctx.author:
            return
        await interaction.response.edit_message(content=None)

        embed_ls = interaction.message.embeds
        num = int(embed_ls[0].title.split(" ")[0].split("*")[2])
        cs.cs()
        orabis.disable_certain_children(num, self.children, len(ocs.data["shop"][str(datetime.date.today())]), False)

        chosen_item = ocs.data["shop"][str(datetime.date.today())][num][0]
        embed_and_item_name = cde.create_item_embed(chosen_item, f"**{num + 1} - Property of {interaction.user.name}**")
        await interaction.edit_original_response(embed=embed_and_item_name[0], view=self)

    @dc.ui.button(style=dc.ButtonStyle.blurple, emoji="🔄", custom_id="ccw", row=0)
    async def arrow_ccw_callback(self, button, interaction):
        await interaction.response.edit_message(content=None)
        ma = interaction.user.mention.replace("!", "")
        description, embed_title, footer = orabis.shop_requested()
        await orabis.create_and_send_embed(embed_title, description, footer, interaction, ma, self)


    @dc.ui.button(style=dc.ButtonStyle.green, emoji="🌓", row=1)
    async def change_shop_mode_callback(self, button, interaction):
        if not interaction.user == self.ctx.author:
            return
        await interaction.response.edit_message(content=None)

        ma = interaction.user.mention.replace("!", "")
        button.emoji, in_view_mode = {"🌓": ["🌗", False], "🌗": ["🌓", True]}[button.emoji.name]

        disable = ["ccw"]
        enable = ["a_right"]
        if in_view_mode:
            disable, enable = enable, disable
            disable.append("a_left")

        for b in self.children:
            if b.custom_id in disable:
                b.disabled = True
            elif b.custom_id in enable:
                b.disabled = False

        if in_view_mode:
            description, embed_title, footer = orabis.shop_requested()
            await orabis.create_and_send_embed(embed_title, description, footer, interaction, ma, self)
            return

        cs.cs()
        chosen_item = ocs.data["shop"][str(datetime.date.today())][0][0]
        embed_and_item_name = cde.create_item_embed(chosen_item, "**1 - Shop-item**")
        await interaction.edit_original_response(embed=embed_and_item_name[0], view=self)


    @dc.ui.button(style=dc.ButtonStyle.green, label="Buy", row=1)
    async def buy_callback(self, button, interaction):
        modal = BuyModal(title="Number to buy")
        await interaction.response.send_modal(modal)


@a_setup.client.slash_command(description="Take a look at the current shop", guild_ids=a_setup.guild_ids)
async def shop(ctx):
    await ctx.respond("Your message is on it's way...")
    ma = ctx.author.mention.replace("!", "")

    today = str(datetime.date.today())
    description = cs.cs()

    embed = dc.Embed(title=f"**The current shop**", colour=dc.Colour(ocs.data[ma]["color"]), description=description)
    embed.set_footer(text=f"Shop - {today}")

    await ctx.edit(content=None, embed=embed, view=ShopView(ctx))


# @a_setup.client.slash_command(description="Take a look at the current shop", guild_ids=a_setup.guild_ids)
# async def view_shop_item(ctx, item_number: dc.Option(int)):
#     await ctx.respond("Your message is on it's way...")
#
#     printed_author = csa.get_printed_author_name(ctx.author)
#     today = str(datetime.date.today())
#
#     try:
#         chosen_item = ocs.data["shop"][today][int(item_number) - 1][0]  # str of the item name
#
#     except IndexError:
#         await ctx.edit(content=f"Invalid item-number **{printed_author}**!")
#         return
#
#     except KeyError:
#         await ctx.edit(content=f"**Check out the shop** before you use that, **{printed_author}**!")
#         return
#
#     embed_and_item_name = cde.create_item_embed(chosen_item, "Shop-item")
#     await ctx.edit(content=None, embed=embed_and_item_name[0])


# @a_setup.client.slash_command(description="Take a look at the current shop", guild_ids=a_setup.guild_ids)
# async def buy_shop(ctx, item_number: dc.Option(int)):
#     await ctx.respond("Your message is on it's way...")
#
#     ma = ctx.author.mention.replace("!", "")
#     printed_author = csa.get_printed_author_name(ctx.author)
#
#     today = str(datetime.date.today())
#
#     try:
#         chosen_item_ls = ocs.data["shop"][today][int(item_number) - 1]
#     except IndexError:
#         await ctx.edit(content=f"Invalid item-number, **{printed_author}**!")
#         return
#
#     except KeyError:
#         await ctx.edit(content=f"**Check out the shop** before you use that, **{printed_author}**!")
#         return
#
#     if ocs.data["shop"][today][int(item_number) - 1][2] == "sold":
#         await ctx.edit(content=f"Someone has **already bought** that item, **{printed_author}**!")
#         return
#
#     if ocs.data[ma]["kk"] < int(chosen_item_ls[1]):
#         await ctx.edit(content=f"You don't have enough Kjell Crowns to buy this, **{printed_author}**!")
#         return
#
#     ocs.data[ma]["kk"] -= int(chosen_item_ls[1])
#     ocs.data["shop"][today][int(item_number) - 1][2] = "sold"
#     ocs.data[ma]["inv"].append(chosen_item_ls[0])
#
#     item_name = cde.create_item_embed(chosen_item_ls[0], "ratioooo")[1]
#     await ctx.edit(content=f"**{printed_author}**, you have successfully bought **{item_name}** from "
#                            f"**the shop** for **{chosen_item_ls[1]}** {a_setup.kk}!")
