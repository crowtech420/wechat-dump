#!/usr/bin/env python3

import pandas as pd
import sqlite3
conn = sqlite3.connect("decrypted.db")
db_df = pd.read_sql_query("SELECT createTime,isSend,Talker,content FROM message where type=1 and talker not like '%chatroom%' order by createTime ASC ;", conn)
uniquetalker = db_df.talker.unique().tolist()
for q in range(len(uniquetalker)):
	thisTalker = uniquetalker[q]
	thisquery = """SELECT createTime,isSend,Talker,content FROM message WHERE type=1 AND talker not like '%chatroom%' AND talker=""" + """'""" + thisTalker + """'""" + """ order by createTime ASC"""
	thisdf = pd.read_sql_query(thisquery, conn)
	

	for i in range(len(thisdf)-1):
		isSend = thisdf.iloc[i,1]
		nextisSend = thisdf.iloc[i+1,1]
		if int(isSend) != int(nextisSend):
			thisMessage = thisdf.iloc[i,3]
			nextMessage = thisdf.iloc[i+1,3]
			fname = "chat_" + thisTalker + ".tsv"
			with open(fname,"a") as f:
				f.write(thisMessage)
				f.write("\t")
				f.write(nextMessage)
				f.write("\n")