#!/usr/bin/env python3

import pandas as pd
import sqlite3
conn = sqlite3.connect("decrypted.db")
db_df = pd.read_sql_query("SELECT createTime,isSend,Talker,content FROM message where type=1 and talker not like '%chatroom%' and talker='wxid_6560135560212' order by createTime ASC ;", conn)
print(db_df)
for i in range(len(db_df)-1):
	isSend = db_df.iloc[i,1]
	nextisSend = db_df.iloc[i+1,1]
	if int(isSend) != int(nextisSend):
		thisMessage = db_df.iloc[i,3]
		nextMessage = db_df.iloc[i+1,3]
		with open("chat.tsv","a") as f:
			f.write(thisMessage,nextMessage)
			f.write("\n")