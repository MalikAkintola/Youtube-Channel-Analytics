#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Importing google's api
from googleapiclient.discovery import build
import pymysql
import pandas as pd

def get_video_ids(channel_id):
    # Get general playlist details
    video_request = youtube.channels().list(
                    part = 'contentDetails',
                    id = channel_id)
    response = video_request.execute()

    #get playlistid from the content details
    play = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    global videos
    videos = []
    nextPageToken = None
    
    while 1:
        #Get video details
        
        vid = youtube.playlistItems().list(playlistId = play, part = 'snippet', pageToken = nextPageToken, maxResults = 50, )
        listed = vid.execute()
        videos += listed['items']
        nextPageToken = listed.get('nextPageToken')

        if nextPageToken is None:
            break
    

    # Gets the video ID from the details returned
    video_ids = []
    i = 0
    while i < len(videos):
        ids = videos[i]['snippet']['resourceId']['videoId']
        video_ids.append(ids)
        i += 1
    return video_ids


def databaseinsertion(data):
    # Connect using PyMySQL
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="yourpassword",  # Replace with your MySQL password
        database="youtube",
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Create table SQL command
    delete_table_query = """
    DROP TABLE IF EXISTS youtube.videos;
    """
    # Execute the query to create the table
    cursor.execute(delete_table_query)
    connection.commit()  # Commit the transaction

    create_table_query = """
    CREATE TABLE videos (
        sn INT AUTO_INCREMENT PRIMARY KEY,
        videoid VARCHAR(255),
        publisheddate TEXT,
        title TEXT,
        categoryId INT,
        duration VARCHAR(50),
        viewCount INT,
        likeCount INT,
        favoriteCount INT,
        commentCount INT,
        url TEXT,
        thumbnailUrl TEXT,
        channelId VARCHAR(255)
    );
    """

    # Execute the query to create the table
    cursor.execute(create_table_query)
    connection.commit()  # Commit the transaction

    #Inserting the data

    for index, row in data.iterrows():
        insert_query = """
        INSERT INTO videos (videoid, publisheddate, title, categoryId, duration, viewCount, likeCount, favoriteCount, commentCount, url, thumbnailUrl, channelId)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            row['videoid'], 
            row['publisheddate'], 
            row['title'], 
            row['categoryId'], 
            row['duration'], 
            row['viewCount'], 
            row['likeCount'], 
            row['favoriteCount'], 
            row['commentCount'], 
            row['url'], 
            row['thumbnailUrl'], 
            row['channelId']
        ))

    # Commit the transaction to save the data
    connection.commit()
    print("Data inserted successfully.")


def get_videos(channelids):
    
    videos = {'videoid': [], 'publisheddate':[], 'title': [], 'categoryId': [], 'duration':[], 'viewCount':[], 'likeCount': [], 'favoriteCount':[], 'commentCount':[], 'url':[], 'thumbnailUrl':[], 'channelId':[]}

    # Gets the list of all video ids on the channel
    for channelid in channelids:
        print(f'Now collecting video IDs from Channel ID - {channelid}...')
        video_ids = get_video_ids(channelid)

        print('Video IDs collected successfully')
        print('Extracting video details...')
 
        num = 1
        error = None 

        #Gets the details of each video id
        for video_id in video_ids:
            details = youtube.videos().list(part = ['snippet', 'statistics', 'contentDetails'], id = video_id).execute()
            #Assigns each detail to the respective category in the dictionary
            videos['videoid'].append(video_id)

            videos['channelId'].append(channelid)

            publisheddate = details['items'][0]['snippet']['publishedAt']
            videos['publisheddate'].append(publisheddate)

            title = details['items'][0]['snippet']['title']
            videos['title'].append(title)

            categoryId = details['items'][0]['snippet']['categoryId']
            videos['categoryId'].append(categoryId)

            duration = details['items'][0]['contentDetails']['duration']
            videos['duration'].append(duration)

            try:
                viewCount = details['items'][0]['statistics']['viewCount']
                videos['viewCount'].append(viewCount)
            except:
                videos['viewCount'].append(error)

            try:
                likeCount = details['items'][0]['statistics']['likeCount']
                videos['likeCount'].append(likeCount)
            except:
                videos['likeCount'].append(error)

            try:
                favoriteCount = details['items'][0]['statistics']['favoriteCount']
                videos['favoriteCount'].append(favoriteCount)
            except:
                videos['favoriteCount'].append(error)

            try:
                commentCount = details['items'][0]['statistics']['commentCount']
                videos['commentCount'].append(commentCount)
            except:
                videos['commentCount'].append(error)

            url = f"https://www.youtube.com/watch?v={video_id}"
            videos['url'].append(url)
            try:
                thumbnailUrl = details['items'][0]['snippet']['thumbnails']['maxres']['url']
                videos['thumbnailUrl'].append(thumbnailUrl)
            except:
                thumbnailUrl = details['items'][0]['snippet']['thumbnails']['high']['url']
                videos['thumbnailUrl'].append(thumbnailUrl)

            print(f"Video id {num} is done")
            num += 1
        print(f'Compilation done for Channel ID - {channelid}') 
    print('All Channels Done') 
    new_df = pd.DataFrame(videos)
    databaseinsertion(new_df)

def get_summary_statistics(channelids, channelnames, images):
    names = channelnames
    imagelink = images
    channel_info = {'channelId' : [], 'name' : [], 'subscribers' : [], 'image link': []}
    for num, id in enumerate(channelids):
        request = youtube.channels().list(
                            part = 'statistics',
                            id = id)
        response = request.execute()
        summary = response['items'][0]['statistics']
        channel_info['channelId'].append(id)
        channel_info['name'].append(names[num])
        channel_info['subscribers'].append(summary['subscriberCount'])
        channel_info['image link'].append(imagelink[num])
    df = pd.DataFrame(channel_info)
    df.to_csv('Channels.csv')
    print('Summary Statistics done')

    
api_key = 'your api key'
mrbeastid = 'UCX6OQ3DkcsbYNE6H8uQQuVA'
dudeperfectid = 'UCRijo3ddMTht_IHyNSNXpNQ'
fisayofosudo = 'UCWHECOBvlhosLKVTHvw-3qw'
mkbhd = 'UCBJycsmduvYEL83R_U4JriQ'
mrwhosetheboss = 'UCMiJRAwDNSNzuYeN2uWa0pA'
alextheanalyst = 'UC7cs8q-gJRlGwj4A8OmCmXg'


channel_ids = [mrbeastid, dudeperfectid, fisayofosudo, mkbhd, mrwhosetheboss, alextheanalyst]
names = ['@MrBeast', '@dudeperfect', '@FisayoFosudo', '@mkbhd', '@Mrwhosetheboss', '@AlexTheAnalyst']
imagelink =  ['https://yt3.googleusercontent.com/fxGKYucJAVme-Yz4fsdCroCFCrANWqw0ql4GYuvx8Uq4l_euNJHgE-w9MTkLQA805vWCi-kE0g=s160-c-k-c0x00ffffff-no-rj',
                    'https://yt3.googleusercontent.com/ytc/AIdro_lnf0k0Vr_bPUzC4OIUIp0hGSvnEnteat4Hq33JMMo6qBI=s160-c-k-c0x00ffffff-no-rj',
                    'https://yt3.googleusercontent.com/ytc/AIdro_ktr-vIl-HX4_mEKjjzEh0rs1QGq1_Wn0NlJZ3nrdEshBk=s160-c-k-c0x00ffffff-no-rj',
                    'https://yt3.googleusercontent.com/lkH37D712tiyphnu0Id0D5MwwQ7IRuwgQLVD05iMXlDWO-kDHut3uI4MgIEAQ9StK0qOST7fiA=s160-c-k-c0x00ffffff-no-rj',
                    'https://yt3.googleusercontent.com/enyLBm1Sy8mVRXJJLWHT2z64nqxJGt2g61A9xnxpUjO2YAUovHaY_JT3rnAg0j6Qij9iaHQlAg=s160-c-k-c0x00ffffff-no-rj',
                    'https://yt3.googleusercontent.com/ytc/AIdro_l9wLnClpLKJeVmP5XwHy4NF_Gu13GfyRT1WTZDaSYS-g=s160-c-k-c0x00ffffff-no-rj']


youtube = build('youtube', 'v3', developerKey=api_key)

get_summary_statistics(channel_ids, names, imagelink)
get_videos(channel_ids)


# In[ ]:




