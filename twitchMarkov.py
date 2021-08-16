import traceback
import re
import markovify
import socket
import datetime
from Global_Authed_Users import Global_Authed_Users
from Global_Banned_Conf import Global_Banned
from conf import Conf
from emoji import demojize
import sys
sys.path.append(Conf.Global_Banned_Path)
sys.path.append(Conf.Global_Authed_Path)
# Removed Twitter

GENERATE_ON = Conf.Gen_Message_On
CLEAR_LOGS_AFTER = Conf.CLEAR_LOGS_AFTER
ALLOW_MENTIONS = Conf.ALLOW_MENTIONS
UNIQUE = Conf.UNIQUE
SEND_MESSAGES = Conf.SEND_MESSAGES
CULL_OVER = Conf.CULL_OVER
TIME_TO_CULL = datetime.timedelta(hours=1)

messageCount = 0
TIMES_TO_TRY = Conf.TIMES_TO_TRY
PERCENT_UNIQUE_TO_SAVE = Conf.PERCENT_UNIQUE_TO_SAVE
STATE_SIZE = Conf.STATE_SIZE
PHRASES_LIST = []
LOGFILE = "/uninitialized.txt"


def Authed_User(Username):
    '''
    Input: A lowercase string containing the username:
    Output: A Boolean (True Or False)
    Use: This Alllows you to check if a user is allowed to use basic bot commands
    Returns: True if Authorised User, Else False
    '''
    if Username == Conf.owner:
        return True
    elif Username in Conf.mods:
        return True
    elif Username == Conf.channel:
        return True
    elif Username in Global_Authed_Users.Global_Authed_Users and Conf.Allows_Global_Auth == True:
        return True
    else:
        return False
    return False


def Super_User(Username):
    '''
    Input: A lowercase string containing the username:
    Output: A Boolean (True Or False)
    Use: This Alllows you to check if a user is allowed to use SuperUser Commands (Wipe and Kill)
    Returns: True if Authorised User, Else False
    '''

    if Username == Conf.owner:
        return True
    elif Username == Conf.channel:
        return True
    elif Username in Global_Authed_Users.Global_Authed_Users and Conf.Allows_Global_Auth == True:
        return True
    else:
        return False
    return False


def isUserIgnored(username):
    '''
    Input: A lowercase string containing the username: 
    Output: A Boolean (True Or False)
    Use: Checks if a message from this user should be ignored, Must use for Bot accounts.
    Returns: True if Ignored User, Else False
    '''
    if username in Conf.ignoredUsers:
        return True
    elif username in Global_Banned.Global_Banned_Users:
        return True
    elif username == Conf.nickname:
        return True
    elif username == Conf.channel:
        return True
    else:
        return False
    return False


def checkBlacklisted(message):
    '''
    Input: A Message in any case
    Output: A Boolean (True Or False)
    Use: Checks if message contains banned words
    Returns: True if banned words, Else False 
    '''
    for i in Conf.blacklisted_words:
        if re.search(r"\b" + i, message, re.IGNORECASE):
            return True
    for i in Global_Banned.Global_Banned_Words:
        if re.search(r"\b" + i, message, re.IGNORECASE):
            return True

    return False


q = open(Conf.logdir, "a", encoding="utf-8")
q.write("Bot Wakes" + '\n')
q.close()


def listMeetsThresholdToSave(part, whole):
    global PERCENT_UNIQUE_TO_SAVE
    pF = float(len(part))
    wF = float(len(whole))
    if wF == 0:
        return False
    uniqueness = (pF/wF) * float(100)
    return (uniqueness >= PERCENT_UNIQUE_TO_SAVE)


def filterMessage(message):
    '''
    Input: A string
    Output: A string
    Use: Checks if a message in banned, if not removes stuff like mentions 
    Returns: Nothing or a cleaned message

    '''

    if checkBlacklisted(message):
        return None

    # Remove links
    # TODO: Fix
    message = re.sub(r"http\S+", "", message)

    # Remove mentions
    if ALLOW_MENTIONS == False:
        message = re.sub(r"@\S+", "", message)

    # Remove just repeated messages.
    words = message.split()
    # Make list unique
    uniqueWords = list(set(words))
    if not listMeetsThresholdToSave(uniqueWords, words):
        return None

    # Space filtering
    message = re.sub(r" +", " ", message)
    message = message.strip()
    return message


def writeMessage(message):
    global CLEAR_LOGS_AFTER
    global LOGFILE
    message = filterMessage(message)
    if message != None and message != "":
        if messageCount == 0 and CLEAR_LOGS_AFTER:
            f = open(LOGFILE, "w", encoding="utf-8")
        else:
            f = open(LOGFILE, "a", encoding="utf-8")
        f.write(message + "\n")
        f.close()
        return True
    return False


def generateMessage():
    global LOGFILE
    global PHRASES_LIST
    with open(LOGFILE, encoding="utf-8") as f:
        text = f.read()
    text_model = markovify.NewlineText(text, state_size=STATE_SIZE)
    testMess = None
    if UNIQUE and (len(PHRASES_LIST) > 0):
        foundUnique = False
        tries = 0
        while not foundUnique and tries < 20:
            testMess = text_model.make_sentence(tries=TIMES_TO_TRY)
            if not (testMess in PHRASES_LIST):
                foundUnique = True
            tries += 1
    else:
        testMess = text_model.make_sentence(tries=TIMES_TO_TRY)
    if not (testMess is None):
        PHRASES_LIST.append(testMess)
        # if Conf.logmessages == True:
        ff = open(Conf.logdir, "a")
        ff.write(str(testMess + '\n'))
        ff.close()
        print(testMess)

        print("Connected", "|", Conf.nickname,
              "|", Conf.channel, Conf.nickname2)
    else:
        PHRASES_LIST = [testMess]
        PHRASES_LIST.append(testMess)
        # if Conf.logmessages == True:
        ff = open(Conf.logdir, "a")
        ff.write(str(testMess + '\n'))
        ff.close()

        print(testMess)
        print("Connected", "|", Conf.nickname,
              "|", Conf.channel, Conf.nickname2)
    return testMess


def generateAndSendMessage(sock, channel):
    if SEND_MESSAGES:
        markoved = generateMessage()
        if markoved != None:
            sendMessage(sock, channel, markoved)
        else:
            print("Could not generate.")


def sendMessage(sock, channel, message):
    if SEND_MESSAGES:
        sock.send("PRIVMSG #{} :{}\r\n".format(
            channel, message).encode("utf-8"))


def sendMaintenance(sock, channel, message):
    sock.send("PRIVMSG #{} :{}\r\n".format(
        channel, Conf.SELF_PREFIX + message).encode("utf-8"))


def handleAdminMessage(username, channel, sock):
    global CLEAR_LOGS_AFTER
    global LOGFILE
    global SEND_MESSAGES
    global GENERATE_ON
    global UNIQUE
    if Authed_User(username):
        # Log clearing after message.
        if message == Conf.CMD_CLEAR:
            if CLEAR_LOGS_AFTER == True:
                CLEAR_LOGS_AFTER = False
                sendMaintenance(
                    sock, channel, "No longer clearing memory after message!" + Conf.emote)
            else:
                CLEAR_LOGS_AFTER = True
                sendMaintenance(
                    sock, channel, "Clearing memory after every message! FeelsDankMan")
            return True
        # Wipe logs
        if message == Conf.CMD_WIPE:
            f = open(LOGFILE, "w", encoding="utf-8")
            f.close()
            sendMaintenance(sock, channel, "Wiped memory banks. D:")
            return True
        # Toggle functionality
        if message == Conf.CMD_TOGGLE:
            if SEND_MESSAGES:
                SEND_MESSAGES = False
                sendMaintenance(
                    sock, channel, "Messages will no longer be sent! D:")
            else:
                SEND_MESSAGES = True
                sendMaintenance(
                    sock, channel, "Messages are now turned on! :)")
            return True
        # Toggle functionality
        if message == Conf.CMD_UNIQUE:
            if UNIQUE:
                UNIQUE = False
                sendMaintenance(
                    sock, channel, "Messages will no longer be unique. PogO")
            else:
                UNIQUE = True
                sendMaintenance(
                    sock, channel, "Messages will now be unique. PogU")
            return True
        # Generate message on how many numbers.
        if message.split()[0] == Conf.CMD_SET_NUMBER:
            try:
                stringNum = message.split()[1]
                if stringNum != None:
                    num = int(stringNum)
                    if num <= 0:
                        raise Exception
                    GENERATE_ON = num
                    sendMaintenance(
                        sock, channel, "Messages will now be sent after " + GENERATE_ON + " chat messages. DankG")
            except:
                sendMaintenance(sock, channel, "Current value: " + str(GENERATE_ON) +
                                ". To set, use: " + str(Conf.CMD_SET_NUMBER) + " [number of messages]")
            return True
        # Check if alive.
        if message == Conf.CMD_ALIVE:
            sendMaintenance(
                sock, channel, "Yeah, I'm alive and learning." + Conf.emote)
            return True
        if message == Conf.CMD_WHAT:
            sendMaintenance(
                sock, channel, "This bot is taken from here https://github.com/MACH2Simulations/TwitchMarkov")
            return True
        if message == Conf.CMD_MEN:
            generateAndSendMessage(sock, channel)
            return True
        # Kill
        if Super_User(username) and message == Conf.CMD_EXIT:
            sendMaintenance(sock, channel, "You have killed me. D:")
            exit()
    return False


def cullFile():
    fin = open(LOGFILE, "r", encoding="utf-8")
    data_list = fin.readlines()
    fin.close()

    size = len(data_list)
    if size <= CULL_OVER:
        return
    size_delete = size // 2
    del data_list[0:size_delete]

    fout = open(LOGFILE, "w", encoding="utf-8")
    fout.writelines(data_list)
    fout.close()


def shouldCull(last_cull):
    now_time = datetime.datetime.now()
    time_since_cull = now_time - last_cull
    if time_since_cull > TIME_TO_CULL:
        cullFile()
        last_cull = datetime.datetime.now()
    return last_cull

# PROGRAM HERE


last_cull = datetime.datetime.now()

while True:
    # Initialize socket.
    sock = socket.socket()

    # Connect to the Twitch IRC chat socket.
    sock.connect((Conf.server, Conf.port))

    # Authenticate with the server.
    sock.send(f"PASS {Conf.token}\n".encode('utf-8'))
    sock.send(f"NICK {Conf.nickname}\n".encode('utf-8'))
    sock.send(f"JOIN #{Conf.channel}\n".encode('utf-8'))

    LOGFILE = Conf.channel + "Logs.txt"

    print("Connected", "|", Conf.nickname, "|",
          Conf.channel, Conf.nickname2, Conf.logdir)

    # Main loop
    while True:
        try:
            # Receive socket message.
            resp = sock.recv(2048).decode('utf-8')

            # Keepalive code.
            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
            # Actual message that isn't empty.
            elif len(resp) > 0:
                try:
                    msg = demojize(resp)
                    # Break out username / channel / message.
                    regex = re.search(
                        r':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', msg)
                    # If we have a matching message, do something.
                    if regex != None:
                        # The variables we need.
                        username, channel, message = regex.groups()
                        message = message.strip()

                        # Handle ignored users.
                        if isUserIgnored(username):
                            continue

                        # Broadcaster saying something.
                        if handleAdminMessage(username, channel, sock):
                            continue

                        # Validate and print message to the log.
                        if not writeMessage(message):
                            continue

                        # At this point, it's not an admin message, and it's a successful, valid entry.

                        # Increase messages logged.
                        messageCount += 1

                        # Generate Markov
                        if (messageCount % GENERATE_ON) == 0:
                            generateAndSendMessage(sock, channel)
                            last_cull = shouldCull(last_cull)
                            messageCount = 0
                except Exception as e:
                    print("Inner")
                    traceback.print_exc()
                    print(e)
        except Exception as e:
            print("Outer")
            traceback.print_exc()
            print(e)
            break
