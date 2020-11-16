###Process Commands and send back output
#import sendMessage
import SongDownloader
import os,signal
import sys
from credentials import iMessageEmail,iMessagePhone,myChar
import iMessageTerminal
from MessageListener import getMostRecentText
import time

def processResponse(message,isItFromMe,sender,conn):
    #########################~~~~PLACE YOUR CUSTOM FUNCTIONS HERE~~~~#########################
    if(message == "exit" and isItFromMe):
        #sendMessage.messageSend("goodbye...",sender)
        exit()
    if (str.lower(message[0:4]) == "song"):
            pid=os.fork()
            if pid == 0 : #child process
                SongDownloader.songGetter(message,sender)
                os._exit(os.EX_OK)
    if (str.lower(message) == "clear" and isItFromMe):
            os.system("python3 clearChat.py {} {}".format(iMessagePhone,iMessageEmail))

    if (message[0:4] == "send"):
        print("sending file...")
        theFile = message[5:]
        inquiry = "osascript sendFile.scpt \"{}\" \"E:{}\" \"$(pwd)/{}\"".format(sender,iMessageEmail,theFile)
        os.system(inquiry)
    cantUse=False
    if (message[0] == myChar):
        #check if terminal in use
        with open('terminalInUse.txt') as f:
            if '1' in f.read():
                cantUse = True
        if cantUse == False:
            pid=os.fork()
            f = open("terminalInUse.txt", "w")
            f.write("1")
            f.close()
            if pid == 0 : #child process
                iMessageTerminal.newSession(message,sender,conn)
                sys.exit("child process \"iMessage terminal\" terminated")
                os._exit(os.EX_OK)