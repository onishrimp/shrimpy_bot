import b_create_item_embeds as cie
import discord as dc


# item_ls = [[raw_item_name, [attack, hp]], alive_bool, status], ...], first your opp 5 then your own 5
# status = one or more emojis of being attacked, attacking or defending
# first one in the list is always the libero
# first dino by curser_number is always [0]
# liberos active, opp first, then own
# round_log typed string
def create_fight_message(ma, f):
    s_1 = ":green_square:"
    s_2 = ":red_square:"

    content_ls = [
        f"**{ma} is team {s_1} !**",
        f"**{f.opponent} is team {s_2} !**",
        f.log,
        s_2 * 12,
        "**Name :id:  | Attack :crossed_swords: | HP :heart_decoration: **",
        s_1 * 12,
    ]

    own_item_ls = []
    opp_item_ls = []
    for d in range(len(f.item_ls)):
        if len(opp_item_ls) <= 4:
            opp_item_ls.append(f.item_ls[d])
        else:
            own_item_ls.append(f.item_ls[d])

    def create_dino_string(items, aic):
        output = []

        name_len = 0
        for i in items:
            if name_len < len(i[0][0]):
                name_len = len(i[0][0])

        if aic == 0:
            lib = 0
        else:
            lib = 1

        for i in items:
            item_name = cie.create_item_embed(i[0], None)[1]

            line_breaks = "\n"
            if len(output) == 0 and not f.liberos_active[lib]:
                line_breaks = "\n\n"

            emojis = i[2]

            spaces = "ㅤ" * round(((name_len - len(i[0][0])) / 2) + 1)  # using an invisible sign
            if aic == f.curser_n:
                output.append(f"**{item_name}{spaces}|  {i[0][1][0]}  |  {i[0][1][1]}  {emojis}  ⬅️**{line_breaks}")
            elif not i[1]:
                output.append(f"~~{item_name}{spaces}|  {i[0][1][0]}  |  {i[0][1][1]}~~  ❌{line_breaks}")
            else:
                output.append(f"{item_name}{spaces}|  {i[0][1][0]}  |  {i[0][1][1]}  {emojis}{line_breaks}")
            aic += 1

        output = "".join(output)
        return output, aic

    all_item_count = 0
    content_ls.append(create_dino_string(opp_item_ls, all_item_count)[0])
    all_item_count = create_dino_string(opp_item_ls, all_item_count)[1]
    content_ls.append(create_dino_string(own_item_ls, all_item_count)[0])

    mc = f"{content_ls[0]}\n" \
         f"{content_ls[1]}\n\n" \
         f"{content_ls[2]}\n\n" \
         f"{content_ls[3]}\n\n" \
         f"{content_ls[4]}\n\n" \
         f"{content_ls[-2]}\n" \
         f"{content_ls[3]}\n\n\n" \
         f"{content_ls[5]}\n\n" \
         f"{content_ls[4]}\n\n" \
         f"{content_ls[-1]}\n" \
         f"{content_ls[5]}"

    embed = dc.Embed(title=f"Round {f.round_n}", colour=dc.Colour(0x485885), description=mc)

    return embed


def disable_certain_buttons(ma, m):
    disabled_buttons = []
    obj = m[ma]

    if not obj.log:
        disabled_buttons.append("clear_log")

    if obj.on_attack:
        disabled_buttons.append("defend")
        disabled_buttons.append("end_turn")

    action = obj.item_ls[obj.curser_n][2]

    if action == "🛡️":
        disabled_buttons.append("attack")

    if action == "⚔️":
        disabled_buttons.append("defend")

    dinos_alive = 5
    for i in range(5, 10):
        if not obj.item_ls[i][1]:
            dinos_alive -= 1
    if obj.used_shields >= round(dinos_alive / 2):
        if not action == "🛡️":
            disabled_buttons.append("defend")

    return disabled_buttons


def x_able_all_buttons(disable, children, message_author, m):
    if disable:
        for b in [x for x in children]:
            b.disabled = True

    else:
        for b in children:
            if b.custom_id not in disable_certain_buttons(message_author, m):
                b.disabled = False


def move_curser(down, f):  # I hate this
    start_curser = f.curser_n
    opp_field = False
    if f.curser_n in range(0, 5):
        opp_field = True

    if down:  # move down
        start_check = 6
        imp_libero = 1
        end = 10
        if opp_field:
            start_check = 1
            imp_libero = 0
            end = 5
        for i in range(f.curser_n + 1, end):  # first non-dead item should get the curser number
            if f.item_ls[i][1]:
                f.curser_n = i
                break
        if f.liberos_active[imp_libero]:  # if libero active
            start_check -= 1
        if f.curser_n == start_curser:  # if everyone down was dead so that the curser did not change
            for i in range(start_check, end):
                if f.item_ls[i][1]:
                    f.curser_n = i
                    break

    else:  # move up
        start = 6
        imp_libero = 1
        end = 10
        if opp_field:
            start = 1
            imp_libero = 0
            end = 5
        if f.liberos_active[imp_libero]:  # if libero active
            start -= 1
        for i in range(start, f.curser_n)[::-1]:  # first non-dead item should get the curser number
            if f.item_ls[i][1]:
                f.curser_n = i
                break
        if f.curser_n == start_curser:  # if everyone down was dead so that the curser did not change
            for i in range(start, end)[::-1]:
                if f.item_ls[i][1]:
                    f.curser_n = i
                    break
