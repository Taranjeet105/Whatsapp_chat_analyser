import streamlit as st
import preprocess
import stats
import matplotlib.pyplot as plt
st.sidebar.title('Whats app chat analyser')

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     bytes_data = uploaded_file.getvalue()
     chats=bytes_data.decode('utf-8')
     chats_df=preprocess.convertToDf(chats)
     st.dataframe(chats_df)

     users=chats_df['user'].unique().tolist()
     users.remove('group_notification')
     users.sort()
     users.insert(0,'overall')
     selected_user=st.sidebar.selectbox('analysis for',users)
     messages_count,words_count,media_count,links_count=stats.stats(selected_user,chats_df)

     # for basic stats
     if st.sidebar.button('Analyse'):

          col1,col2,col3,col4=st.columns(4)

          with col1:
               st.header('Total messages')
               st.title(messages_count)
          with col2:
               st.header('Total words')
               st.title(words_count)
          with col3:
               st.header('Media shared')
               st.title(media_count)
          with col4:
               st.header('Links Shared')
               st.title(links_count)
     if selected_user=='overall':
          busy_users,busy_users_df=stats.busyUsers(chats_df)
          x=busy_users.index
          y=busy_users.values
          fig,ax=plt.subplots()
          # ax.xticks(rotation='vertical')
          col1,col2=st.columns(2)

          with col1:
               st.header('Busy users')
               plt.xticks(rotation='vertical')
               ax.bar(x,y)
               st.pyplot(fig)
          with col2:
               st.header('Messages percentage')
               st.dataframe(busy_users_df)
     st.header('Most frequently used words')
     
     col1,col2=st.columns(2)
     
     with col1:
          
          frequently_used_words_df=preprocess.mostCommonWords(selected_user,chats_df)
          st.dataframe(frequently_used_words_df)
     with col2:
          fig,ax=plt.subplots()
          ax.barh(frequently_used_words_df[0],frequently_used_words_df[1])
          plt.xticks(rotation='vertical')
          st.pyplot(fig)
          
          
     