# bot.py

import cfg, socket, re, time, sys

HOST = cfg.HOST
PORT = cfg.PORT
NICK = cfg.NICK
PASS = cfg.PASS
CHAN = cfg.CHAN

ENGAGE = False
approvedUsers = [cfg.USER1, cfg.USER2, cfg.USER3]
sec = cfg.sec # ◄ Set desired seconds to wait for script termination (Mine is set for 2)
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

def command_scrublords():
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

#------------------------------------------------▼ approvedUsers !commands [Admins]

def parse_message(sender, msg):
    if len(msg) >= 1:
        s1 = 'scrublords 4 life'
        if s1 in msg.lower():
            command_scrublords()
            
        
        admin = True
        split_msg = msg.split(' ')
        #checks to see if sender is an admin
        for user in approvedUsers:
            if sender == user:
                options = {'!yolo': command_yolo,
                   '!swag': command_swag,
                   '!c': command_clear,
                   '!exit': command_leave
                   }
                if split_msg[0] in options:
                    options[split_msg[0]]()
            else:
                admin = False
                
        #if the sender is not an admin, runs the commands
        if not admin:
            print ('here')
            hlink = 'http'
            if hlink in msg:
                command_purge(sender)
            else:
                options = {'!yolo': command_yolo,
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

