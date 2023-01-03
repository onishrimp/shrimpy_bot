import random
import a_setup
import b_community_server_active as csa
import discord as dc


@a_setup.client.slash_command(name="ping", description="Get the bots ping", guild_ids=a_setup.guild_ids)
async def ping(ctx):
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
    await ctx.respond(f"{emoji_1} **Bot Ping - {bot_ping}ms** {emoji_2}")


@a_setup.client.slash_command(name="mmm", description="Ask a question to my magic mussel", guild_ids=a_setup.guild_ids)
async def mmm(ctx, question: dc.Option(description="Your question to my magic mussel")):
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
    await ctx.respond(message)


@a_setup.client.slash_command(description="Flip a coin", guild_ids=a_setup.guild_ids)
async def coinflip(ctx):
    printed_author = csa.get_printed_author_name(ctx.author)
    responses = [":moyai: Head :moyai:", ":shark: Tails :shark:"]
    await ctx.respond(f"**{printed_author}** flipped a coin. :coin:\nThe result is:\n"
                      f"**{random.choice(responses)}**")


@a_setup.client.slash_command(description="Suggest something for the server", guild_ids=a_setup.guild_ids)
async def suggestion(ctx, sug: dc.Option(description="Your suggestion in under 250 characters")):
    await ctx.respond("Your message is on it's way...")
    printed_author = csa.get_printed_author_name(ctx.author)
    sug_len = len(sug)
    if sug_len <= 250:
        with open(f"{a_setup.data_file_folder_name}/{ctx.channel.guild.id}/suggestions.txt", mode="a", encoding="utf-8") \
                as suggestions:
            suggestions.write(f"{printed_author} suggested: {sug}\n\n")
        await ctx.edit(content=f"**{printed_author}**, you have successfully suggested something.")
    elif sug_len == 690:
        await ctx.edit(content=f"**{printed_author}**, try to stay below **250 characters**! You used: "
                               f"**{sug_len}** :flushed:")
    elif sug_len > 250:
        await ctx.edit(content=f"**{printed_author}**, try to stay below **250 characters**! You used: "
                                       f"**{sug_len}** :skull:")
