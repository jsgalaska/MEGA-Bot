# bot.py

"""import cfg"""
import socket
import re
import time

HOST = "irc.twitch.tv"              # the Twitch IRC server
PORT = 6667                         # always use port 6667!
NICK = "shuabot"            # your Twitch username, lowercase
PASS = "oauth:" # your Twitch OAuth token
CHAN = "#xshadow421x"                   # the channel you want to join
RATE = (20.0/30) # messages per second
CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# network functions go here

s = socket.socket()
s.connect((HOST, PORT))
s.send("PASS {}\r\n".format(PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        print (response)
        username = re.search(r"\w+", response).group(0) # return the entire match
        message = CHAT_MSG.sub("", response)
        print(username + ": " + message)
    time.sleep(1 / RATE)
    

