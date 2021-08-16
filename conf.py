class Conf():

    # Hard conf
    server = 'irc.chat.twitch.tv'
    port = 6667

    # Bot account conf
    # Lowercase name
    nickname = ""
    # oauth generate with https://twitchapps.com/tmi/
    token = ""

    # Run config
    # Lowercase channel to join.
    channel = ""
    emote = ""
    # Add mods who can use commands, lowercase.
    # Use Double quotes
    Global_Authed_Path = '/'  # Path To Globally Authed users, usefull for mass deployment
    Allows_Global_Auth = True  # Should Global Authed Users be able to contorl Bot
    mods = [
        "mach2simulations"
    ]

    # Do you want to log all messages sent by the bot?
    # logmessages = False #TODO Make this optional
    # Note this directory must exsist but the file doesnt have to
    logdir = "C:\\bots\\logs\\" + channel + "_" + nickname + ".txt"

    # Add users to ignore, lowercase. #### See ./GlobalBotIgnored : for mass deployment change Global_Banned_Conf

    # Path To Global Banned Users/Words --- Used for bulk deployment
    Global_Banned_Path = '/'
    ignoredUsers = [
        "nightbot", "streamlabs", nickname
    ]
    # THESE ARE WORDS THE BOT SHOULD NEVER LEARN. #### See ./GlobalWordIgnored : for mass deployment change Global_Banned_Conf
    blacklisted_words = [
        'bits'
    ]

    nickname2 = "@" + nickname
    CMD_MEN = "@Bot"  # Calls Bot to force a message
    CMD_WHAT = "-botinfo"  # Posts link to github
    CMD_TOGGLE = "-toggle"  # Toggles bot off and on
    CMD_CLEAR = "-refreshing"
    CMD_WIPE = "-wipe"
    CMD_SET_NUMBER = "-number"  # how many chat messages before bot talks
    CMD_ALIVE = "-ping"
    CMD_UNIQUE = "-unique"
    CMD_EXIT = "-exit"

    SELF_PREFIX = "Maintenance Message: "

# Your Twitch name, lowercase.
    owner = ""
    # ConfigVars
    Gen_Message_On = 10
    CLEAR_LOGS_AFTER = False  # Should it clear logs after a message: Def False
    ALLOW_MENTIONS = True  # Should Bot @ People: Def True
    UNIQUE = True  # Should bot make unique messages: Def True
    SEND_MESSAGES = True  # Should the bot send messages: Def True
    CULL_OVER = 12000  # How many chat messages should the bot save: Def 12000
    TIMES_TO_TRY = 1000  # How many times should the bot try to make a message
    PERCENT_UNIQUE_TO_SAVE = 100  # How Much should bot remeber it has said
    STATE_SIZE = 4  # An integer, indicating the number of words in the model's state. ----- i don;t know what this means 2 WORKS Well, trying 4 to see what happens
