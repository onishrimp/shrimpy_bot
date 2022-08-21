import a_setup


def get_printed_author_name(user):

    if a_setup.name_mentions_active:
        return user.mention.replace("!", "")

    else:
        return user.name
