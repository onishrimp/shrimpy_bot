import discord as dc
import b_fight_buttons as fbt
import b_fight_base as fb
import d_open_close_stuff as ocs
import datetime
import b_generate_random_items as gri
import a_setup


m_pve = {}
pve_items = {}
m_pvp = {}
pvp_items = {}
queue = {}
fight_starts = {}


def check_items(item_numbers, embed, ma):
    err = False

    try:
        for i in item_numbers:
            _ = ocs.data[ma]["inv"][int(i) - 1]
    except (IndexError, ValueError):
        embed.description = "🌐 Invalid item-number/s! 🌐"
        err = True
    except KeyError:
        embed.description = "🌐 You need **items** to fight, Try to use **/daily** and **/gamble**! 🌐"
        err = True

    for n in range(0, 5):
        same_count = 0
        for i in range(0, 5):
            try:
                if item_numbers[n] == item_numbers[i]:
                    same_count += 1
            except IndexError:
                embed.description = "🌐 You need 5 items to fight! 🌐"
                err = True
            if same_count == 2:
                embed.description = "🌐 You can't use the same item twice! 🌐"
                err = True
    return err


def create_item_ls(own_items, opp_items):
    item_ls = []
    for d in range(0, 10):
        if len(item_ls) <= 4:
            # Item name, Alive_bool, Action, Attacking who
            item_ls.append([[opp_items[d][0], [opp_items[d][1][0], opp_items[d][1][1]]], True, "", ""])
        else:
            item_ls.append([[own_items[d - 5][0], [own_items[d - 5][1][0], own_items[d - 5][1][1]]], True, "", ""])
    return item_ls


async def pve_fight_modal(self, interaction):
    ma = interaction.user.mention.replace("!", "")
    embed = interaction.message.embeds[0]
    item_numbers = [self.children[0].value, *self.children[1].value.split(" ")]

    if not check_items(item_numbers, embed, ma):
        m_pve[ma] = item_numbers
        fight_starts[ma] = "pve"
        embed.description = "🌐 You can now use **/fight** to join your PVE fight! 🌐\n" \
                            "🌐 You have **60 minutes** to finish it. 🌐"

        m_pve.pop(ma)

        own_items = []
        for i in item_numbers:
            own_items.append(ocs.data[ma]["inv"][int(i) - 1])

        opp_items = gri.gri([10, 5, 50, 35, 5], 5, 0)
        item_ls = create_item_ls(own_items, opp_items)

        log = "🕒 You have **60** minutes to finish the fight. 🕞"
        start_time = datetime.datetime.now()
        f = Fight(item_ls, 1, ma, 6, 0, [False, False], log, False, start_time, a_setup.bot_id, None, None)
        m_pve[ma] = f

    await interaction.response.edit_message(embed=embed)


async def pvp_fight_modal(self, interaction):
    ma = interaction.user.mention.replace("!", "")
    embed = interaction.message.embeds[0]
    item_numbers = [self.children[0].value, *self.children[1].value.split(" ")]

    if check_items(item_numbers, embed, ma):
        await interaction.response.edit_message(embed=embed)
        return

    embed.description = "🌐 You have **joined the queue**. Wait for a message to appear! 🌐"

    if not queue:
        queue[ma] = item_numbers
    else:
        for k in queue:  # if someone is in queue fight will start
            fight_starts[k] = "pvp"
            fight_starts[ma] = "pvp"

            log = "🕒 You have **4** minutes to end your turn. 🕞"

            ma_items = []
            k_items = []

            for i in item_numbers:
                ma_items.append(ocs.data[ma]["inv"][int(i) - 1])
            for i in queue[k]:
                k_items.append(ocs.data[k]["inv"][int(i) - 1])

            start_time = datetime.datetime.now()
            f_ma = Fight(create_item_ls(ma_items, k_items), 1, ma, 6, 0, [False, False], log,
                         False, start_time, k, None, None)
            f_op = Fight(create_item_ls(k_items, ma_items), 1, k, 6, 0, [False, False], log,
                         False, start_time, ma, None, None)

            m_pvp[ma] = f_ma
            m_pvp[k] = f_op
            queue.pop(k)

            await interaction.channel.send(f"🔆 A fight has begun! {ma} is fighting against {k}! "
                                           f"Both of you, do **/fight**! 🔆")
            break

    await interaction.response.edit_message(embed=embed)
    if ma in m_pvp:
        obj_own = m_pvp[ma]
        await fbt.end_turn_timer(ma, obj_own.round_n, 0)


class FightModal(dc.ui.Modal):
    def __init__(self, pvp_bool, *args, **kwargs):
        super(FightModal, self).__init__(*args, **kwargs)
        self.pvp_bool = pvp_bool

        self.add_item(dc.ui.InputText(label="Liberos Number", placeholder="ex.: 1"))
        self.add_item(dc.ui.InputText(label=f"Other 4 items", placeholder=f"ex.: 2 3 4 5"))

    async def callback(self, interaction):
        # pvp_bool is something you give the class so that it knows if pvp or pve is requested, with that I can
        # save me creating this class two times
        if not self.pvp_bool:
            await pve_fight_modal(self, interaction)
        else:  # elif pvp_bool
            await pvp_fight_modal(self, interaction)


class PreFightView(dc.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @dc.ui.button(style=dc.ButtonStyle.grey, label="PVE ➡️", row=0, disabled=True)
    async def useless_1(self, button, interaction):
        pass

    @dc.ui.button(style=dc.ButtonStyle.grey, label="PVP ➡️", row=1, disabled=True)
    async def useless_2(self, button, interaction):
        pass

    @dc.ui.button(style=dc.ButtonStyle.green, label="Start", custom_id="start_pve", row=0)
    async def start_pve_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        embed = interaction.message.embeds[0]

        if ma in m_pve:
            embed.description = "🌐 There is already a PVE fight running! Try **rejoining** it! 🌐"
            await interaction.response.edit_message(embed=embed)
            return

        if ma in fight_starts:
            embed.description = "🌐 Join your other fight first with **/fight**! 🌐"
            await interaction.response.edit_message(embed=embed)
            return

        modal = FightModal(title="Items for fight", pvp_bool=False)
        await interaction.response.send_modal(modal)

    @dc.ui.button(style=dc.ButtonStyle.blurple, label="Rejoin", custom_id="rj_pve", row=0)
    async def rj_pve_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        embed = interaction.message.embeds[0]

        if ma in fight_starts:
            embed.description = "🌐 Join your other fight first with **/fight**! 🌐"
            await interaction.response.edit_message(embed=embed)
            return

        if ma not in m_pve:
            embed.description = "🌐 There isn't a **running fight**. Start one first! 🌐"
            await interaction.response.edit_message(embed=embed)
            return

        embed.description = "🌐 You can now use **/fight** to rejoin your PVE fight! 🌐"
        fight_starts[ma] = "pve"
        await interaction.response.edit_message(embed=embed)

    @dc.ui.button(style=dc.ButtonStyle.red, label="Surrender️", row=0)
    async def sur_pve_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        embed = interaction.message.embeds[0]

        if ma not in m_pve:
            embed.description = "🌐 There isn't a running fight. Start one first! 🌐"
            await interaction.response.edit_message(embed=embed)
            return

        embed.description = "🌐 You have successfully **surrendered**. 🌐"
        m_pve.pop(ma)
        if ma in fight_starts:
            fight_starts.pop(ma)
        ocs.data[ma]["daily_matches"] = str(datetime.date.today())

        await interaction.channel.send(f"{ma} has **surrendered** in a PVE fight.")
        await interaction.response.edit_message(embed=embed)

    @dc.ui.button(style=dc.ButtonStyle.green, label="Queue", custom_id="start_pvp", row=1)
    async def start_pvp_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        embed = interaction.message.embeds[0]

        if ma in m_pvp:
            embed.description = "🌐 There is already a PVP fight running! Try **rejoining** it! 🌐"

        elif ma in queue:
            embed.description = "🌐 You have **left the queue**. 🌐"
            queue.pop(ma)

        elif ma in fight_starts:
            embed.description = "🌐 Join your other fight first with **/fight**! 🌐"
            await interaction.response.edit_message(embed=embed)
            return

        else:
            modal = FightModal(title="Items for the fight", pvp_bool=True)
            await interaction.response.send_modal(modal)
            return

        await interaction.response.edit_message(embed=embed)

    @dc.ui.button(style=dc.ButtonStyle.blurple, label="Rejoin", custom_id="rj_pvp", row=1)
    async def rj_pvp_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        embed = interaction.message.embeds[0]

        if ma not in m_pvp:
            embed.description = "🌐 There isn't a running fight. Start one first! 🌐"
            await interaction.response.edit_message(embed=embed)
            return

        embed.description = "🌐 You can now use **/fight** to rejoin your PVP fight! 🌐"
        fight_starts[ma] = "pvp"
        await interaction.response.edit_message(embed=embed)

    @dc.ui.button(style=dc.ButtonStyle.red, label="Surrender️", row=1)
    async def sur_pvp_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        embed = interaction.message.embeds[0]

        if ma not in m_pvp:
            embed.description = "🌐 There isn't a running fight. Start one first! 🌐"
            await interaction.response.edit_message(embed=embed)
            return

        embed.description = "🌐 You have successfully surrendered. 🌐"
        opp = m_pvp[ma].opponent

        m_pvp.pop(opp)
        m_pvp.pop(ma)
        if ma in fight_starts:
            fight_starts.pop(ma)
            fight_starts.pop(opp)
        fbt.rank_shit(ma, opp)

        await interaction.response.edit_message(embed=embed)
        await interaction.message.channel.send(f"🔆 {ma} has **surrendered** in a fight against {opp} 🔆")

    async def get_button(self, custom_id):
        for b in self.children:
            if b.custom_id == custom_id:  # pycharm and the pycord docs say attribute doesn't exist, but it does L
                return b


class Fight:
    def __init__(self, item_ls, round_n, ma, curser_n, used_shields, liberos_active, log, on_attack, start_time,
                 opponent, cur_ctx, selff):
        self.item_ls = item_ls
        self.round_n = round_n
        self.ma = ma
        self.curser_n = curser_n
        self.used_shields = used_shields
        self.liberos_active = liberos_active
        self.log = log
        self.on_attack = on_attack
        self.start_time = start_time
        self.opponent = opponent
        self.cur_ctx = cur_ctx
        self.selff = selff


class FightViewPVE(dc.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # super(FightViewPVE, self).__init__(disable_on_timeout=True)

    @dc.ui.button(style=dc.ButtonStyle.blurple, emoji="⬆️", custom_id="a_up", row=0)
    async def arrow_up_callback(self, button, interaction):
        await fbt.arrow_up(self, interaction, m_pve)

    @dc.ui.button(style=dc.ButtonStyle.red, emoji="🛡️", custom_id="defend", row=0)
    async def defend_callback(self, button, interaction):
        await fbt.defend(self, interaction, m_pve)

    @dc.ui.button(style=dc.ButtonStyle.green, label="END TURN", custom_id="end_turn", row=0)
    async def end_turn_callback(self, button, interaction):
        await fbt.end_turn(self, interaction)

    @dc.ui.button(style=dc.ButtonStyle.blurple, emoji="⬇️", custom_id="a_down", row=1)
    async def arrow_down_callback(self, button, interaction):
        await fbt.arrow_down(self, interaction, m_pve)

    @dc.ui.button(style=dc.ButtonStyle.red, emoji="⚔️", custom_id="attack", row=1)
    async def attack_callback(self, button, interaction):
        await fbt.attack(self, button, interaction, m_pve)

    @dc.ui.button(style=dc.ButtonStyle.green, label="CLEAR LOG", custom_id="clear_log", row=1)
    async def clear_log_callback(self, button, interaction):
        await fbt.clear_log(self, interaction, m_pve)


class FightViewPVP(dc.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @dc.ui.button(style=dc.ButtonStyle.blurple, emoji="⬆️", custom_id="a_up", row=0)
    async def arrow_up_callback(self, button, interaction):
        await fbt.arrow_up(self, interaction, m_pvp)

    @dc.ui.button(style=dc.ButtonStyle.red, emoji="🛡️", custom_id="defend", row=0)
    async def defend_callback(self, button, interaction):
        await fbt.defend(self, interaction, m_pvp)

    @dc.ui.button(style=dc.ButtonStyle.green, label="END TURN", custom_id="end_turn", row=0)
    async def end_turn_callback(self, button, interaction):
        ma = interaction.user.mention.replace("!", "")
        fb.x_able_all_buttons(True, self.children, ma, m_pvp)
        await interaction.response.edit_message(view=self)
        await fbt.end_pvp_turn(self, ma)

    @dc.ui.button(style=dc.ButtonStyle.blurple, emoji="⬇️", custom_id="a_down", row=1)
    async def arrow_down_callback(self, button, interaction):
        await fbt.arrow_down(self, interaction, m_pvp)

    @dc.ui.button(style=dc.ButtonStyle.red, emoji="⚔️", custom_id="attack", row=1)
    async def attack_callback(self, button, interaction):
        await fbt.attack(self, button, interaction, m_pvp)

    @dc.ui.button(style=dc.ButtonStyle.green, label="CLEAR LOG", custom_id="clear_log", row=1)
    async def clear_log_callback(self, button, interaction):
        await fbt.clear_log(self, interaction, m_pvp)
