from datetime import datetime
import regex as re 
import pandas as pd 
def preprocessor(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages =data.split('\n')
    data=[]
    for i in range(len(messages)):
        data.append(messages[i].replace("\u202f", ""))
    message2 = []

    for i in range(len(data)):
        text = data[i]
        
        #"am" or "pm"
        text = text.replace("am", " am").replace("pm", " pm")
        #before the " - " separator)
        date_time_str = text.split(" - ")[0]

        try:
            date_time_obj = datetime.strptime(date_time_str, "%d/%m/%y, %I:%M %p")

            new_format = date_time_obj.strftime("%d/%m/%y, %H:%M")

            cleaned_text = text.replace(date_time_str, new_format)
        except ValueError:
            # If there's a ValueError, skip this message
            cleaned_text = text

        message2.append(cleaned_text)
    k=str(message2)
    m2 =re.split(pattern,k)[1:]
    datas=re.findall(pattern,k)

    # Example DataFrame
    df = pd.DataFrame({'user_message': m2, 'message_date': datas})

    # Convert message_date to datetime using the correct format for 2-digit year
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ', errors='coerce')

    # Rename the column to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    user = []
    mes3= []
    for mess in df['user_message']: 
        entry =re.split('([\w\W]+?):\s',mess)
        if entry[1:]: 
            user.append(entry[1])
            mes3.append(entry[2])
        else : 
            user.append("group_notif")
            mes3.append(entry[0])

    df['user'] =user 
    df['message']=mes3
    df.drop(columns=['user_message'],inplace=True)
    print(df['user'].value_counts())
    df['year']=df['date'].dt.year
    df['month_num'] =df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['min']=df['date'].dt.minute

    return df