import a_setup
import b_fight_base as fb
import b_fight_buttons as fbt
import b_community_server_active as csa
import b_views_fight as vf
import d_open_close_stuff as ocs
import discord as dc


@a_setup.client.slash_command(description="Fightingggggg", guild_ids=a_setup.guild_ids)
async def fight(ctx):
    ma = ctx.author.mention.replace("!", "")
    printed_author = csa.get_printed_author_name(ctx.author)
    await ctx.respond(f"Your message is on it's way...", ephemeral=True)

    if ma not in vf.fight_starts:
        await ctx.edit(content=f"Choose what you want to do with **/fight-menu** first, **{printed_author}**!")
        return

    fight_id = vf.fight_starts[ma]

    if fight_id == "pve":
        vf.m_pve[ma].cur_ctx = ctx
        embed = fb.create_fight_message(ma, vf.m_pve[ma])
        view = vf.FightViewPVE()
        fb.x_able_all_buttons(True, view.children, ma, vf.m_pve)
        fb.x_able_all_buttons(False, view.children, ma, vf.m_pve)

    else:  # elif fight_id == "pvp":
        vf.m_pvp[ma].cur_ctx = ctx
        embed = fb.create_fight_message(ma, vf.m_pvp[ma])
        view = vf.FightViewPVP()

        fb.x_able_all_buttons(True, view.children, ma, vf.m_pvp)
        vf.m_pvp[ma].selff = view
        if ma not in fbt.ending_turn:
            fb.x_able_all_buttons(False, view.children, ma, vf.m_pvp)

    await ctx.edit(content=None, embed=embed, view=view)
    vf.fight_starts.pop(ma)


def get_top_players():
    ranks = []
    for k, v in ocs.data.items():
        if not k in ["bazaar", "shop", "last_dis"]:
            if not v["rank"] == 0:
                ranks.append((k, v["rank"]))
    ranks = sorted(ranks, key=lambda j: j[1], reverse=True)

    price_ls = [50, 35, 20, 10, 5]
    value_desc = []
    highest_ranks = []
    ran = 5
    if len(ranks) < 5:
        ran = len(ranks)
    for r in range(0, ran):
        highest_ranks.append((ranks[r][0], price_ls[r]))
        value_desc.append(f"**{r + 1}** - {ranks[r][0]} - **{ranks[r][1]}** 💠 - {price_ls[r]} {a_setup.kk}\n")

    return "".join(value_desc), highest_ranks


@a_setup.client.slash_command(name="fight-menu", description="Open the fight menu", guild_ids=a_setup.guild_ids)
async def fight_menu(ctx):
    await ctx.respond("Your message is on it's way...", ephemeral=True)
    ma = ctx.author.mention.replace("!", "")

    ocs.check_user(ma)
    embed = dc.Embed(title=f"Pick a fight, {ctx.author.name}", colour=dc.Colour(ocs.data[ma]["color"]),
                     description="🌐 Choose what you want to do. 🌐")
    gtp = get_top_players()[0]
    if not gtp:
        gtp = "No top players."
    embed.add_field(name="Top Players - Weekly", value=gtp)

    view = vf.PreFightView()
    await ctx.edit(content=None, embed=embed, view=view)
