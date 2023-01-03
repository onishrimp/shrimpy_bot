import asyncio
import b_fight_base as fb
import b_views_fight as vf
import d_open_close_stuff as ocs
import a_setup
import datetime
import random


async def arrow_up(self, interaction, m):
    ma = interaction.user.mention.replace("!", "")
    fb.x_able_all_buttons(True, self.children, ma, m)
    await interaction.response.edit_message(view=self)
    if ma not in m:
        return

    fb.move_curser(False, m[ma])
    embed = fb.create_fight_message(ma, m[ma])

    fb.x_able_all_buttons(False, self.children, ma, m)
    await interaction.edit_original_response(embed=embed, view=self)


async def defend(self, interaction, m):
    ma = interaction.user.mention.replace("!", "")
    fb.x_able_all_buttons(True, self.children, ma, m)
    await interaction.response.edit_message(view=self)
    if ma not in m:
        return

    f = m[ma]
    if f.item_ls[f.curser_n][2] == "🛡️":  # removed shield by double-clicking
        f.item_ls[f.curser_n][2] = ""
        f.used_shields -= 1
    else:
        f.item_ls[f.curser_n][2] = "🛡️"  # now has a shield
        f.used_shields += 1  # used shields + 1
        fb.move_curser(True, f)

    embed = fb.create_fight_message(ma, m[ma])

    fb.x_able_all_buttons(False, self.children, ma, m)
    await interaction.edit_original_response(embed=embed, view=self)


async def end_turn(self, interaction):
    ma = interaction.user.mention.replace("!", "")
    fb.x_able_all_buttons(True, self.children, ma, vf.m_pve)
    await interaction.response.edit_message(view=self)

    m = vf.m_pve
    if ma not in m:
        return

    obj = m[ma]
    items = obj.item_ls

    # is the time up?
    tdelta = datetime.timedelta(hours=1)
    time_ends = obj.start_time + tdelta
    time_now = datetime.datetime.now()
    if time_ends < time_now:
        obj.curser_n = 10
        log = [f"🔆 You have **lost** the fight due to **inactivity**. 🔆", crown_shit(False, ma)]
        obj.log = "".join(log)
        embed = fb.create_fight_message(ma, m[ma])
        m.pop(ma)
        await interaction.edit_original_response(embed=embed, view=self)
        return

    # what will the bot do?
    available_opp_items = []
    available_own_items = []
    if obj.liberos_active[0] and obj.item_ls[0][1]:
        available_opp_items.append(0)
    if obj.liberos_active[1] and obj.item_ls[5][1]:
        available_own_items.append(5)

    for i in range(1, 5):
        if obj.item_ls[i][1]:
            available_opp_items.append(i)
    for i in range(6, 10):
        if obj.item_ls[i][1]:
            available_own_items.append(i)

    max_shields = round(len(available_opp_items) / 2)
    if max_shields:
        used_shields = random.choice([s for s in range(0, max_shields + 1)])
    else:
        used_shields = 0
    shield_users = []
    for i in range(0, used_shields):
        shield_users.append(random.choice(available_opp_items))
    for i in available_opp_items:
        if i in shield_users:
            obj.item_ls[i][2] = "🛡️"
        else:
            obj.item_ls[i][2] = "⚔️"
            obj.item_ls[i][3] = random.choice(available_own_items)

    # evaluate
    defending = []
    afk = []
    attacking = []
    fainted = []
    for i in range(0, 10):
        if i in range(0, 5):
            emoji_1 = "🟥"
            emoji_2 = "🟩"
        else:
            emoji_1 = "🟩"
            emoji_2 = "🟥"
        if items[i][2] == "🛡️":
            defending.append((i, emoji_1))
        elif items[i][2] == "⚔️":
            attacking.append((i, items[i][3], emoji_1, emoji_2))
        elif items[i][2] == "" and items[i][1]:
            afk.append((i, emoji_1))

    # make log and adjust the hp
    log = []
    for a in afk:
        log.append(f"**{a[1]} {obj.item_ls[a[0]][0][0]}** is just standing there... MENACINGLY\n")

    for d in defending:
        log.append(f"**{d[1]} {obj.item_ls[d[0]][0][0]}** is defending itself.\n")

    for f in attacking:
        if f[1] not in [x[0] for x in defending]:
            obj.item_ls[f[1]][0][1][1] -= obj.item_ls[f[0]][0][1][0]
            if obj.item_ls[f[1]][0][1][1] <= 0 and f[1] not in [x[0] for x in fainted]:
                fainted.append((f[1], f[3]))
            log.append(f"**{f[2]} {obj.item_ls[f[0]][0][0]}** attacked **{f[3]} {obj.item_ls[f[1]][0][0]}**.\n")
        else:
            log.append(f"**{f[2]} {obj.item_ls[f[0]][0][0]}** tried to attack **{f[3]} {obj.item_ls[f[1]][0][0]}**"
                       f", but it defended itself.\n")

    for u in fainted:
        log.append(f"**{u[1]} {obj.item_ls[u[0]][0][0]}** fainted.\n")
        obj.item_ls[u[0]][1] = False

    # activate liberos
    for i in range(0, 10):
        if not obj.item_ls[i][1] and i in range(0, 5) and not obj.liberos_active[0]:
            obj.liberos_active[0] = True
            log.append(f"**🟥 {obj.item_ls[0][0][0]}** joined the fight!\n")
        if not obj.item_ls[i][1] and i in range(5, 10) and not obj.liberos_active[1]:
            obj.liberos_active[1] = True
            log.append(f"**🟩 {obj.item_ls[5][0][0]}** joined the fight!\n")

    # reset all actions
    for i in range(0, 10):
        obj.item_ls[i][2] = ""
        obj.item_ls[i][3] = ""

    # update log
    obj.log = "".join(log)

    # check if everyone is dead so that the game ends
    game_ends = False
    winner = ""
    loser = ""
    crown_log_add = ""
    end_fight_message = ""
    for i in range(0, 10):
        if obj.item_ls[i][1]:
            break
        if i == 9:
            game_ends = True
            h_opp = 0
            for j in range(0, 5):
                h_opp += obj.item_ls[j][0][1][1]
            h_own = 0
            for j in range(5, 10):
                h_own += obj.item_ls[j][0][1][1]
            if h_own < h_opp:
                winner = obj.opponent
                loser = ma
                crown_log_add = crown_shit(False, ma)
            else:
                winner = ma
                loser = obj.opponent
                crown_log_add = crown_shit(True, ma)

            end_fight_message = f"\n🔆 The fight is over! It tied! But {winner} **dealt more/ equal** 🔆\n" \
                                f"🔆 damage than {loser} and therefore **won** the fight! 🔆 "
    if not game_ends:
        for i in range(0, 5):
            if obj.item_ls[i][1]:
                break
            if i == 4:
                game_ends = True
                winner = ma
                loser = obj.opponent
                crown_log_add = crown_shit(True, ma)
        for i in range(5, 10):
            if obj.item_ls[i][1]:
                break
            if i == 9:
                game_ends = True
                winner = obj.opponent
                loser = ma
                crown_log_add = crown_shit(False, ma)
        end_fight_message = f"\n🔆 The fight is over! {winner} has **won** the fight! 🔆"

    if game_ends:
        obj.curser_n = 10
        log.append(end_fight_message)
        log.append(crown_log_add)
        obj.log = "".join(log)
        embed = fb.create_fight_message(ma, m[ma])
        m.pop(ma)
        await interaction.channel.send(f"🔆 {winner} has just **won** a fight against {loser}! 🔆")
        await interaction.edit_original_response(embed=embed)
        return

    # time left info
    log.append(
        f"\n🕒 You have **{round((time_ends - time_now).seconds // 60)}** minutes left to finish the fight. 🕞")
    obj.log = "".join(log)

    # round + 1
    obj.round_n += 1

    # reset curser and shields
    obj.curser_n = 5
    fb.move_curser(True, m[ma])
    obj.used_shields = 0

    # finally
    embed = fb.create_fight_message(ma, m[ma])
    fb.x_able_all_buttons(False, self.children, ma, vf.m_pve)
    await interaction.edit_original_response(embed=embed, view=self)


async def end_turn_timer(ma, turn, rec_level):
    obj_own = vf.m_pvp[ma]
    obj_opp = vf.m_pvp[obj_own.opponent]

    if rec_level == 3:  # if someone doesn't join, even after 12 minutes, the fight is over and tied
        if ma in vf.fight_starts:
            if vf.fight_starts[ma] == "pvp":
                vf.fight_starts.pop(ma)
        if obj_own.opponent in vf.fight_starts:
            if vf.fight_starts[obj_own.opponent] == "pvp":
                vf.fight_starts.pop(obj_own.opponent)
        vf.m_pvp.pop(ma)
        vf.m_pvp.pop(obj_own.opponent)
        return

    for i in range(12):
        await asyncio.sleep(20)
        if not obj_own.round_n == turn:
            break
    else:
        if ma not in ending_turn:
            # if user didn't dp /fight yet, there is no self object, therefore message can't be reached
            # so the timer should start over again
            try:
                fb.x_able_all_buttons(True, obj_own.selff.children, ma, vf.m_pvp)
            except AttributeError:
                await end_turn_timer(ma, turn, rec_level + 1)
                return

        if obj_own.opponent not in ending_turn:
            # same here
            try:
                fb.x_able_all_buttons(True, obj_opp.selff.children, obj_own.opponent, vf.m_pvp)
            except AttributeError:
                await end_turn_timer(ma, turn, rec_level + 1)
                return
            await end_pvp_turn(obj_opp.selff, obj_own.opponent)

        if ma not in ending_turn:
            await end_pvp_turn(obj_own.selff, ma)


ending_turn = []


async def end_pvp_turn(self, ma):
    m = vf.m_pvp
    if ma not in m:
        return
    obj_own = m[ma]
    obj_opp = m[obj_own.opponent]

    await obj_own.cur_ctx.edit(view=self)

    if ma in ending_turn:
        return
    ending_turn.append(ma)

    obj_own.selff = self
    # did both press end_turn?
    if obj_own.opponent not in ending_turn:
        obj_own.log = "".join([obj_own.log, "\n**Waiting for opponent...**"])
        obj_own.curser_n = 11
        embed = fb.create_fight_message(ma, m[ma])
        await obj_own.cur_ctx.edit(embed=embed, view=self)
        return

    # EXAMPLE OPP: a: 0, b: 0 | c: 1, d: 2
    # EXAMPLE OWN: c: 0, d: 0 | a: 1, b: 2
    # both should have the information that a and c are 1 and b and d are 2
    for i in range(0, 5):
        obj_own.item_ls[i] = obj_opp.item_ls[i + 5].copy()
        obj_opp.item_ls[i] = obj_own.item_ls[i + 5].copy()

    # if item attacks, it should attack something 5 higher so that the attacked item stay's the same
    for i in range(0, 5):
        if obj_own.item_ls[i][2] == "⚔️":
            # if opponent was still on attack when the turn ended
            if obj_own.item_ls[i][3] == "":
                obj_own.item_ls[i][2] = ""
            else:
                obj_own.item_ls[i][3] += 5

    # evaluate
    defending = []
    afk = []
    attacking = []
    fainted = []
    for i in range(0, 10):
        if i in range(0, 5):
            emoji_1 = "🟥"
            emoji_2 = "🟩"
        else:
            emoji_1 = "🟩"
            emoji_2 = "🟥"
        if obj_own.item_ls[i][2] == "🛡️":
            defending.append((i, emoji_1))

        elif obj_own.item_ls[i][2] == "⚔️":
            if not obj_own.item_ls[i][3] == "":
                # if timer didn't end when user was on attack
                attacking.append((i, obj_own.item_ls[i][3], emoji_1, emoji_2))

        elif obj_own.item_ls[i][2] == "" and obj_own.item_ls[i][1]:
            afk.append((i, emoji_1))

    # make log and adjust the hp
    log = []
    for a in afk:
        log.append(f"**{a[1]} {obj_own.item_ls[a[0]][0][0]}** is just standing there... MENACINGLY\n")

    for d in defending:
        log.append(f"**{d[1]} {obj_own.item_ls[d[0]][0][0]}** is defending itself.\n")

    for f in attacking:
        if f[1] not in [x[0] for x in defending]:
            obj_own.item_ls[f[1]][0][1][1] -= obj_own.item_ls[f[0]][0][1][0]
            if obj_own.item_ls[f[1]][0][1][1] <= 0 and f[1] not in [x[0] for x in fainted]:
                fainted.append((f[1], f[3]))
            log.append(f"**{f[2]} {obj_own.item_ls[f[0]][0][0]}** attacked **{f[3]} {obj_own.item_ls[f[1]][0][0]}**.\n")
        else:
            log.append(
                f"**{f[2]} {obj_own.item_ls[f[0]][0][0]}** tried to attack **{f[3]} {obj_own.item_ls[f[1]][0][0]}**"
                f", but it defended itself.\n")

    # kill the fainted
    for u in fainted:
        log.append(f"**{u[1]} {obj_own.item_ls[u[0]][0][0]}** fainted.\n")
        obj_own.item_ls[u[0]][1] = False
        # it has to be plus or minus 5, depending on who is the own and who is opponent
        number_adder = 5
        if u[0] in range(5, 10):
            number_adder -= 10
        obj_opp.item_ls[u[0] + number_adder][1] = False

    # activate liberos
    for i in range(0, 10):
        if not obj_own.item_ls[i][1] and i in range(0, 5) and not obj_own.liberos_active[0]:
            obj_own.liberos_active[0] = True
            obj_opp.liberos_active[1] = True
            log.append(f"**🟥 {obj_own.item_ls[0][0][0]}** joined the fight!\n")
        if not obj_own.item_ls[i][1] and i in range(5, 10) and not obj_own.liberos_active[1]:
            obj_own.liberos_active[1] = True
            obj_opp.liberos_active[0] = True
            log.append(f"**🟩 {obj_own.item_ls[5][0][0]}** joined the fight!\n")

    # update log and change it for the opponent
    own_log = "".join(log)
    for i in range(len(log)):
        log[i] = log[i].replace("🟩", "red_box")
        log[i] = log[i].replace("🟥", "🟩")
        log[i] = log[i].replace("red_box", "🟥")
    opp_log = "".join(log)

    for obj in [obj_own, obj_opp]:
        # reset all actions
        for i in range(0, 10):
            obj.item_ls[i][2] = ""
            obj.item_ls[i][3] = ""

        # round + 1
        obj.round_n += 1

        # if obj was on attack, reset it
        obj.on_attack = False
        obj.selff.children[4].emoji = "⚔️"

        # reset curser and shields
        obj.curser_n = 5
        fb.move_curser(True, obj)
        obj.used_shields = 0

    # game ends?
    game_ends = False
    winner = ""
    loser = ""
    end_fight_message = ""
    for i in range(0, 10):
        if obj_own.item_ls[i][1]:
            break
        if i == 9:
            game_ends = True
            h_opp = 0
            for j in range(0, 5):
                h_opp += obj_own.item_ls[j][0][1][1]
            h_own = 0
            for j in range(5, 10):
                h_own += obj_own.item_ls[j][0][1][1]
            if h_own < h_opp:
                winner = obj_own.opponent
                loser = ma
            else:
                winner = ma
                loser = obj_own.opponent

            end_fight_message = f"\n🔆 The fight is over! It tied! But {winner} **dealt more** 🔆\n" \
                                f"🔆 damage than {loser} and therefore **won** the fight! 🔆 "
            if h_own == h_opp:
                winner = obj_own.opponent
                loser = ma
                end_fight_message = f"\n🔆 The fight is over! It tied! Both players **dealt equal** damage but " \
                                    f"{winner} 🔆\n🔆 endet his turn first and therefore **won** against {loser} ! 🔆 "

    # check if everyone is dead in one or both teams so that the game ends
    if not game_ends:
        for i in range(0, 5):
            if obj_own.item_ls[i][1]:
                break
            if i == 4:
                game_ends = True
                winner = ma
                loser = obj_own.opponent
        for i in range(5, 10):
            if obj_own.item_ls[i][1]:
                break
            if i == 9:
                game_ends = True
                winner = obj_own.opponent
                loser = ma
        end_fight_message = f"\n🔆 The fight is over! {winner} **has won** the fight! 🔆"

    # end the game
    if game_ends:
        obj_own.log = "".join([own_log, end_fight_message])
        obj_opp.log = "".join([opp_log, end_fight_message])
        for obj in [obj_own, obj_opp]:
            obj.curser_n = 10
            m.pop(obj.opponent)

        embed = fb.create_fight_message(obj_own.opponent, obj_opp)
        await obj_opp.cur_ctx.edit(embed=embed, view=obj_opp.selff)

        embed = fb.create_fight_message(ma, obj_own)
        await obj_own.cur_ctx.edit(embed=embed, view=obj_own.selff)

        rank_shit(loser, winner)
        await obj_own.cur_ctx.channel.send(f"🔆 {winner} has just **won** a fight against {loser}! 🔆")
        return

    # time left info, only if game is not over
    m4 = "\n🕒 You have **4** minutes to end your turn. 🕞"
    obj_own.log = "".join([own_log, m4])
    obj_opp.log = "".join([opp_log, m4])

    # delete opp from ending turn
    for i in ending_turn[:]:
        if i == obj_own.opponent:
            ending_turn.remove(i)
        elif i == ma:
            ending_turn.remove(i)

    # finally
    embed = fb.create_fight_message(obj_own.opponent, obj_opp)
    fb.x_able_all_buttons(False, obj_opp.selff.children.copy(), obj_own.opponent, vf.m_pvp)
    await obj_opp.cur_ctx.edit(embed=embed, view=obj_opp.selff)

    embed = fb.create_fight_message(ma, obj_own)
    fb.x_able_all_buttons(False, self.children, ma, vf.m_pvp)
    await obj_own.cur_ctx.edit(embed=embed, view=obj_own.selff)

    # start a new timer
    await end_turn_timer(ma, obj_own.round_n, 0)


async def arrow_down(self, interaction, m):
    ma = interaction.user.mention.replace("!", "")
    fb.x_able_all_buttons(True, self.children, ma, m)
    await interaction.response.edit_message(view=self)
    if ma not in m:
        return

    fb.move_curser(True, m[ma])
    embed = fb.create_fight_message(ma, m[ma])

    fb.x_able_all_buttons(False, self.children, ma, m)
    await interaction.edit_original_response(embed=embed, view=self)


async def attack(self, button, interaction, m):
    ma = interaction.user.mention.replace("!", "")
    fb.x_able_all_buttons(True, self.children, ma, m)
    await interaction.response.edit_message(view=self)
    if ma not in m:
        return

    obj = m[ma]

    if obj.item_ls[obj.curser_n][2] == "⚔️":  # remove attack
        obj.item_ls[obj.curser_n][2] = ""
        remaining_emojis = [i for i in obj.item_ls[obj.item_ls[obj.curser_n][3]][2]]  # what am I doing here
        del remaining_emojis[0]
        obj.item_ls[obj.item_ls[obj.curser_n][3]][2] = "".join(remaining_emojis)
        obj.item_ls[obj.curser_n][3] = []

    elif obj.on_attack:  # already in attack
        for i in range(len(obj.item_ls)):
            if obj.item_ls[i][2] == "⚔️" and not obj.item_ls[i][3] in range(0, 10):  # who is attacking
                obj.item_ls[i][3] = obj.curser_n  # give the attack the number of who he is attacking
        obj.item_ls[obj.curser_n][2] = "".join([obj.item_ls[obj.curser_n][2], "🏹"])
        obj.curser_n = 5
        fb.move_curser(True, m[ma])
        button.emoji = "⚔️"
        obj.on_attack = False

    else:  # starts attack
        obj.item_ls[obj.curser_n][2] = "⚔️"
        button.emoji = "🏹"  # bow emoji
        obj.on_attack = True
        if obj.liberos_active[0]:  # these are -1 and 0 so that I can use move_curser() which will be this + 1
            obj.curser_n = -1
        else:
            obj.curser_n = 0
        fb.move_curser(True, m[ma])

    embed = fb.create_fight_message(ma, m[ma])

    fb.x_able_all_buttons(False, self.children, ma, m)
    await interaction.edit_original_response(embed=embed, view=self)


async def clear_log(self, interaction, m):
    ma = interaction.user.mention.replace("!", "")
    fb.x_able_all_buttons(True, self.children, ma, m)
    await interaction.response.edit_message(view=self)
    if ma not in m:
        return

    m[ma].log = ""
    embed = fb.create_fight_message(ma, m[ma])

    fb.x_able_all_buttons(False, self.children, ma, m)
    await interaction.edit_original_response(embed=embed, view=self)


def crown_shit(ma_won, ma):  # I'm losing my mind
    # d_matches saves the date if you did a fight on that day
    m_started_at = str(vf.m_pve[ma].start_time.date())
    ocs.check_user(ma)

    if ocs.data[ma]["daily_matches"] == m_started_at:
        return ""

    ocs.data[ma]["daily_matches"] = m_started_at

    if ma_won:
        ocs.data[ma]["kk"] += 20
        return f"\n🔆 You have **won** the first fight of the day and therefore received 🔆\n🔆 **20** {a_setup.kk}. 🔆"

    else:
        return f"\n🔆 You have **lost** the first fight of the day and therefore did 🔆\n🔆 **not** receive your **20** " \
               f"{a_setup.kk}. 🔆"


def rank_shit(loser, winner):
    ocs.data[loser]["rank"] -= 20
    ocs.data[winner]["rank"] += 20
    if ocs.data[loser]["rank"] < 0:
        ocs.data[loser]["rank"] = 0
