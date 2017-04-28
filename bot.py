#!/usr/bin/python3
import cfg, socket, re, time, sys, random
import psycopg2
import sys

HOST = cfg.HOST
PORT = cfg.PORT
NICK = cfg.NICK
PASS = cfg.PASS
CHAN = cfg.CHAN
DB_HOST = cfg.DB_HOST
DB_NAME = cfg.DB_NAME
DB_USER = cfg.DB_USER
DB_PASSWORD = cfg.DB_PASSWORD
DB_VIEWERS_TABLE = cfg.DB_VIEWERS_TABLE

ENGAGE = False
adminList = [cfg.ADMIN1, cfg.ADMIN2, cfg.ADMIN3]
sec = cfg.sec # ◄ Set desired seconds to wait for script termination (0 is 1 sec)
MAXSENDINTERVAL = 20.0/30

#------------------------------------------------▼ IRC control dictionary

def send_pong(msg):
    s.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))

def send_message(chan, msg):
    s.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))

def send_nick(nick):
    s.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))

def send_pass(password):
    s.send(bytes('PASS %s\r\n' % password, 'UTF-8'))

def join_channel(chan):
    s.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))

def part_channel(chan):
    s.send(bytes('PART %s\r\n' % chan, 'UTF-8'))

#------------------------------------------------▼ get_stuff

def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result

#------------------------------------------------▼ !commands dictionary

#------▼ Admin only commands

def command_yolo():
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, 'SWAG'), 'UTF-8'))

def command_swag():
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, 'YOLO'), 'UTF-8'))

def command_clear():
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, '.clear'), 'UTF-8'))

def command_leave():
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, 'OK, fine. Later Scrublords!'), 'UTF-8'))
    time.sleep(1)
    countdown(sec)

def list_viewers(): # Prints logged viewers in Terminal/Shell
    print('▌Viewers Log:')
    for viewer in loggedViewers:
        print('• ' + viewer)

#------▼ Non-Admin commands

def command_scrublord():
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, 'Once a scrublord always a scublord'), 'UTF-8'))

def command_general(): #◄ 003 ▓
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, '/me knows: !roulette, !commands, "How art thou <Bot Name>?"'), 'UTF-8'))

#------▼ Soft Ban-Hammer

def command_purge(sender):
    s.send(bytes("PRIVMSG %s :%s %s 1\r\n" %(CHAN, '.timeout', sender), 'UTF-8'))

#------------------------------------------------▼ Cap dictionary

def command_getusers():
    s.send(bytes("CLEARCHAT %s" % CHAN, 'UTF-8'))

def capreq_tags():
    s.send(bytes("CAP REQ :twitch.tv/tags\r\n", 'UTF-8'))

def capreq_membership():
    s.send(bytes("CAP REQ :twitch.tv/membership\r\n", 'UTF-8'))

def capreq_commands():
       s.send(bytes("CAP REQ :twitch.tv/commands\r\n", 'UTF-8'))

#------------------------------------------------▼ Bot Messages

def arrive_message():
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, 'The Bot has arrived!'), 'UTF-8'))

#------------------------------------------------▼ The Bot know's that feel, bro

mood = [cfg.nice, cfg.fine, cfg.not_bad, cfg.ok, cfg.not_sure, cfg.frustrated, cfg.doin_great] 

def mood_swing():
    send_message(CHAN,"@"+sender+random.choice(mood))

#------------------------------------------------▼ I wanna play a game

chamber = 0
cylinder = 0

def shoot_me_mofo():
    send_message(CHAN, 'Six chambers; one ban-hammer, ' + sender + '. What will you get?')
    time.sleep(2)
    send_message(CHAN, '/me loads a grenade and rotates the cylinder...')
    time.sleep(2)
    chamber = random.randint(1,6)
    cylinder = random.randint(1,6)
    if  cylinder == chamber:
        time.sleep(1)
        send_message(CHAN, sender + ' JUST GOT REKT!!')
        command_purge(sender)
    else:
        send_message(CHAN, sender + ', you got lucky this time, scrub!')
        print('Bullet in:', chamber, 'of 6', 'Rotated to:', cylinder, 'of 6')

#------------------------------------------------▼ Message parsing & related variables

admin_commands = ['^!swag $', '^!c $', '^!viewers $'] #◄ 000
general_commands = ['^!yolo $', '^!roulette $', '^!commands $']
href = ['https://www.', 'www.', '.com', '.co', '.uk', '.jpg', '.gif']#◄ 001
leave_channel = '!exit' #◄ 002
scrublord = 'scrublord 4 life'
hat = 'how art thou '+NICK+'?'


def parse_message(sender, msg):
    if len(msg) >= 1:
        split_msg = msg.split(' ')
        
        #----------------------------------------▼ Admin !commands
        #Checks to see if sender is an admin
        
        for command in admin_commands: #◄ 000
            if re.match(command, msg):
                adminFile = None
                print('▓ Admin command detected! ▓')
                try:
                    with open('admins.txt', 'rt') as adminFile:
                        for line in adminFile: 
                            if sender in line:
                                options = {
                                    '!swag': command_swag,
                                    '!c': command_clear,
                                    '!viewers': list_viewers
                                    }
                                if split_msg[0] in options:
                                    options[split_msg[0]]()
                                
                except IOError:
                    print('▓▓ ▓▓ ERROR: Failed to load admins.txt! ▓▓ ▓▓')
                    return
                
                finally:
                    if adminFile is not None:
                        adminFile.close()
                    return

        #----------------------------------------▼ General Non-Admin commands
        #If sender is not an Admin, runs this

        for command in general_commands:
            if re.match(command, msg):
                print('▓ Command detected! ▓')
                options = {
                    '!yolo': command_yolo,
                    '!roulette': shoot_me_mofo,
                    '!commands': command_general
                    }

                if split_msg[0] in options:
                    options[split_msg[0]]()
                    return

        #----------------------------------------▼ Link posting
        #if link posted, checks user's privilege
        
        for hlink in href: #◄ 001
            if hlink in msg.lower():
                scrubsFile = None
                link_privilege = None
                print('▓ Hyperlink Detected!             ▓')
                try:
                    with open('scrubs.txt', 'rt') as scrubsFile:
                        for line in scrubsFile: 
                            if sender in line:
                                link_privilege = 1
                except IOError:
                    print('▓▓ ▓▓ ERROR: Failed to load scrubs.txt! ▓▓ ▓▓')
                    return
                
                finally:
                    if link_privilege is None:
                        print('▓ Scrub not found; purging sender ▓')
                        command_purge(sender)
                        send_message(CHAN, 'Sorry, you were not authorized to do that, ' + sender)
                    if scrubsFile is not None:
                        scrubsFile.close()
                    if link_privilege is not None:
                        link_privilege = None
                    return

        #----------------------------------------▼ Other message commands

        if scrublord in msg.lower():
            command_scrublord()
        elif hat in msg.lower():
            mood_swing()

        elif leave_channel in msg.lower(): #◄ 002
            for user in adminList:
                if sender == user:
                    command_leave()

        else:
            return

#------------------------------------------------▼ Terminate Script Timer

def countdown(sec):
    #---------This CANNOT work here! #◄ 004
    '''for viewer in loggedViewers:
        viewersLog.write(viewer)
        viewersLog.write('\n')
    viewersLog.close()'''
    print('Bot DISABLED!') 
    while (sec >= 0):
        print('Terminating script in:', sec,'seconds.')
        sec -= 1
        time.sleep(1)
    if sec == -1:
        part_channel(CHAN)
        print('Safe to end this Process.')
        sys.exit()

#------------------------------------------------▼ Connect to DB

def save_to_db(username):
    #Define our connection string
    conn_string = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)

    #Print the connection string we will use to connection
    print ("Connecting to database\n ->%s" % (conn_string))

    #get a connection, if connection cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    #conn.cursor will return a cursor object, you can use this cursor object to perform queries
    cursor = conn.cursor()
    print ("Connected:\n")

    #Check to see if username exists in database. If not, insert username
    cursor.execute("SELECT username FROM " +DB_VIEWERS_TABLE+ " WHERE username=%s", (username,))

    if(cursor.fetchone() is not None):
        print ("username found")
    else:
        cursor.execute("INSERT INTO " +DB_VIEWERS_TABLE+ " (username) VALUES (%s);", (username,))
        conn.commit()

    cursor.close()
    conn.close()

    print ("Disconnected:\n")
#------------------------------------------------

data = ""

s = socket.socket()
s.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
capreq_membership()
capreq_commands()
#capreq_tags() -Works, but breaks adminList commands; possibly other things
join_channel(CHAN)

print('Initializing')

while True:
    
    try:
        data = data+s.recv(1024).decode('UTF-8')
        print (data)
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()
            
        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)

            if len(line) >= 1:
                if line[0] == 'PING':
                    send_pong(line[1])

                if line[1] == 'PRIVMSG':
                    sender = get_sender(line[0])
                    message = get_message(line)
                    parse_message(sender, message)
                    print('CHAT> '+sender +": " + message)

                if line[1] == 'JOIN':
                    sender = get_sender(line[0])
                    save_to_db(sender)
                    print('▌VIEWER UPDATE: ' +'|' +sender +'|' +' has joined the chat!')
                    #send_message(CHAN, 'Welcome '+sender+'! Ya Scrub') -Turned off. May scare/trigger people

                if line[1] == 'PART':
                    sender = get_sender(line[0])
                    print('▌VIEWER UPDATE: '+sender +' has left the chat! :(')

            while ENGAGE == False:
                print('I have arrived in ' + CHAN + "'s channel!")
                #arrive_message()
                time.sleep(1)
                ENGAGE = True
        time.sleep(MAXSENDINTERVAL)
                
    except socket.error:
        print("Socket lost")

    except socket.timeout:
        print("Socket timeout")

