import a_setup
import b_create_item_embeds as cie
import discord as dc
import d_open_close_stuff as ocs
import b_ora_baz_inv_sho as orabis


# @a_setup.client.slash_command(name="view-bazaar-item", description="Take a look at one of the bazaar-items",
#                               guild_ids=a_setup.guild_ids)
# async def view_bazaar_item(ctx, item_number: dc.Option(int)):
#     await ctx.respond("Your message is on it's way...")
#     printed_author = csa.get_printed_author_name(ctx.author)
#
#     try:
#         chosen_item = ocs.data["bazaar"][int(item_number) - 1][0]  # str of the item name
#
#     except IndexError:
#         await ctx.edit(content=f"Invalid item-number **{printed_author}**!")
#         return
#
#     embed_and_item_name = cie.create_item_embed(chosen_item, "Bazaar-item")
#     await ctx.edit(content=None, embed=embed_and_item_name[0])


class BazModal(dc.ui.Modal):
    def __init__(self, self_, *args, **kwargs):
        super(BazModal, self).__init__(*args, **kwargs)
        self.add_item(dc.ui.InputText(label="Starting Number", placeholder="ex.: 1"))
        self.self_ = self_

    async def callback(self, interaction):
        if not ocs.data["bazaar"]:
            return

        item_number = self.children[0].value
        try:
            chosen_item = ocs.data["bazaar"][int(item_number) - 1]
        except (IndexError, ValueError, ValueError):
            chosen_item = ocs.data["bazaar"][0]

        item_number = int(item_number)
        disables = ["ccw"]
        if item_number == 1:
            disables.append("a_left")
        if item_number == len(ocs.data["bazaar"]):
            disables.append("a_right")
        for b in self.self_.children:
            if b.custom_id in disables:
                b.disabled = True

        embed_and_item_name = cie.create_item_embed(
            chosen_item[0], f"**{item_number} - Bazaar-item**")
        await interaction.response.edit_message(embed=embed_and_item_name[0], view=self.self_)


class GetModal(dc.ui.Modal):
    def __init__(self, *args, **kwargs):
        super(GetModal, self).__init__(*args, **kwargs)
        self.add_item(dc.ui.InputText(label="Number to buy or claim", placeholder="ex.: 1"))

    async def callback(self, interaction):
        ma = interaction.user.mention.replace("!", "")
        ocs.check_user(ma)

        item_number = self.children[0].value
        await interaction.response.edit_message(content=None)

        try:
            chosen_item_ls = ocs.data["bazaar"][int(item_number) - 1]
        except (IndexError, ValueError, ValueError):
            await interaction.channel.send(content=f"Invalid item-number, {ma}!")
            return

        if chosen_item_ls[2] == ma:
            del ocs.data["bazaar"][int(item_number) - 1]
            ocs.data[ma]["inv"].append(chosen_item_ls[0])
            item_name = cie.create_item_embed(chosen_item_ls[0], "ratio???")[1]
            await interaction.channel.send(content=f"{ma}, you have successfully claimed "
                                                   f"**{item_name}** from the bazaar!")
            return

        if ocs.data[ma]["kk"] < int(chosen_item_ls[1]):
            await interaction.channel.send(content=f"You don't have enough Kjell Crowns to buy this, {ma}!")
            return

        ocs.data[ma]["kk"] -= int(chosen_item_ls[1])
        ocs.data[chosen_item_ls[2]]["kk"] += int(chosen_item_ls[1])
        del ocs.data["bazaar"][int(item_number) - 1]
        ocs.data[ma]["inv"].append(chosen_item_ls[0])

        item_name = cie.create_item_embed(chosen_item_ls[0], "ratio")[1]

        await interaction.channel.send(content=f"**{ma}**, you have successfully bought **{item_name}** from "
                               f"{chosen_item_ls[2]} for **{chosen_item_ls[1]}** {a_setup.kk}!")


class SellModal(dc.ui.Modal):
    def __init__(self, *args, **kwargs):
        super(SellModal, self).__init__(*args, **kwargs)
        self.add_item(dc.ui.InputText(label="Number to sell from your inventory", placeholder="ex.: 1"))
        self.add_item(dc.ui.InputText(label="Price to sell for", placeholder="ex.: 200"))

    async def callback(self, interaction):
        ma = interaction.user.mention.replace("!", "")
        ocs.check_user(ma)

        item_number = self.children[0].value
        price = self.children[1].value
        await interaction.response.edit_message(content=None)

        try:
            chosen_item = ocs.data[ma]["inv"][int(item_number) - 1]
            price = int(price)
        except (IndexError, ValueError, ValueError):
            await interaction.channel.send(content=f"Invalid item-number or price, {ma}!")
            return

        if price < 0:
            price = 250
        elif price > 10000:
            price = 10000

        ocs.data["bazaar"].append([chosen_item, price, ma])
        del ocs.data[ma]["inv"][int(item_number) - 1]

        item_name = cie.create_item_embed(chosen_item, "get a load of this ratio")[1]
        await interaction.channel.send(content=f"{ma}, you have successfully sold **{item_name}** for **{price}** "
                               f"{a_setup.kk} to the bazaar!")


class BazView(dc.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @dc.ui.button(style=dc.ButtonStyle.blurple, emoji="◀", custom_id="a_left", row=0)
    async def arrow_left_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        if not interaction.user == self.ctx.author:
            return
        await interaction.response.edit_message(content=None)

        embed_ls = interaction.message.embeds
        if embed_ls[0].title.split(" ")[0] == "**The":
            page, item_range = orabis.get_page_stuff("◀️", embed_ls)
            description, embed_title, footer = orabis.bazaar_requested(item_range, page)
            await orabis.create_and_send_embed(embed_title, description, footer, interaction, ma, self)
            return

        num = int(embed_ls[0].title.split(" ")[0].split("*")[2])
        orabis.disable_certain_children(num, self.children, len(ocs.data["bazaar"]), True)

        chosen_item = ocs.data["bazaar"][num - 2][0]
        embed_and_item_name = cie.create_item_embed(chosen_item, f"**{num - 1} - Bazaar-item**")
        await interaction.edit_original_response(embed=embed_and_item_name[0], view=self)

    @dc.ui.button(style=dc.ButtonStyle.blurple, emoji="▶", custom_id="a_right", row=0)
    async def arrow_right_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        if not interaction.user == self.ctx.author:
            return
        await interaction.response.edit_message(content=None)

        embed_ls = interaction.message.embeds
        if embed_ls[0].title.split(" ")[0] == "**The":
            page, item_range = orabis.get_page_stuff("▶", embed_ls)
            description, embed_title, footer = orabis.bazaar_requested(item_range, page)
            await orabis.create_and_send_embed(embed_title, description, footer, interaction, ma, self)
            return

        embed_ls = interaction.message.embeds
        num = int(embed_ls[0].title.split(" ")[0].split("*")[2])
        orabis.disable_certain_children(num, self.children, len(ocs.data["bazaar"]), False)

        chosen_item = ocs.data["bazaar"][num][0]
        embed_and_item_name = cie.create_item_embed(chosen_item, f"**{num + 1} - Bazaar-item**")
        await interaction.edit_original_response(embed=embed_and_item_name[0], view=self)

    @dc.ui.button(style=dc.ButtonStyle.blurple, emoji="🔄", custom_id="ccw", row=0)
    async def arrow_ccw_callback(self, button, interaction):
        await interaction.response.edit_message(content=None)
        ma = interaction.user.mention.replace("!", "")
        embed_ls = interaction.message.embeds
        page, item_range = orabis.get_page_stuff("🔄", embed_ls)
        description, embed_title, footer = orabis.bazaar_requested(item_range, page)
        await orabis.create_and_send_embed(embed_title, description, footer, interaction, ma, self)

    @dc.ui.button(style=dc.ButtonStyle.red, emoji="🌓", row=1)
    async def change_baz_mode_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        if not interaction.user == self.ctx.author:
            return

        button.emoji, in_view_mode = {"🌓": ["🌗", False], "🌗": ["🌓", True]}[button.emoji.name]
        if in_view_mode:
            await interaction.response.edit_message(content=None)
            for b in self.children:
                b.disabled = False
            description, embed_title, footer = orabis.bazaar_requested(0, 1)
            await orabis.create_and_send_embed(embed_title, description, footer, interaction, ma, self)
            return

        modal = BazModal(title="Number to start at", self_=self)
        await interaction.response.send_modal(modal)
        await interaction.edit_original_response(view=self)

    @dc.ui.button(style=dc.ButtonStyle.red, label="Get", row=1)
    async def get_callback(self, button, interaction):
        modal = GetModal(title="Buy or claim an item")
        await interaction.response.send_modal(modal)

    @dc.ui.button(style=dc.ButtonStyle.red, label="Sell", row=1)
    async def sell_callback(self, button, interaction):
        modal = SellModal(title="Sell an item")
        await interaction.response.send_modal(modal)


@a_setup.client.slash_command(description="Get the current bazaar", guild_ids=a_setup.guild_ids)
async def bazaar(ctx, starting_page: dc.Option(int, required=False, description="Page you want to start at")):
    await ctx.respond("Your message is on it's way...")
    ma = ctx.author.mention.replace("!", "")

    if not starting_page:
        starting_page = 1

    if starting_page < 1:
        starting_page = 1

    if not ocs.data["bazaar"]:
        description = "The bazaar is empty!"

    else:
        item_range = 25 * (starting_page - 1)
        description = []
        for d in range(item_range, item_range + 25):
            try:
                tb = ocs.data["bazaar"][d]
                description.append(f"**{d + 1}** - {cie.create_item_embed(tb[0], None)[1]} - "
                               f"{tb[1]} {a_setup.kk} - von {tb[2]}\n")
            except IndexError:
                break
        description = "".join(description)

    embed = dc.Embed(title="**The current bazaar**", colour=dc.Colour(ocs.data[ma]["color"]), description=description)
    embed.set_footer(text=f"Page {starting_page}")
    view = BazView(ctx)

    await ctx.edit(content=None, embed=embed, view=view)
