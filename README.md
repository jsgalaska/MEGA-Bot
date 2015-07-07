# MEGA-Bot

A simple irc chat bot designed to interact with Twitch chat


A cfg.py file needs to be created in the same directory as bot.py in order to run the program.
It must contain the following variables:

HOST = "irc.twitch.tv"              # the Twitch IRC server
PORT = 6667                         # always use port 6667!
NICK = "nick"                       # your Twitch username, lowercase
PASS = "oauth:"                     # your Twitch OAuth token
CHAN = "#chan"                      # the channel you want to join
