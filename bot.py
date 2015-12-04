import cfg, socket, re, time, sys, random

HOST = cfg.HOST
PORT = cfg.PORT
NICK = cfg.NICK
PASS = cfg.PASS
CHAN = cfg.CHAN

ENGAGE = False
adminList = [cfg.ADMIN1, cfg.ADMIN2, cfg.ADMIN3]
sec = cfg.sec # ◄ Set desired seconds to wait for script termination (0 is 1 sec)
MAXSENDINTERVAL = 20.0/30

#------------------------------------------------▼

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

def capreq_tags():
    s.send(bytes("CAP REQ :twitch.tv/tags\r\n", 'UTF-8'))

def capreq_membership():
    s.send(bytes("CAP REQ :twitch.tv/membership\r\n", 'UTF-8'))

def capreq_commands():
       s.send(bytes("CAP REQ :twitch.tv/commands\r\n", 'UTF-8'))

#------------------------------------------------▼ !commands dictionary

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

def command_scrublord():
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, 'Once a scrublord always a scublord'), 'UTF-8'))

def command_purge(sender):
    s.send(bytes("PRIVMSG %s :%s %s 1\r\n" %(CHAN, '.timeout', sender), 'UTF-8'))

def general_commands(): #◄ 003 ▓
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, 'General commands available: !roulette, and !commands'), 'UTF-8'))

#------------------------------------------------▼ Cap Commands

def command_getusers():
    s.send(bytes("CLEARCHAT %s" % CHAN, 'UTF-8'))

#------------------------------------------------▼ Messages

def arrive_message():
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, 'The Bot has arrived!'), 'UTF-8'))

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

#------------------------------------------------▼

admin_commands = ['^!swag $', '^!c $'] #◄ 000 ▓ (◄ 003 Conflict with !c & !commands)
href = ['https://www.', 'www.', '.com', '.co', '.uk', '.jpg', '.gif']#◄ 001
part = '!exit' #◄ 002

def parse_message(sender, msg):
    if len(msg) >= 1:
        s1 = 'scrublord 4 life'
        hat = 'how art thou ' + NICK

        split_msg = msg.split(' ')
        
        if s1 in msg.lower():
            command_scrublord()
        elif hat in msg.lower():
            mood_swing()

        elif part in msg.lower(): #◄ 002
            for user in adminList:
                if sender == user:
                    command_leave()
                    
        


        #----------------------------------------▼
        # ▓ 2015-09-07 Test Code Below! ▓
        link_privilege = None
        print('DEBUG: link_privilege = ', link_privilege)
        #----------------------------------------▼ Admin !commands
        #checks to see if sender is an admin
        for command in admin_commands: #◄ 000
            if re.match(command, msg):
                print('DEBUG: Match found in msg!')
                try:
                    aF = open('admins.txt', 'rt') # ◄ Create a/this user-list File
                    with aF as file:
                        print('DEBUG: Is Admins File open?: ', aF.closed)
                        print('DEBUG: Scanning Sender data...')
                        for line in file: 
                            if sender in line:
                                print('DEBUG: Sender is an Admin!')
                                print('DEBUG: Scanning Options...')
                                options = {'!swag': command_swag,
                                           '!c': command_clear
                                           }
                                if split_msg[0] in options:
                                    options[split_msg[0]]()
                                
                except IOError:
                    print('DEBUG: ▓▓ ▓▓ ▓▓ ▓ ERROR ▓ File Not Found! ▓▓ ▓▓ ▓▓')
                    return
                
                finally:
                    if aF is not None:
                        aF.close()
                    print('DEBUG: Is Admins File open?: ', aF.closed)
                    return

        #----------------------------------------▼
        # ▓ 2015-09-07 Test Code Below! ▓
        #if link posted, checks user's privilege     
        for hlink in href: #◄ 001
            if hlink in msg.lower():
                print('DEBUG: link_privilege = ', link_privilege)
                print('DEBUG: Match found in msg!')
                try:
                    sF = open('scrubs.txt', 'rt') # ◄ Create a/this user-list File
                    with sF as file:
                        print('DEBUG: Scrub File open?: ', sF.closed)
                        print('DEBUG: Scanning Sender data...')
                        for line in file: 
                            if sender in line:
                                print('DEBUG: Sender is a Scrub!')
                                print('DEBUG: link_privilege = ', link_privilege)
                                link_privilege = 1
                                print('DEBUG: link_privilege = ', link_privilege)
                                
                except IOError:
                    print('DEBUG: ▓▓ ▓▓ ▓▓ ▓ ERROR ▓ File Not Found! ▓▓ ▓▓ ▓▓')
                    return
                
                finally:
                    if link_privilege is None:
                        command_purge(sender)
                        send_message(CHAN, 'You were not authorized to do that, ' + sender)
                    if sF is not None:
                        sF.close()
                    if link_privilege is not None:
                        link_privilege = None
                    print('DEBUG: Scrub File open?: ', sF.closed)
                    return

        #----------------------------------------▼
        #if the sender is not an admin, runs this                
        else:
            print('DEBUG: No Match')
            options = {'!yolo': command_yolo,
                       '!roulette': shoot_me_mofo,# ◄, (Reminder to replace comma if solution found for !commands)
                       '!commands': general_commands
                       }
            if split_msg[0] in options:
                options[split_msg[0]]()
                return

        


        ''' ▓ 2015-09-07 Temp Removal (Former Code) ▓
        #----------------------------------------▼ !commands [Admins]
        #checks to see if sender is an admin
        for user in adminList:
            if sender == user:
                options = {'!yolo': command_yolo,
                   '!swag': command_swag,
                   '!c': command_clear,
                   '!exit': command_leave,
                   '!roulette': shoot_me_mofo
                   }
                if split_msg[0] in options:
                    options[split_msg[0]]()
                    return
        #----------------------------------------▼                
        #if the sender is not an admin, runs the command
        hlink = 'http'
        if hlink in msg:
            command_purge(sender)
            send_message(CHAN, 'You were not authorized to do that, ' + sender)
        else:
            options = {'!yolo': command_yolo,
                       '!roulette': shoot_me_mofo
                    }
            if split_msg[0] in options:
                options[split_msg[0]]()'''

#------------------------------------------------▼ Terminate Script Timer

def countdown(sec):
    print('Bot DISABLED!') 
    while (sec >= 0):
        print('Terminating script in:', sec,'seconds.')
        sec -= 1
        time.sleep(1)
    if sec == -1:
        part_channel(CHAN)
        print('Safe to end this Process.')
        sys.exit()

#------------------------------------------------▼

data = ""

s = socket.socket()
s.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
capreq_membership()
capreq_commands()
#capreq_tags()
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

                    print(sender + ": " + message)
                if line[1] == 'JOIN':
                    sender = get_sender(line[0])
                    send_message(CHAN, 'Welcome '+sender+'! Ya Scrub')

            while ENGAGE == False:
                print('I have arrived in ' + CHAN + "'s channel!")
                arrive_message()
                time.sleep(1)
                ENGAGE = True
        time.sleep(MAXSENDINTERVAL)


        
                    
    except socket.error:
        print("Socket lost")

    except socket.timeout:
        print("Socket timeout")

