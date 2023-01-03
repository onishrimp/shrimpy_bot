import a_setup
import b_create_item_embeds as cie
import discord as dc
import d_open_close_stuff as ocs
import b_ora_baz_inv_sho as orabis


# @a_setup.client.slash_command(name="view-inventory-item", description="Take a look at one of your items",
#                               guild_ids=a_setup.guild_ids)
# async def view_inventory_item(ctx, item_number: dc.Option(int)):
#     await ctx.respond("Your message is on it's way...")
#
#     ma = ctx.author.mention.replace("!", "")
#     printed_author = csa.get_printed_author_name(ctx.author)
#     ocs.check_user(ma)
#
#     try:
#         chosen_item = ocs.data[ma]["inv"][int(item_number) - 1]  # str name of the item
#     except IndexError:
#         await ctx.edit(content=f"Invalid item-number **{printed_author}**!")
#         return
#
#     embed_and_item_name = cde.create_item_embed(chosen_item, f"**Property of {ctx.author.name}**")
#     await ctx.edit(content=None, embed=embed_and_item_name[0])


class InvModal(dc.ui.Modal):
    def __init__(self, self_, *args, **kwargs):
        super(InvModal, self).__init__(*args, **kwargs)
        self.add_item(dc.ui.InputText(label="Starting Number", placeholder="ex.: 1"))
        self.self_ = self_

    async def callback(self, interaction):
        ma = interaction.user.mention.replace("!", "")
        if not ocs.data[ma]["inv"]:
            return

        item_number = self.children[0].value
        try:
            chosen_item = ocs.data[ma]["inv"][int(item_number) - 1]
        except (IndexError, ValueError, ValueError):
            chosen_item = ocs.data[ma]["inv"][0]

        item_number = int(item_number)
        disables = ["ccw"]
        if item_number == 1:
            disables.append("a_left")
        if item_number == len(ocs.data[ma]["inv"]):
            disables.append("a_right")
        for b in self.self_.children:
            if b.custom_id in disables:
                b.disabled = True

        embed_and_item_name = cie.create_item_embed(
            chosen_item, f"**{item_number} - Property of {interaction.user.name}**")
        await interaction.response.edit_message(embed=embed_and_item_name[0], view=self.self_)


class InvView(dc.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    @dc.ui.button(style=dc.ButtonStyle.grey, emoji="◀", custom_id="a_left")
    async def arrow_left_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        if not interaction.user == self.ctx.author:
            return
        await interaction.response.edit_message(content=None)

        embed_ls = interaction.message.embeds
        if embed_ls[0].title.split(" ")[0] == "**Inventory":
            page, item_range = orabis.get_page_stuff("◀️", embed_ls)
            description, embed_title, footer = orabis.inventory_requested(item_range, ma, page, interaction)
            await orabis.create_and_send_embed(embed_title, description, footer, interaction, ma, self)
            return

        num = int(embed_ls[0].title.split(" ")[0].split("*")[2])
        orabis.disable_certain_children(num, self.children, len(ocs.data[ma]["inv"]), True)

        try:
            chosen_item = ocs.data[ma]["inv"][num - 2]
        except IndexError:
            return
        embed_and_item_name = cie.create_item_embed(chosen_item, f"**{num - 1} - Property of {interaction.user.name}**")
        await interaction.edit_original_response(embed=embed_and_item_name[0], view=self)

    @dc.ui.button(style=dc.ButtonStyle.grey, emoji="▶", custom_id="a_right")
    async def arrow_right_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        if not interaction.user == self.ctx.author:
            return
        await interaction.response.edit_message(content=None)

        embed_ls = interaction.message.embeds
        if embed_ls[0].title.split(" ")[0] == "**Inventory":
            page, item_range = orabis.get_page_stuff("▶️️️", embed_ls)
            description, embed_title, footer = orabis.inventory_requested(item_range, ma, page, interaction)
            await orabis.create_and_send_embed(embed_title, description, footer, interaction, ma, self)
            return

        num = int(embed_ls[0].title.split(" ")[0].split("*")[2])
        orabis.disable_certain_children(num, self.children, len(ocs.data[ma]["inv"]), False)

        try:
            chosen_item = ocs.data[ma]["inv"][num]
        except IndexError:
            return
        embed_and_item_name = cie.create_item_embed(chosen_item, f"**{num + 1} - Property of {interaction.user.name}**")
        await interaction.edit_original_response(embed=embed_and_item_name[0], view=self)

    @dc.ui.button(style=dc.ButtonStyle.grey, emoji="🔄", custom_id="ccw")
    async def arrow_ccw_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        if not interaction.user == self.ctx.author:
            return
        await interaction.response.edit_message(content=None)

        embed_ls = interaction.message.embeds
        page, item_range = orabis.get_page_stuff("🔄", embed_ls)
        description, embed_title, footer = orabis.inventory_requested(item_range, ma, page, interaction)
        await orabis.create_and_send_embed(embed_title, description, footer, interaction, ma, self)

    @dc.ui.button(style=dc.ButtonStyle.grey, emoji="🌓")
    async def change_inv_mode_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        if not interaction.user == self.ctx.author:
            return

        button.emoji, in_view_mode = {"🌓": ["🌗", False], "🌗": ["🌓", True]}[button.emoji.name]
        if in_view_mode:
            await interaction.response.edit_message(content=None)
            for b in self.children:
                b.disabled = False
            description, embed_title, footer = orabis.inventory_requested(0, ma, 1, interaction)
            await orabis.create_and_send_embed(embed_title, description, footer, interaction, ma, self)
            return

        modal = InvModal(title="Number to start at", self_=self)
        await interaction.response.send_modal(modal)


@a_setup.client.slash_command(description="Take a look at your inventory", guild_ids=a_setup.guild_ids)
async def inventory(ctx, starting_page: dc.Option(int, required=False, description="The page you wish to start at")):
    await ctx.respond(content="Your message is on it's way...")

    ma = ctx.author.mention.replace("!", "")
    ocs.check_user(ma)

    if not starting_page:
        starting_page = 1

    if starting_page < 1:
        starting_page = 1

    if not ocs.data[ma]["inv"]:
        description = "Your inventory is empty!"

    else:
        item_range = 25 * (starting_page - 1)
        description = []
        for d in range(item_range, item_range + 25):
            try:
                description.append(f"**{d + 1}** - {cie.create_item_embed(ocs.data[ma]['inv'][d], None)[1]}\n")
            except IndexError:
                break
        description = "".join(description)

        if description == "":
            description = "There is nothing on this page!"

    embed = dc.Embed(title=f"**Inventory of {ctx.author.name}**", colour=dc.Colour(ocs.data[ma]["color"]),
                     description=description)
    embed.set_footer(text=f"Page {starting_page}")
    view = InvView(ctx)
    await ctx.edit(content=None, embed=embed, view=view)


class SortView(dc.ui.View):
    @dc.ui.select(
        placeholder="Choose a sorting order!",
        min_values=1,
        max_values=1,
        options=[
            dc.SelectOption(
                label="Alphabetically Descending",
                description="A B C D"
            ),
            dc.SelectOption(
                label="Alphabetically Ascending",
                description="D C B A"
            ),
            dc.SelectOption(
                label="By Rarity Descending",
                description="Legendary Epic Common"
            ),
            dc.SelectOption(
                label="By Rarity Ascending",
                description="Common Epic Legendary"
            ),
            dc.SelectOption(
                label="By Stats Descending",
                description="100 50 20"
            ),
            dc.SelectOption(
                label="By Stats Ascending",
                description="20 50 100"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        ma = interaction.user.mention.replace("!", "")

        inv = ocs.data[ma]["inv"].copy()
        items = ocs.open_items()
        rarity_dict = {"common": [], "uncommon": [], "rare": [], "epic": [], "legendary": [], "specialrank": []}

        # sort by rarity
        for item in inv:
            rarity_dict[items[item[0]][0]].append(item)

        output = []
        select_value_ls = select.values[0].split(" ")

        # sort alphabetically
        if select.values[0] == "Alphabetically Descending":
            output = sorted(sorted(inv, key=lambda j: j[1][0] * j[1][1], reverse=True), key=lambda i: i[0].lower())
        elif select.values[0] == "Alphabetically Ascending":
            output = sorted(sorted(inv, key=lambda j: j[1][0] * j[1][1], reverse=True), key=lambda i: i[0].lower(),
                            reverse=True)

        # sort by rarity
        elif select_value_ls[1] == "Rarity":
            for _, v in rarity_dict.items():
                if v:
                    output.append(sorted(sorted(v, key=lambda j: j[1][0] * j[1][1], reverse=True), key=lambda i: i[0].
                                         lower()))
            if select_value_ls[2] == "Descending":
                output = output[::-1]
            output = [x for subls in output for x in subls]

        # sort by multiplied stats
        elif select_value_ls[1] == "Stats":
            output = sorted(inv, key=lambda j: j[1][0] * j[1][1], reverse=True)
            if select_value_ls[2] == "Ascending":
                output = output[::-1]

        ocs.data[ma]["inv"] = output
        await interaction.response.send_message(f"{ma} you have **successfully** sorted "
                                                f"your inventory ***{select.values[0]}***.")


@a_setup.client.slash_command(name="sort-inventory", description="Sort your inventory!", guild_ids=a_setup.guild_ids)
async def sort_inventory(ctx):
    await ctx.respond("🧑‍🏫 **Choose** how you would like to **sort your inventory**! 🧑‍🏫", view=SortView())


@a_setup.client.slash_command(name="change-embed-colors", description="Change the color of your embeds!",
                              guild_ids=a_setup.guild_ids)
async def change_embed_colors(ctx, hex_color: dc.Option(description="Color in a Hexadecimal number")):
    ma = ctx.author.mention.replace("!", "")
    await ctx.respond("Your message is on it's way...", ephemeral=True)

    hex_int = int(hex_color, 16)
    if hex_int > 16777215:
        await ctx.edit(content="That's not a hex color. Example: 485885 or 5F1841")
        return

    ocs.data[ma]["color"] = hex_int
    await ctx.edit(content=f"You have **successfully changed** the color of your **inventory** to #{hex_color}")
