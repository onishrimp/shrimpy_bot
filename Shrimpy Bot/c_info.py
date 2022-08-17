import a_setup
import discord as dc


@a_setup.slash.slash(description="Learn more about the rarities of items", guild_ids=a_setup.guild_ids)
async def rarities(ctx):

    print(f"{ctx.author.name} used the rarities command")
    kk = a_setup.kk

    description = f"**Common :white_circle:**\n " \
                  f"You can sell them for **40** {kk} to the bank. The probability to pull one is **45%**.\n\n " \
                  f"**Uncommon :green_circle:**\n" \
                  f"You can sell them for **60** {kk} to the bank. The probability to pull one is **25%**.\n\n " \
                  f"**Rare :blue_circle:**\n" \
                  f"You can sell them for **90** {kk} to the bank. The probability to pull one is **20%**.\n\n " \
                  f"**Epic :purple_circle:**\n" \
                  f"You can sell them for **220** {kk} to the bank. The probability to pull one is **7.5%**.\n\n " \
                  f"**Kjell Crowns {kk}**\n" \
                  f"With a chance of **2%** you will get **600** Kjell Crowns instead of an item.\n\n" \
                  f"**Legendary :star:**\n" \
                  f"You can sell them for **800** {kk} to the bank. The probability to pull one is **0.5%**.\n\n " \
                  f"**Specialrank :secret:**\n" \
                  f"You **can't sell** them to the bank. You **can't receive them by gambling**, only during events. " \
                  f"Each of them **should only be once in the game**."

    embed = dc.Embed(title="Information about rarities", colour=dc.Colour(0x6d3619), description=description)
    await ctx.send(embed=embed)


@a_setup.slash.slash(description="The bots basics", guild_ids=a_setup.guild_ids)
async def help_bot(ctx):

    print(f"{ctx.author.name} used the help_bot command")
    kk = a_setup.kk

    description = f"This bot was created by **github.com/onishrimp**.\n\n" \
                  f"**Features**\n" \
                  f"This bot features a gacha system. Each day, you can claim so called 'Kjell Crowns' {kk} with " \
                  f"**/daily**. With **/gamble** you can gamble for dinosaurs and then collect and trade them with " \
                  f"others.\n\n" \
                  f"**It's commands**\n" \
                  f"If you type / in the bot chat and click on the bots icon you will get an overview with simple " \
                  f"descriptions of the bots commands. Then just chose a command and if required give it the needed " \
                  f"parameters. Easier than it sounds." \

    embed = dc.Embed(title="The Shrimpy Bot", colour=dc.Colour(0x6d3619), description=description)

    icon = "https://cdn.discordapp.com/attachments/912362937077891132/914146351548338216/KK_real.png"
    embed.set_thumbnail(url=icon)

    await ctx.send(embed=embed)
