import os,signal
import time
import sqlite3
import pandas as pd
from credentials import iMessageEmail,iMessagePhone
from MessageListener import getMostRecentSender,getMostRecentText
import sys

conn = sqlite3.connect(os.path.expanduser("~") + '/Library/Messages/chat.db') #or your username
cur = conn.cursor()

def removeQuotes(s):
    s = str(s)
    s = s.replace("'","")
    s = s.replace('"',"")
    s = s.replace("`","")
    s = s.strip("'").strip("`").strip('"')
    return s

def songGetter(new,sender):
    songRequest = new[5:]
    songResults = removeQuotes(os.popen("cd song; node search.js \"{}\"".format(songRequest)).read()[:-1])
    #print("song results are: " + songResults)
    sendResults = 'osascript -e \'tell application "Messages" \n send \"{}\" to buddy \"{}\" of service "E:{}" \n end tell\''.format(songResults,sender,iMessageEmail)
    os.system(sendResults)
    sendResults = 'osascript -e \'tell application "Messages" \n send \"𝕡𝕝𝕖𝕒𝕤𝕖 𝕤𝕖𝕝𝕖𝕔𝕥 𝕥𝕙𝕖 𝕟𝕦𝕞𝕓𝕖𝕣 𝕪𝕠𝕦 𝕨𝕚𝕤𝕙 𝕥𝕠 𝕕𝕠𝕨𝕟𝕝𝕠𝕒𝕕\" to buddy \"{}\" of service "E:{}" \n end tell\''.format(sender,iMessageEmail)
    os.system(sendResults)
    last = pd.read_sql_query("select text from message ORDER BY ROWID DESC limit 1",conn)['text'][0]
    songIndex = ""
    while True:
        new = pd.read_sql_query("select text from message ORDER BY ROWID DESC limit 1",conn)['text'][0]
        if (new!=last and getMostRecentSender(conn)[0] == sender): #there is a new message from the sender
            if (not str.isdigit(new) or (int(new) > 9 or int(new) < 0)): #check for alphanumeric
                    print("quitting because last message was " + new)
                    inform = 'osascript -e \'tell application "Messages" \n send \"quitting...\" to buddy "{}" of service "E:{}" \n end tell\''.format(sender,iMessageEmail)
                    os.system(inform)
                    os._exit()
                    print("hoodtown")
                    sys.exit()
            songIndex = int(new)
            break
        time.sleep(0.5) #or a desired resolution
    inform = 'osascript -e \'tell application "Messages" \n send \"Downloading song {}. Type cancel to cancel\" to buddy "{}" of service "E:{}" \n end tell\''.format(songIndex,sender,iMessageEmail)
    os.system(inform)
    fp = open("song/links.txt")
    for i, line in enumerate(fp):
        if i == int(songIndex):
            songLink = line
    fp.close()
    pid = os.fork()
    if pid == 0:
        #attempt to donwload the song under this child process
        os.system("youtube-dl --output \"song.%(ext)s\" --quiet --extract-audio --embed-thumbnail --audio-format mp3 \'{}\'".format(songLink))
        os.system("osascript sendSong.scpt \"{}\"".format(sender))
        inform = 'osascript -e \'tell application "Messages" \n send \"Process {} complete.\" to buddy "{}" of service "E:{}" \n end tell\''.format(os.getpid(),sender,iMessageEmail)
        os.system(inform)
        os._exit(os.EX_OK)
        sys.exit()
    else:
        ##parent process
        count = 0
        while True:
            mostRecent = getMostRecentText(conn)
            if (count > 400):
                break
            if ((mostRecent == "cancel") and (getMostRecentSender(conn)[0] == sender)):
                print("cancelling")
                inform = 'osascript -e \'tell application "Messages" \n send \"Download cancelled successfully.\" to buddy "{}" of service "E:{}" \n end tell\''.format(sender,iMessageEmail)
                os.system(inform)
                os.kill(pid, signal.SIGSTOP)
                sys.exit()
            if (str(pid) in mostRecent or ("quitting" in mostRecent)):
                print("ending")
                os.kill(pid, signal.SIGSTOP)
                sys.exit()

            time.sleep(0.5)
            count += 0.5
    print("song downloaded")
