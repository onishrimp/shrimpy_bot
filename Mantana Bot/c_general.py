import a_setup
import discord as dc


@a_setup.client.event
def on_member_join(member):
    channel = dc.utils.get(member.guild.channels, name=a_setup.welcome_channel_name)
    await channel.send(f"{member.mention} joined the server!")


@a_setup.client.event
def on_member_remove(member):
    channel = dc.utils.get(member.guild.channels, name=a_setup.welcome_channel_name)
    await channel.send(f"{member.mention} left the server!")
