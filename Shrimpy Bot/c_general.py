import random
import a_setup
import b_community_server_active as csa


@a_setup.slash.slash(description="Get the bots ping", guild_ids=a_setup.guild_ids)
async def ping(ctx):
    print(f"{ctx.author.name} used the ping command")
    bot_ping = round(a_setup.client.latency * 1000)
    clock_emojis = ["🕐", "🕙", "🕥", "🕚", "🕦", "🕛", "🕧", "🕜", "🕑", "🕝", "🕒", "🕞", "🕓", "🕟", "🕔", "🕠", "🕕",
                    "🕡", "🕖", "🕢", "🕗", "🕣", "🕘", "🕤"]
    if bot_ping == 69:
        emoji_1, emoji_2 = ":flushed:", ":flushed:"
    elif bot_ping == 187:
        emoji_1, emoji_2 = ":woman_police_officer:", ":man_police_officer:"
    elif bot_ping == 42:
        emoji_1, emoji_2 = ":four_leaf_clover:", ":four_leaf_clover:"
    else:
        emoji_1, emoji_2 = random.choice(clock_emojis), random.choice(clock_emojis)
    await ctx.send(f"{emoji_1} **Bot Ping - {bot_ping}ms** {emoji_2}")


@a_setup.slash.slash(description="Ask a question to my magic mussel", guild_ids=a_setup.guild_ids)
async def mmm(ctx, question):
    print(f"{ctx.author.name} used the mmm command")
    printed_author = csa.get_printed_author_name(ctx.author)
    responses = ["Yes",
                 "Definitely",
                 "Certainly",
                 "No",
                 "Definitely not",
                 "Preferably not",
                 "Maybe",
                 "I don't know"]
    message = f"**Question from {printed_author}:** {question}\n**Answer:** {random.choice(responses)}"
    if "blood shed" in question.lower():
        message = f"**QUESTION FROM {printed_author}:** {question}\n**ANSWER:** :boom: I KNOW A LOT :zap: " \
                  f"BUT THE ONLY THING I KNOW FOR REAL :earth_africa: IS THAT THERE WILL BE :fire: " \
                  f":fire: **BLOOOOOOOD :white_flower: SHEEEEEEEEEED** :boom: :boom: :boom:"
    elif question == "What do you know?":
        message = f"**QUESTION FROM {printed_author}:** {question}\n**ANSWER:** I only know what I know."
    await ctx.send(message)


@a_setup.slash.slash(description="Flip a coin", guild_ids=a_setup.guild_ids)
async def coinflip(ctx):
    print(f"{ctx.author.name} used the coinflip command")
    printed_author = csa.get_printed_author_name(ctx.author)
    responses = [":moyai: Head :moyai:", ":shark: Tails :shark:"]
    await ctx.send(f"**{printed_author}** flipped a coin. :coin:\n\nThe result is:\n"
                   f"**{random.choice(responses)}**")


@a_setup.slash.slash(description="Suggest something for the server", guild_ids=a_setup.guild_ids)
async def suggestion(ctx, sug):
    print(f"{ctx.author.name} used the suggestion command")
    await ctx.send("Your message is on it's way...")
    printed_author = csa.get_printed_author_name(ctx.author)
    sug_len = len(sug)
    if sug_len <= 250:
        with open(f"{a_setup.data_file_folder_name}/{ctx.channel.guild.id}/suggestions.txt", mode="a", encoding="utf-8") \
                as suggestions:
            suggestions.write(f"{printed_author} suggested: {sug}\n\n")
        await ctx.message.edit(content=f"**{printed_author}**, you have successfully suggested something.")
    elif sug_len == 690:
        await ctx.message.edit(content=f"**{printed_author}**, try to stay below **250 characters**! You used: "
                               f"**{sug_len}** :flushed:")
    elif sug_len > 250:
        await ctx.message.edit(content=f"**{printed_author}**, try to stay below **250 characters**! You used: "
                                       f"**{sug_len}** :skull:")
