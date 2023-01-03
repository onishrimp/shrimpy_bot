import a_setup


@a_setup.client.event
async def on_ready():
    print("The bot is online")


a_setup.client.run(a_setup.token)
