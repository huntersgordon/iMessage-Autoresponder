import time
import os
import sqlite3
from MessageListener import getMostRecentText,isFromMe,getMostRecentSender
import CommandProcess

#connect to iMessage SQLite3 database
conn = sqlite3.connect(os.path.expanduser("~") + '/Library/Messages/chat.db') #or your username
cur = conn.cursor()

last = getMostRecentText(conn)
while(True):
    new = getMostRecentText(conn)
    if(new!=last):
        print("text: " + new)
        CommandProcess.processResponse(new,isFromMe(conn),getMostRecentSender(conn)[0],conn)
        last = new
    time.sleep(0.5)
