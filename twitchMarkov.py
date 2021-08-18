from conf import Conf
from emoji import demojize
import sys
sys.path.append(Conf.GlobalConf)
from Global_Conf import Global_Banned
from Global_Conf import Global_Authed
from Global_Conf import Global_Conf
sys.path.append(Conf.logdir)
import datetime
import socket
import markovify
import re
import traceback
import random
import requests
import json
import time

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


with open(Conf.logdir, "a", encoding="utf-8")as q:
    q.write("Bot Wakes" + '\n')


def SysPrint():
    '''
    Returns 
    -------
    Connection Information,used to know which channel each windows is connected to
    As: Conncted | BotName | Channel Name @BotName LogDIR
    '''
    print("Connected", "|", Conf.nickname,"|", Conf.channel, Conf.nickname2, Conf.logdir)


def Authed_User(Username):
    '''
    Input: A lowercase string containing the username:
    Output: A Boolean (True Or False)
    Use: This Alllows you to check if a user is allowed to use basic bot commands
    Returns: True if Authorised User, Else False
    '''
    if Username == Conf.owner:
        return True
    if Username in Conf.mods:
        return True
    if Username == Conf.channel:
        return True
    if Username in Global_Authed.Global_Authed_Users:
        if Conf.Allows_Global_Auth is True:
            return True
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
    if Username == Conf.channel:
        return True
    if Username in Global_Authed.Global_Authed_Users:
        if Conf.Allows_Global_Auth is True:
            return True
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
    if username in Global_Banned.Global_Banned_Users:
        return True
    if username == Conf.nickname:
        return True
    if username == Conf.channel:
        return True
    
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



def sendMessage(sock, channel, message,isadmin):
    '''

    Parameters
    ----------
    channel : String
        A Channel Name in lowercase
    message : String
        a message
    isadmin : Boolean
        Is this an admin message
    Returns
    -------
    None.

    '''
    
    
    if isadmin is False:
        if SEND_MESSAGES:
            sock.send("PRIVMSG #{} :{}\r\n".format(
            channel, message).encode("utf-8"))
    else:
        sock.send("PRIVMSG #{} :{}\r\n".format(
        channel, Conf.SELF_PREFIX + message).encode("utf-8"))
        
        
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
    if ALLOW_MENTIONS is False:
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
    # if message != None and message != "":  ## Linter is shouting at me
    try: 
        if len(message) > 1:
            if messageCount == 0 and CLEAR_LOGS_AFTER:
                f = open(LOGFILE, "w", encoding="utf-8")
            else:
                f = open(LOGFILE, "a", encoding="utf-8")
                f.write(message + "\n")
                f.close()
                return True
            return False
    except TypeError:
        return None 
    
    
    
def TrollLoved(sock,channel,username,isadmin=False):
    '''
    Parameters
    ----------
    username : String
        a lower case string
    This takes a username and sends a trolly message to a loved user

    '''
    rand = random.randint(0, 1000)
    print ("Troll ",rand)
    SysPrint()
    if rand % 50 == 0:
        message ='@' + username +  ' You are a brat'
        sendMessage(sock,channel,message,isadmin=False)
    

def RandomCommand(sock,channel,isadmin=False):
    rand = random.randint(0, 100)
    print ("Troll ",rand)
    SysPrint()
    if rand % 5 == 0:
        Tup = Global_Conf.Global_Commands
        RandTup = random.randint(0,(len(Tup)-1))
        message = Tup[RandTup]
        print(message)
        sendMessage(sock, channel, message, isadmin=False)


def Translate(sock,channel,message,isadmin=False):
    rand = random.randint(0, 100)
    print ("Lang ",rand)
    SysPrint()
    rand = 5
    if rand % 5 == 0:
    
        message1 = message 
        key = "GOOGELAPIKEY"
        TargetLang = Global_Conf.Langs[random.randint(0,len(Global_Conf.Langs)-1)]
       
        url = 'https://translation.googleapis.com/language/translate/v2?key='+key+'&q='+message+'&target='+TargetLang+'&format=text'
        x = requests.post(url)
        response = x.json()
        response = response['data']
        response = response['translations']
        response = response[0]
        response = response['translatedText']
        message = response
        print (message, TargetLang, message1)
        time.sleep(3)
        sendMessage(sock, channel, message, isadmin=False)
        print(message)









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
        with open(Conf.logdir, "a") as file_ob:
            file_ob.write(testMess + '\n')
            print(testMess)
    else:
        PHRASES_LIST = [testMess]
        PHRASES_LIST.append(testMess)
        # if Conf.logmessages == True:
        with open(Conf.logdir, "a") as file_ob:
            file_ob.write(testMess + '\n')
            print(testMess)
        SysPrint()
    return testMess


def generateAndSendMessage(sock, channel):
    if SEND_MESSAGES:
        markoved = generateMessage()
        RandomCommand(sock,channel,isadmin=False)
        
        if markoved != None:
            sendMessage(sock, channel, markoved,False)
        else:
            print("Could not generate.")
        Translate(sock,channel,markoved,isadmin=False)




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
                sendMessage(
                    sock, channel, "No longer clearing memory after message!" + Conf.emote, True)
            else:
                CLEAR_LOGS_AFTER = True
                sendMessage(
                    sock, channel, "Clearing memory after every message! FeelsDankMan",True)
            return True
        # Wipe logs
        if message == Conf.CMD_WIPE:
            f = open(LOGFILE, "w", encoding="utf-8")
            f.close()
            sendMessage(sock, channel, "Wiped memory banks. D:",True)
            return True
        # Toggle functionality
        if message == Conf.CMD_TOGGLE:
            if SEND_MESSAGES:
                SEND_MESSAGES = False
                sendMessage(
                    sock, channel, "Messages will no longer be sent! D:",True)
            else:
                SEND_MESSAGES = True
                sendMessage(
                    sock, channel, "Messages are now turned on! :)",True)
            return True
        # Toggle functionality
        if message == Conf.CMD_UNIQUE:
            if UNIQUE:
                UNIQUE = False
                sendMessage(
                    sock, channel, "Messages will no longer be unique. PogO",True)
            else:
                UNIQUE = True
                sendMessage(
                    sock, channel, "Messages will now be unique. PogU",True)
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
                    sendMessage(
                        sock, channel, "Messages will now be sent after " + GENERATE_ON + " chat messages. DankG",True)
            except:
                sendMessage(sock, channel, "Current value: " + str(GENERATE_ON) +
                                ". To set, use: " + str(Conf.CMD_SET_NUMBER) + " [number of messages]",True)
            return True
        # Check if alive.
        if message == Conf.CMD_ALIVE:
            sendMessage(
                sock, channel, "Yeah, I'm alive and learning." + Conf.emote,True)
            return True
        if message == Conf.CMD_WHAT:
            sendMessage(
                sock, channel, "This bot is taken from here https://github.com/MACH2Simulations/TwitchMarkov",True)
            return True
        if message == Conf.CMD_MEN:
            generateAndSendMessage(sock, channel)
            return True
        # Kill
        if Super_User(username) and message == Conf.CMD_EXIT:
            sendMessage(sock, channel, "You have killed me. D:",True)
            sys.exit()   ##Deeposoure says to use this over exit()
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

    SysPrint()

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
                        if username in Global_Banned.Global_Loved_Users:
                            TrollLoved(username)

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
