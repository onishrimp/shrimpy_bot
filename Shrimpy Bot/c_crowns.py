import a_setup
import datetime
import d_open_close_stuff as ocs
import b_community_server_active as csa


@a_setup.client.slash_command(description=f"Claim your daily Kjell Crowns", guild_ids=a_setup.guild_ids)
async def daily(ctx):
    await ctx.respond("Your message is on it's way...")

    ma = ctx.author.mention.replace("!", "")
    printed_author = csa.get_printed_author_name(ctx.author)

    # can the user claim their dailies?
    with open(f"{a_setup.data_file_folder_name}/{ctx.channel.guild.id}/banned.txt", mode="r", encoding="utf-8") as \
            banned_users_load:
        banned_users = []
        for user in banned_users_load.readlines():
            banned_users.append(user)

    if ma in banned_users:
        return

    today = datetime.date.today()
    tdelta = datetime.timedelta(days=1)
    yeday = today - tdelta

    if ocs.data[ma]["daily_kk"] == str(today):
        await ctx.edit(content=f"**{printed_author}**, you have already claimed your {a_setup.kk} today!")
        return

    user_earnings = 65

    # If the date is not yesterday and the streak is therefore interrupted
    if not ocs.data[ma]["daily_kk"] == str(yeday):
        ocs.data[ma]["streak"] = 1
        ocs.data[ma]["kk"] += user_earnings
        end_emoji = ":fire:"

    # If the date is yesterday and the streak is therefore not interrupted
    else:
        ocs.data[ma]["streak"] += 1
        new_streak = ocs.data[ma]["streak"]

        if new_streak == 69:
            end_emoji = ":people_hugging:"
        else:
            end_emoji = ":fire:"

        rewards = ("65 " * 3) + ("70 " * 2) + ("75 " * 2) + ("80 " * 2) + ("85 " * 2) + ("90 " * 2) + "95"
        reward_list = rewards.split(" ")
        try:
            user_earnings = reward_list[ocs.data[ma]["streak"]]
        except IndexError:
            user_earnings = 95
        ocs.data[ma]["kk"] += int(user_earnings)

    ocs.data[ma]["daily_kk"] = str(today)

    await ctx.edit(content=
                   f"Congratulations **{printed_author}**, you have claimed your daily "
                   f"**{user_earnings}** {a_setup.kk} ! Your streak is now **{ocs.data[ma]['streak']}** "
                   f"{end_emoji}!")


@a_setup.client.slash_command(description="See how many Kjell Crowns you have", guild_ids=a_setup.guild_ids)
async def kk(ctx):
    await ctx.respond("Your message is on it's way...")

    ma = ctx.author.mention.replace("!", "")
    printed_author = csa.get_printed_author_name(ctx.author)

    ocs.check_user(ma)
    await ctx.edit(content=f"**{printed_author}** has **{ocs.data[ma]['kk']}** {a_setup.kk}")
