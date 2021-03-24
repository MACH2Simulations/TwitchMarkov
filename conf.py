class Conf:
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



    # Do you want to log all messages sent by the bot?
    #logmessages = False #TODO Make this optional
    logdir = "C:\\bots\\logs\\" + channel + "_" + nickname + ".txt" #Note this directory must exsist but the file doesnt have to


    # Add users to ignore, lowercase.
    ignoredUsers = [
        "nightbot", "streamlabs", nickname
    ]

    # Add mods who can use commands, lowercase.
    # Use Double quotes 
    mods = [
           "mach2simulations"
    ]

    # THESE ARE WORDS THE BOT SHOULD NEVER LEARN.
    blacklisted_words = [
    ]
    nickname2 = "@" + nickname
    CMD_MEN = "@Bot" #Calls Bot to force a message
    CMD_WHAT = "-botinfo" #Posts link to github
    CMD_TOGGLE = "-toggle" #Toggles bot off and on
    CMD_CLEAR = "-refreshing"
    CMD_WIPE = "-wipe"
    CMD_SET_NUMBER = "-number" #how many chat messages before bot talks
    CMD_ALIVE = "-ping"
    CMD_UNIQUE = "-unique"
    CMD_EXIT = "-exit"

    SELF_PREFIX = "Maintenance Message: "

    # Your Twitch name, lowercase.
    owner = ""
