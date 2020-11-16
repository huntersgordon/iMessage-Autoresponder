import time
import sqlite3
import pandas as pd
from credentials import iMessageEmail,iMessagePhone

################################################################

def getMostRecentText(conn):
    return pd.read_sql_query("select text from message ORDER BY ROWID DESC limit 1",conn)['text'][0]

def isFromMe(conn):
    return bool(pd.read_sql_query("select is_from_me from message ORDER BY ROWID DESC limit 1",conn)['is_from_me'][0])

def getMostRecentSender(conn):
    #return sender "guid". Also returns who the recent sender was (an iMessage, SMS, or groupchat), then whether it is from you
    isItFromMe = isFromMe(conn)
    if (isItFromMe):
        return iMessagePhone,1,isItFromMe
    rowID = pd.read_sql_query("select ROWID from message ORDER BY ROWID DESC limit 1",conn)['ROWID'][0]
    chatID = pd.read_sql_query("select chat_id from chat_message_join where message_id={}".format(rowID),conn)["chat_id"][0]
    raw_phone_number = pd.read_sql_query("select guid from chat where ROWID={}".format(chatID),conn)["guid"][0]
    if ("chat" in raw_phone_number):
        return raw_phone_number,3,isItFromMe
    if(raw_phone_number[0:8] == "iMessage"):
        return raw_phone_number[raw_phone_number.rindex(';')+1:],1,isItFromMe
    else:
        #it's an sms
        return raw_phone_number[raw_phone_number.rindex(';')+1:],2,isItFromMe
    return
