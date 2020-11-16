import os
import time
from subprocess import PIPE, Popen
from MessageListener import getMostRecentText,getMostRecentSender
from credentials import iMessageEmail,myChar
import sys
import atexit

def goodbye():
    f = open("terminalInUse.txt", "w")
    f.write("0")
    f.close()

atexit.register(goodbye)

def removeQuotes(s):
    s = str(s)
    s = s.replace("'","")
    s = s.replace('"',"")
    s = s.replace("`","")
    s = s.strip("'").strip("`").strip('"')
    return s

def newSession(message,sender,conn):
    inform = 'osascript -e \'tell application "Messages" \n send \"Welcome to terminal!\" to buddy "{}" of service "E:{}" \n end tell\''.format(sender,iMessageEmail)
    os.system(inform)
    message = message[1:]
    last = message
    lastOutput = ""
    while True:
        message = getMostRecentText(conn)
        if (message=="quit"):
            f = open("terminalInUse.txt", "w")
            f.write("0")
            inform = 'osascript -e \'tell application "Messages" \n send \"bye!\" to buddy "{}" of service "E:{}" \n end tell\''.format(sender,iMessageEmail)
            os.system(inform)
            f.close()
            sys.exit("session ended successfully")
        if message[0] == 'ä':
            p = Popen(message[1:],shell=True, stdout=PIPE, stderr=PIPE) #get output of command
            stdout, stderr = p.communicate()
            if(stdout):
                try:
                    output = stdout.decode('ascii') # [-1] excludes the return character
                except:
                    output = "There was an error."
            else:
                try:
                    output = stderr.decode('ascii')
                except:
                    output = "There was an error."
            #print("lets go")
            lastOutput = output
            inform = 'osascript -e \'tell application "Messages" \n send \"{}\" to buddy "{}" of service "E:{}" \n end tell\''.format(removeQuotes(output),sender,iMessageEmail)
            os.system(inform)
            last = message
        time.sleep(0.5)
