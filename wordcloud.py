# -*- coding: utf-8 -*-
import pandas as pd
import pkuseg
import matplotlib.pyplot as plt
from wordcloud import WordCloud
seg = pkuseg.pkuseg()
worddump = ""
contactList = pd.read_csv("contacts.csv")
messageList = pd.read_csv("messages.csv")
content = (messageList["content"])
for i in range(len(content)):
    thisseg = seg.cut(str(content[i]))
    for q in range(len(thisseg)):
        worddump+=thisseg[q]
        worddump+=" "
wordcloud = WordCloud(font_path="SimHei.ttf",background_color="white",width=1920,height=1080,max_words = 1000).generate(worddump)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
wordcloud.to_file('white.png')