import cfg, socket, re, time, sys, random

HOST = cfg.HOST
PORT = cfg.PORT
NICK = cfg.NICK
PASS = cfg.PASS
CHAN = cfg.CHAN

ENGAGE = False
adminList = [cfg.USER1, cfg.USER2, cfg.USER3]
sec = cfg.sec # ◄ Set desired seconds to wait for script termination (0 is 1 sec)
MAXSENDINTERVAL = 20.0/30

#------------------------------------------------▼ Emotes

angry = " >( "
bigsmile = " :D "  
bored = " :z "
confused = " o_O "
cool = "  B)  "
heart = " <3 "
sad = " :( "
smile = " :) "
tongue = " :P "
surprised = " :o "
undecided = " :\ "
wink = " ;p "
winking =" ;) "

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

mood = 0 # ◄ Leave as is

def mood_swing():
    mood = random.randint(1,7)
    if mood == 1:
        send_message(CHAN, 'Nice, ' + sender  + smile)
    elif mood == 2:
        send_message(CHAN, 'Fine, ' + sender  + tongue)
    elif mood == 3:
        send_message(CHAN, 'Not bad, ' + sender  + bored)
    elif mood == 4:
        send_message(CHAN, 'OK, ' + sender   + undecided)
    elif mood == 5:
        send_message(CHAN, 'Not sure, ' + sender   + confused)
    elif mood == 6:
        send_message(CHAN, 'Fustrated, ' + sender   + ' PJSalt')
    elif mood == 7:
        send_message(CHAN, "I'm doing wonderfully, " + sender + '. Just observing these MLG-pro, players'  + ' Kappa')

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
    if  chamber == 1 and cylinder == chamber:
        time.sleep(1)
        send_message(CHAN, sender + ' JUST GOT REKT!!')
        command_purge(sender)
    elif  chamber == 2 and cylinder == chamber:
        time.sleep(1)
        send_message(CHAN, sender + ' JUST GOT REKT!!')
        command_purge(sender)
    elif  chamber == 3 and cylinder == chamber:
        time.sleep(1)
        send_message(CHAN, sender + ' JUST GOT REKT!!')
        command_purge(sender)
    elif  chamber == 4 and cylinder == chamber:
        time.sleep(1)
        send_message(CHAN, sender + ' JUST GOT REKT!!')
        command_purge(sender)
    elif  chamber == 5 and cylinder == chamber:
        time.sleep(1)
        send_message(CHAN, sender + ' JUST GOT REKT!!')
        command_purge(sender)
    elif  chamber == 6 and cylinder == chamber:
        time.sleep(1)
        send_message(CHAN, sender + ' JUST GOT REKT!!')
        command_purge(sender)
    else:
        send_message(CHAN, sender + ', you got lucky this time, scrub!')
        print('Bullet in:', chamber, 'of 6', 'Rotated to:', cylinder, 'of 6')
#------------------------------------------------▼

def parse_message(sender, msg):
    if len(msg) >= 1:
        s1 = 'scrublord 4 life'
        hau = 'how art thou ' + NICK
        if s1 in msg.lower():
            command_scrublord()
        elif hau in msg.lower():
            mood_swing()
                    
        split_msg = msg.split(' ')
#------------------------------------------------▼ !commands [Admins]
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
#------------------------------------------------▼                
        #if the sender is not an admin, runs the command
        hlink = 'http'
        if hlink in msg:
            command_purge(sender)
        else:
            options = {'!yolo': command_yolo,
                       '!roulette': shoot_me_mofo
                    }
            if split_msg[0] in options:
                options[split_msg[0]]()

#------------------------------------------------▼ Terminate script Timer

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
join_channel(CHAN)

print('loading')

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

