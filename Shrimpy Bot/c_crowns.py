import a_setup
import datetime
import d_open_close_stuff as ocs
import b_community_server_active as csa


@a_setup.slash.slash(description=f"Claim your daily Kjell Crowns", guild_ids=a_setup.guild_ids)
async def daily(ctx):

    print(f"{ctx.author.name} used the daily command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")
    printed_author = csa.get_printed_author_name(ctx.author)

    # can the user claim their dailies?
    with open(f"{a_setup.data_file_folder_name}/{ctx.channel.guild.id}/banned.txt", mode="r", encoding="utf-8") as \
            banned_users_load:
        banned_users = []
        for user in banned_users_load.readlines():
            banned_users.append(user)

    if message_author in banned_users:
        return

    daily_time = ocs.open_time(ctx)
    users_crowns = ocs.open_crowns(ctx)
    streak = ocs.open_streak(ctx)

    today = datetime.date.today()
    tdelta = datetime.timedelta(days=1)
    yeday = today - tdelta

    # Did they ever claim it/ today?
    if message_author not in daily_time:
        daily_time[message_author] = "0"
        users_crowns[message_author] = 300  # newcomer bonus :]
        streak[message_author] = 0

    if daily_time[message_author] == str(today):
        await ctx.message.edit(content=f"**{printed_author}**, you have already claimed your {a_setup.kk} today!")
        return

    user_earnings = 65

    # If the date is not yesterday and the streak is therefore interrupted
    if not daily_time[message_author] == str(yeday):
        streak[message_author] = 1
        users_crowns[message_author] += user_earnings
        end_emoji = ":fire:"

    # If the date is yesterday and the streak is therefore not interrupted
    else:
        streak[message_author] += 1
        new_streak = streak[message_author]

        if new_streak == 69:
            end_emoji = ":people_hugging:"
        else:
            end_emoji = ":fire:"

        rewards = ("65 " * 3) + ("70 " * 2) + ("75 " * 2) + ("80 " * 2) + ("85 " * 2) + ("90 " * 2) + "95"
        reward_list = rewards.split(" ")
        try:
            user_earnings = reward_list[streak[message_author]]
        except IndexError:
            user_earnings = 95
        users_crowns[message_author] += int(user_earnings)

    daily_time[message_author] = str(today)

    ocs.close_crowns(ctx, users_crowns)
    ocs.close_time(ctx, daily_time)
    ocs.close_streak(ctx, streak)

    await ctx.message.edit(content=
                           f"Congratulations **{printed_author}**, you have claimed your daily "
                           f"**{user_earnings}** {a_setup.kk} ! Your streak is now **{streak[message_author]}** "
                           f"{end_emoji}!")


@a_setup.slash.slash(description="See how many Kjell Crowns you have", guild_ids=a_setup.guild_ids)
async def kk(ctx):

    print(f"{ctx.author.name} used the kk command")

    await ctx.send("Your message is on it's way...")

    message_author = ctx.author.mention.replace("!", "")
    printed_author = csa.get_printed_author_name(ctx.author)

    users_crowns = ocs.open_crowns(ctx)

    if message_author not in users_crowns:
        await ctx.message.edit(content=f"**{printed_author}**, you haven't possessed any {a_setup.kk} yet!")

    else:
        await ctx.message.edit(content=f"**{printed_author}** has **{users_crowns[message_author]}** {a_setup.kk}")
