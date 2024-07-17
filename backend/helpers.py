from googleapiclient.discovery import build

API_KEY = 'AIzaSyCzk_DuGfmCnnbZIWmslsfW1cTLEN7mSe4'
api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=API_KEY)


def getVideoIds(playlistId):
  request = youtube.playlistItems().list(
      part="contentDetails",
      playlistId=playlistId,
      maxResults=50
  )
  response = request.execute()
  video_ids = []
  for i in range(len(response.get('items'))):
    video_ids.append(response.get('items')[i]["contentDetails"]['videoId'])
  next_page_token = response.get('nextPageToken')
  while next_page_token != None:
    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlistId,
        maxResults=50,
        pageToken=next_page_token)
    response = request.execute()
    for i in range(len(response.get('items'))):
      video_ids.append(response.get('items')[
                       i]["contentDetails"]['videoId'])
    next_page_token = response.get('nextPageToken')

  return video_ids


def getVideoDetails(videoIds):
  videoDetails = []
  for i in range(0, len(videoIds), 50):
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=','.join(videoIds[i:i+50]))
    response = request.execute()
    for video in response['items']:
      videoStats = dict(title=video['snippet']['title'],
                        id=video['id'],
                        published=video['snippet']['publishedAt'],
                        views=video['statistics']['viewCount'],
                        likes=video['statistics']['likeCount'],
                        comments=video['statistics']['commentCount']
                        )
      videoDetails.append(videoStats)

  return videoDetails


def getRawComments(videoId):
  comments = []
  response = youtube.commentThreads().list(
      part='snippet',
      videoId=videoId,
      textFormat='plainText',
      maxResults=100
  ).execute()
  next_page_token = response.get('nextPageToken')
  if not response['items']:
    print(f"Comments are disabled for video with ID: {
        videoId}. Skipping...")
    return comments
  for i in range(len(response.get('items'))):
    comments.append(response.get('items')[
                    i]['snippet']['topLevelComment']['snippet']['textDisplay'])
  while next_page_token != None and len(comments) <= 1000:
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=videoId,
        textFormat='plainText',
        maxResults=3,
        pageToken=next_page_token
    ).execute()

    for i in range(len(response.get('items'))):
      comments.append(response.get('items')[
          i]['snippet']['topLevelComment']['snippet']['textDisplay'])
    next_page_token = response.get('nextPageToken')

  return comments
