# bot.py

import socket
import re

HOST = "irc.twitch.tv"              # the Twitch IRC server
PORT = 6667                         # always use port 6667!
NICK = "nick"            # your Twitch username, lowercase
PASS = "oauth:" # your Twitch OAuth token
CHAN = "#chan"                   # the channel you want to join


#-------------------------------------------------

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

def command_yolo():
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, 'swag'), 'UTF-8'))

def command_test():
    s.send(bytes("PRIVMSG %s :%s\r\n" %(CHAN, 'test'), 'UTF-8'))


#------------------------------------------------

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
        
def parse_message(msg):
    if len(msg) >= 1:
        msg = msg.split(' ')
        options = {'!yolo': command_yolo,
                   '!test': command_test,
                   }
        if msg[0] in options:
            options[msg[0]]()

#------------------------------------------------------
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
                    parse_message(message)

                    print(sender + ": " + message)


        
                    
    except socket.error:
        print("Socket lost")

    except socket.timeout:
        print("Socket timeout")

