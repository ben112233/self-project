import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import re
import seaborn as sns
from datetime import datetime
from matplotlib.ticker import MaxNLocator
#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#extract date time
def get_date_time(new_line):
    import re
    date = []
    time = []
    a = []
    for line in new_line:
        tmp = re.search('^(.+)(AM|PM)', line)
        if tmp != None:
            a.append(tmp.group())
    for a in a:
        date.append(a.split(',')[0])
        time.append(a.split(',')[1].strip())
    return date, time
#get_date_time(new_line) ##tuple of list for date and time

#combine and remove line
def combine_line(new_line):
    import re
    a = []
    for index, line in enumerate(new_line):
        t = re.search('^(.+)(AM|PM)', line)
        if t == None:
            a.append(index)

    #print(a)
    c = []
    e = []
    tmp = []
    for index, aa in enumerate(a):
        e.append(new_line[aa])
        if index in range(len(a) - 1):
            if a[index + 1] == aa + 1:
                c.append((aa, aa + 1))
                tmp.append(aa)
                tmp.append(aa + 1)

    tmp = list(dict.fromkeys(tmp))
    #print(c)
    #print(tmp)

    d = []
    for index, cc in enumerate(c):
        if index in range(len(c) - 1):
            if c[index + 1][0] == cc[1]:
                d.append((cc[0], c[index + 1][1]))
            else:
                d.append(cc)

    #print(d) # all need to merge back to the main sentence line(if tuple is (3,4) it will need to merge with 2)
    for dd in d:
        diff = dd[1] - dd[0] #diff + 1 will be the number needed to iterate
        if diff == 1:
            new_line[dd[0] - 1] = new_line[dd[0] - 1] + ' ' + new_line[dd[0]] + ' ' + new_line[dd[1]]
        elif diff > 1:
            new_line[dd[0] - 1] = new_line[dd[0] - 1] + ' ' + new_line[dd[0]]
            for i in range(diff):
                new_line[dd[0] - 1] = new_line[dd[0] - 1] + ' ' + new_line[dd[0] + i + 1]

    tmp1 = []
    for aa in a:
        if aa not in tmp:
            tmp1.append(aa)
    tmp = tmp1
    #print(tmp)

    for index, value in enumerate(tmp):
        new_line[value - 1] = new_line[value - 1] + ' ' + new_line[value]

    #remove line
    #print(e)
    for ee in e:
        new_line.remove(ee)
    return new_line
#combine_line(new_line)

#extract author
def aut(line):
    import re
    a = []
    aut = []
    for l in line:
        a = l.split(': ')[0]
        if re.search('^.+(AM)', a):
            aut.append(a.split('AM ')[-1])
        elif re.search('^.+(PM)', a):
            aut.append(a.split('PM ')[-1])
    return aut
#author(line)

#message
def mess(line):
    mess = []
    for line in line:
        mess.append(line.split(': ')[1:])
    return mess

def transform(df):
    df.message = df.message.apply(lambda x: ''.join(x))
    df.message = df.message.apply(lambda x: x.strip().split('\n'))
    df['length'] = df.message.apply(lambda x: len(x))
    df.message = df.message.apply(lambda x: ''.join(x))
    df.date = pd.to_datetime(df.date)

    #transform date
    weeks = {0 : 'Monday', 1 : 'Tuesday', 2 : 'Wednesday', 3 : 'Thrusday', 4 : 'Friday', 5 : 'Saturday', 6 : 'Sunday'}
    df['day'] = df['date'].dt.weekday.map(weeks)
    df['day'] = df['day'].astype('category')

    #count word
    df['word'] = df.message.apply(lambda x: len(x)) - df.length + 1

    # count url
    URLPATTERN = r'(https?://S+)'
    df['url_count'] = df.message.apply(lambda x: re.findall(URLPATTERN, x)).str.len()
    links = np.sum(df.url_count)

    ### Function to count number of media in chat.
    MEDIAPATTERN = r'<Media omitted>'
    df['media_count'] = df.message.apply(lambda x : re.findall(MEDIAPATTERN, x)).str.len()
    media = np.sum(df.media_count)

    # convert unknown phone number to 'unknown'
    df.author = df.author.apply(lambda x: str('unknown' if re.search('(\+)', x) else x))
    
    lst = []
    for i in df['time']:
        out_time = datetime.strftime(datetime.strptime(i,"%I:%M:%S %p"),"%H:%M:%S")
        lst.append(out_time)
    df['24H_Time'] = lst
    df['Hours'] = df['24H_Time'].apply(lambda x : x.split(':')[0])
    
    df['Year'] = df['date'].dt.year
    df['Mon'] = df['date'].dt.month
    months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    df['Month'] = df['Mon'].map(months)
    df.drop('Mon',axis=1,inplace=True)
    
    return df
#df['word'] = df.message.apply(lambda x : len(x.split(' ')))
#df = df[['date', 'day', 'time', 'author', 'message', 'length']]

def basic_info(df):
    total_messages = df.shape[0]
    media_messages = df[df['message'] == '<Media omitted>'].shape[0]
    links = np.sum(df.url_count)
    print('Group Chatting Stats : ')
    print('Total Number of Messages : {}'.format(total_messages))
    print('Total Number of Media Messages : {}'.format(media_messages))
    print('Total Number of Links : {}'.format(links))
#basic_info(df)

def get_author_info(df):
    l = df.author.unique()
    for i in range(len(l)):
        ### Filtering out messages of particular user
        req_df = df[df["author"] == l[i]]
        ### req_df will contain messages of only one particular user
        print(f'--> Stats of {l[i]} <-- ')
        ### shape will print number of rows which indirectly means the number of messages
        print('Total Message Sent : ', req_df.shape[0])
        ### Word_Count contains of total words in one message. Sum of all words/ Total Messages will yield words per message
        words_per_message = (np.sum(req_df['word']))/req_df.shape[0]
        w_p_m = ("%.3f" % round(words_per_message, 2))  
        print('Average Words per Message : ', w_p_m)
        ### media conists of media messages
        media = sum(req_df["media_count"])
        print('Total Media Message Sent : ', media)
        ### links consist of total links
        links = sum(req_df["url_count"])   
        print('Total Links Sent : ', links)   
        print()
        print('----------------------------------------------------------n')
#get_author_info(df)

def analysis_on_day(df):
    l = df.day.unique()
    for i in range(len(l)):
        ### Filtering out messages of particular user
        req_df = df[df["day"] == l[i]]
        ### req_df will contain messages of only one particular user
        print(l[i],'  ->  ',req_df.shape[0])
        
    ### Mostly Active day in the Group
    plt.figure(figsize=(8,5))
    active_day = df['day'].value_counts()
    ### Top 10 peoples that are mostly active in our Group is : 
    a_d = active_day.head(10)
    a_d.plot.bar()
    plt.xlabel('Day',fontdict={'fontsize': 12,'fontweight': 10})
    plt.ylabel('No. of messages',fontdict={'fontsize': 12,'fontweight': 10})
    plt.title('Mostly active day of Week in the Group',fontdict={'fontsize': 18,'fontweight': 8})
    return plt.savefig('static/images/analysis_on_day.png')
#analysis_on_day(df)

def get_most_active_member(df):    
    ### Mostly Active Author in the Group
    plt.figure(figsize=(9,6))
    mostly_active = df['author'].value_counts()
    ### Top 10 peoples that are mostly active in our Group is : 
    m_a = mostly_active.head(10)
    bars = m_a.index
    x_pos = np.arange(len(bars))
    m_a.plot.bar()
    plt.xlabel('Authors',fontdict={'fontsize': 14,'fontweight': 10})
    plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
    plt.title('Mostly active member of Group',fontdict={'fontsize': 20,'fontweight': 8})
    plt.xticks(x_pos, bars)
    return plt.savefig('static/images/get_most_active_member.png')
#get_most_active_member(df)

def most_media_by_author(df):
    ### Top-10 Media Contributor of Group
    mm = df[df['message'] == '<Media omitted>']
    if not mm.empty:
        mm1 = mm['author'].value_counts()
        bars = mm1.index
        x_pos = np.arange(len(bars))
        top10 = mm1.head(10)
        top10.plot.bar()
        plt.xlabel('Author',fontdict={'fontsize': 12,'fontweight': 10})
        plt.ylabel('No. of media',fontdict={'fontsize': 12,'fontweight': 10})
        plt.title('Top-10 media contributor of Group',fontdict={'fontsize': 18,'fontweight': 8})
        plt.xticks(x_pos, bars)
        return plt.savefig('static/images/most_media_by_author.png')
    else:
        print('no media data')
        mm1 = mm['author'].value_counts()
        bars = mm1.index
        x_pos = np.arange(len(bars))
        plt.xlabel('Author',fontdict={'fontsize': 12,'fontweight': 10})
        plt.ylabel('No. of media',fontdict={'fontsize': 12,'fontweight': 10})
        plt.title('Top-10 media contributor of Group',fontdict={'fontsize': 18,'fontweight': 8})
        plt.xticks(x_pos, bars)
        return plt.savefig('static/images/most_media_by_author.png')
#most_media_by_author(df)

def get_most_word_by_author(df):    
    max_words = df[['author','word']].groupby('author').sum()
    m_w = max_words.sort_values('word',ascending=False).head(10)
    bars = m_w.index
    x_pos = np.arange(len(bars))
    m_w.plot.bar(rot=90)
    plt.xlabel('Author')
    plt.ylabel('No. of words')
    plt.title('Analysis of members who has used max. no. of words in his/her messages')
    plt.xticks(x_pos, bars)
    return plt.savefig('static/images/get_most_word_by_author.png')
#get_most_word_by_author(df)

def no_link_share(df):
    ### Member who has shared max numbers of link in Group 
    max_words = df[['author','url_count']].groupby('author').sum()
    m_w = max_words.sort_values('url_count',ascending=False).head(10)
    bars = m_w.index
    x_pos = np.arange(len(bars))
    m_w.plot.bar(rot=90)
    plt.xlabel('Author')
    plt.ylabel('No. of link')
    plt.title('Analysis of member who has shared max no. of link in Group')
    plt.xticks(x_pos, bars)
    return plt.savefig('static/images/no_link_share.png')
#no_link_share(df)

def active_hour(df):    
    ### Most suitable hour of day, whenever there will more chances of getting responce from group members.
    plt.figure(figsize=(8,5))
    std_time = df['Hours'].value_counts().head(15)
    s_T = std_time.plot.bar()
    s_T.yaxis.set_major_locator(MaxNLocator(integer=True))  #Converting y axis data to integer
    plt.xlabel('Hours (24-Hour)',fontdict={'fontsize': 12,'fontweight': 10})
    plt.ylabel('No. of messages',fontdict={'fontsize': 12,'fontweight': 10})
    plt.title('Most suitable hour of day.',fontdict={'fontsize': 18,'fontweight': 8})
    return plt.savefig('static/images/active_hour.png')
#active_hour(df)

def active_date(df):    
    ### Date on which our Group was highly active.
    plt.figure(figsize=(8,5))
    df['date'].value_counts().head(15).plot.bar()
    plt.xlabel('Date',fontdict={'fontsize': 14,'fontweight': 10})
    plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
    plt.title('Analysis of Date on which Group was highly active',fontdict={'fontsize': 18,'fontweight': 8})
    return plt.savefig('static/images/active_date.png')
#active_date(df)

def graph_of_message_vs_month(df):
    z = df['date'].value_counts() 
    z1 = z.to_dict() #converts to dictionary
    df['Msg_count'] = df['date'].map(z1)
    ### Timeseries plot 
    plt.plot(df['date'],df['Msg_count'], marker='o')
    plt.title('Analysis of number of message using TimeSeries plot.')
    plt.xlabel('Month')
    plt.ylabel('No. of Messages')
    return plt.savefig('static/images/graph_of_message_vs_month.png')
#graph_of_message_vs_month(df)

def active_month(df):    
    z = df['Month'].value_counts() 
    z1 = z.to_dict() #converts to dictionary
    df['Msg_count_monthly'] = df['Month'].map(z1)
    plt.figure(figsize=(18,9))
    sns.set_style("darkgrid")
    sns.lineplot(data=df,x='Month',y='Msg_count_monthly',markers=True,marker='o')
    plt.xlabel('Month',fontdict={'fontsize': 14,'fontweight': 10})
    plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
    plt.title('Analysis of mostly active month using line plot.',fontdict={'fontsize': 20,'fontweight': 8})
    return plt.savefig('static/images/active_month.png')
#active_month(df)

def message_vs_year(df):
    ### Total message per year
    ### As we analyse that the group was created in mid 2019, thats why number of messages in 2019 is less.
    plt.figure(figsize=(12,6))
    active_month = df['Year'].value_counts()
    a_m = active_month
    print(a_m)
    print(a_m.max())
    a_m.plot.bar()
    plt.xlabel('Year',fontdict={'fontsize': 14,'fontweight': 10})
    plt.ylabel('No. of messages',fontdict={'fontsize': 14,'fontweight': 10})
    plt.title('Analysis of mostly active year.',fontdict={'fontsize': 20,'fontweight': 8})
    return plt.savefig('static/images/message_vs_year.png')
#message_vs_year(df)

def empty():
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    x = [1, 2, 3, 4]
    ax1 = plt.subplot()
    ax1.set_xticks(x)
    ax1.set_xticklabels(["one", "two", "three", "four"])
    print("Empty tick labels: ", ax1.get_xticklabels(which='minor'))
    plt.show()
    return plt.savefig('static/images/empty.png')

def main():
    #main
    lines = []
    with open('text.txt', encoding="utf-8") as f:
        lines = f.readlines()

    new_line = []    
    for line in lines:
        if (line[0] == '[') and (line[23] == ']'):
            line = line[1:23] + line[24:]
            new_line.append(line)
        elif (line[0] == '[') and (line[24] == ']'):
            line = line[1:24] + line[25:]
            new_line.append(line)
        else:
            new_line.append(line)
    new_line = new_line[1:]
    date, time = get_date_time(new_line)
    line = combine_line(new_line)
    author = aut(line)
    message = mess(line)
    #print(date, time, author, line) okoko
    df = pd.DataFrame({'date': date, 'time': time, 'author': author, 'message': message})
    df = transform(df)

    basic_info(df)
    get_author_info(df)
    analysis_on_day(df)
    get_most_active_member(df)
    most_media_by_author(df)
    get_most_word_by_author(df)
    no_link_share(df)
    active_date(df)
    graph_of_message_vs_month(df)
    active_month(df)
    message_vs_year(df)

main()
plt.close('all')