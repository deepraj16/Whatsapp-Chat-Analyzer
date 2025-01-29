from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud
import regex as re
from collections import Counter
import emoji


def fetch_stats(selected_user,df): 
    if selected_user != 'Overall' : 
        df=df[df['user']==selected_user]
        
    #message
    num_message =df.shape[0]
    #word
    word=[]
    for mess1 in df['message']: 
        word.extend(mess1.split())

    #media message 
    num_media_message=df[df['message']=="<Media omitted>', '"].shape[0]

    #links 
    extract =URLExtract()
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_message,len(word) ,num_media_message , len(links)

def most_busy_user(df): 
    x=df['user'].value_counts().head()
    return x 

def create_wordcloud(selected_user, df):  
    if selected_user != 'Overall': 
        df = df[df['user'] == selected_user]


    marathi_stopword =['ahe','la','te','ha','kare','mi']
    temp=df[df['user'] !='group_notif']
    temp=temp[temp['message']!="<Media omitted>', '" ] 
    f= open('hindlish_stopword.txt','r')
    stop_word=f.read().split('\n')


    # Fixing the typo in background_color
    wc = WordCloud(width=500, height=500, min_font_size=18, background_color='white')
    
    # Generate word cloud from the 'message' column
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_word(selected_user,df): 
    if selected_user != 'Overall': 
        df = df[df['user'] == selected_user]

    temp=df[df['user'] !='group_notif']
    temp=temp[temp['message']!="<Media omitted>', '" ] 
    f= open('hindlish_stopword.txt','r')
    stop_word=f.read().split('\n')

    words =[]

    f= open('hindlish_stopword.txt','r')
    stop_word=f.read().split('\n')
    marathi_stopword =['ahe','la','te','ha','kare','mi']
    for message1 in temp['message']: 
        for word in message1.lower().split():
            if word not in stop_word:
                if word not in marathi_stopword:
                    words.append(word)

    cleaned_list = [item for item in words if re.match(r'^[a-zA-Z\s]+$', item)]
    
    new_df=pd.DataFrame(Counter(cleaned_list).most_common(20))

    return new_df


def emoji_helper(selected_user,df): 
  
    if selected_user != 'Overall' : 
        df=df[df['user']==selected_user]


    emojis = []
    for i in df['message']:
        emojis.extend([c for c in i if c in emoji.EMOJI_DATA])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df



def monthly_timeline(selected_user,df):
    if selected_user != 'Overall' : 
        df=df[df['user']==selected_user]

    timeline=df.groupby(['year','month','month_num']).count()['message'].reset_index()
    time=[]
    
    for i in range(timeline.shape[0]): 
        time.append(timeline['month'][i] + "-"+str(timeline['year'][i]))
    
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df): 
    if selected_user != 'Overall' : 
        df=df[df['user']==selected_user]

    df['only_date']=df['date'].dt.date
    daily_time=df.groupby('only_date').count()['message'].reset_index()

    return daily_time

def week_activate_map(selected_user,df): 
    # most activat day 
    if selected_user != 'Overall' : 
        df=df[df['user']==selected_user]
    # most activat day 
    df['only_day']=df['date'].dt.day_name()
    k=df['only_day'].value_counts()
    return k


def month_activate_map(selected_user,df): 
    # most activat day 
    if selected_user != 'Overall' : 
        df=df[df['user']==selected_user]

    k=df['month'].value_counts()
    return k


    