from urlextract import URLExtract
urlExtractor=URLExtract()
def stats(selected_user,df):
    if(selected_user!='overall'):
        df=df[df['user']==selected_user]
    total_words=[]

        #total messages
    messages_count=df.shape[0]
        #media count
    media_count=df[df['message']=='<Media omitted>\n'].shape[0]

        #words count
    urls=[]
    for word in df['message']:
        urls.extend(urlExtractor.find_urls(word))
        total_words.extend(word.split())
            
    total_words_written=len(total_words)
    total_links_shared=len(urls)
    return messages_count,total_words_written,media_count,total_links_shared

def busyUsers(df):
    busy_users_df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
    columns={'index':'name',
             'user':'percentage'
            })
    return df['user'].value_counts().head(),busy_users_df