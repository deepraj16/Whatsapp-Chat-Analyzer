import streamlit as st  
import preprocesser ,helper
import matplotlib.pyplot as plt 
from wordcloud import WordCloud




st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file =st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None :
    byter_data =uploaded_file.getvalue()
    data =byter_data.decode("utf-8")
    df = preprocesser.preprocessor(data)
    # st.dataframe(df)
    #user 
    user_list=df['user'].unique().tolist() 
    user_list.remove('group_notif')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        num_message  ,word  ,num_media  , link=helper.fetch_stats(selected_user,df)
        st.title("Top Staticstics")
        col1 ,col2,col3,col4 = st.columns(4)

        
        with col1:
            st.header("Total Message")
            st.title(num_message)

        with col2:
            st.header("Total Word")
            st.title(word)

        with col3:
            st.header("Media shared")
            st.title(num_media)

        with col4:
            st.header("Total Links")
            st.title(link)


        #monthy time line
        st.title("")
        st.title("Monthly Timeline")
        timeline =helper.monthly_timeline(selected_user,df)
        fig,ax =plt.subplots()
        plt.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timelint 
        st.title("")
        st.title("Daily Timeline")
        da_timeline =helper.daily_timeline(selected_user,df)
        fig,ax =plt.subplots()
        plt.plot(da_timeline['only_date'],da_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # bubsy day 
        st.title("Activate Map")
        col1 ,col2 =st.columns(2)

        with col1: 
            st.header("most Busy day")
            busy_day =helper.week_activate_map(selected_user,df)
            fig,ax =plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2: 
            st.header("most Bauy month")
            busy_m =helper.month_activate_map(selected_user,df)
            fig,ax =plt.subplots()
            ax.bar(busy_m.index,busy_m.values,color='orange')
            st.pyplot(fig)

        # most use active time

        st.text("")
        if selected_user =="Overall" :
        #top Busy five user 
            st.title("Most Busy user")
            x=helper.most_busy_user(df)
            fig,ax =plt.subplots()
            

            col1,col2 = st.columns(2)

            with col1: 
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2: 
                k=round(df['user'].value_counts()/df.shape[0]*100).reset_index()
                k=k.head()
                st.dataframe(k,width=700, height=300)

        st.text("")
        st.title("Word cloud")
        df_wc =helper.create_wordcloud(selected_user,df)

        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')  # Hide the axes for better display

        # Display the plot in Streamlit
        st.pyplot(fig)



        #most common word most
        st.title("")
        st.title("Most common words in chat")
        most_common_df =helper.most_common_word(selected_user,df)
        fig,ax =plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emojo anyl

        emoji_df =helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2 =st.columns(2)
        with col1:
            st.dataframe(emoji_df ,height=400,width=300)


        with col2: 
            fig,ax =plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)


#time base anlyiss
#total message ,links ,sentance ,emojis
