import re
import pandas as pd
from collections import Counter
def convertToDf(chats):
    regexPattern="\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s\S\S\s-"
    messages=re.split(regexPattern,chats)[1:]         #  12/4/21, 5:22 PM - 
    dates=re.findall(regexPattern,chats)               # 12/4/21, 8:45 PM - 
    whatsAppChats_df=pd.DataFrame({'date and time':dates,'messages':messages})

    #converting date and time column to date and time object
    whatsAppChats_df['date and time']=pd.to_datetime(whatsAppChats_df['date and time'],format='%m/%d/%y, %I:%M %p -')
    # spliting name of user from the messages
    users = []
    messages = []
    for message in whatsAppChats_df['messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:   # group notification
            users.append('group_notification')
            messages.append(entry[0])

    whatsAppChats_df['user'] = users
    whatsAppChats_df['message'] = messages
    whatsAppChats_df.drop(columns=['messages'], inplace=True)
    whatsAppChats_df['year']=whatsAppChats_df['date and time'].dt.year
    whatsAppChats_df['month']=whatsAppChats_df['date and time'].dt.month_name()
    whatsAppChats_df['day']=whatsAppChats_df['date and time'].dt.day
    whatsAppChats_df['hour']=whatsAppChats_df['date and time'].dt.hour
    whatsAppChats_df['minute']=whatsAppChats_df['date and time'].dt.minute
    return whatsAppChats_df

def mostCommonWords(selected_user,df):
    if(selected_user!='overall'):
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    f=open('./hinglish_stop_words.txt','r')
    stopwords=f.read()
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if(word not in stopwords):
                words.append(word)
    
    return pd.DataFrame(Counter(words).most_common(20))
