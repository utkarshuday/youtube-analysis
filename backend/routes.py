from flask_restful import fields, Resource, marshal_with
from helpers import youtube, getVideoDetails, getVideoIds
from sentiments import getSentimentScores
from helpers import getRawComments
import pandas as pd


channelField = {
    'channelId': fields.String,
    'channelTitle': fields.String,
    'channelDescription': fields.String,
    'thumbnail': fields.String,
    'customUrl': fields.String,
    'viewCount': fields.Integer,
    'subscriberCount': fields.Integer,
    'videoCount': fields.Integer,
    'playlistId': fields.String,
    'maxViews': fields.Integer,
    'maxLikes': fields.Integer,
    'maxComments': fields.Integer,
    'videoDetails': fields.List(fields.Nested({
        'id': fields.String,
        'likes': fields.Integer,
        'views': fields.Integer,
        'comments': fields.Integer,
        'title': fields.String,
        'published': fields.String
    }))
}

# route /channel-details/:id to send details


class Channel(Resource):
  @marshal_with(channelField)
  def get(self, id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=id
    )
    response = request.execute()
    item = response['items'][0]
    data = dict(channelTitle=item['snippet']['title'],
                channelId=response['items'][0]['id'],
                channelDescription=item['snippet']['description'],
                customUrl=item['snippet']['customUrl'],
                thumbnail=item['snippet']['thumbnails']['medium']['url'],
                viewCount=item['statistics']['viewCount'],
                subscriberCount=item['statistics']['subscriberCount'],
                videoCount=item['statistics']['videoCount'],
                playlistId=response['items'][0]['contentDetails']['relatedPlaylists']['uploads'])
    videoIds = getVideoIds(data['playlistId'])
    videoDetails = getVideoDetails(videoIds)
    df = pd.DataFrame(videoDetails)
    df['views'] = pd.to_numeric(df['views'])
    df['comments'] = pd.to_numeric(df['comments'])
    df['likes'] = pd.to_numeric(df['likes'])

    df_sorted = df.sort_values(by='views', ascending=False)
    data['maxViews'] = df['views'].max()
    data['maxComments'] = df['comments'].max()
    data['maxLikes'] = df['likes'].max()

    sorted_videoDetails = df_sorted.to_dict(orient='records')
    data['videoDetails'] = sorted_videoDetails
    return data


channelFields = {
    'channelId': fields.String,
    'channelTitle': fields.String
}


class Channels(Resource):
  @marshal_with(channelFields)
  def get(self, name):
    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=name,
        type="channel"
    )
    response = request.execute()
    channels = []
    for item in response.get('items'):
      channel = {}
      channel['channelId'] = item['snippet']['channelId']
      channel['channelTitle'] = item['snippet']['channelTitle']
      channels.append(channel)

    return channels


sentimentFields = {
    'positivePercentage': fields.Float,
    'neutralPercentage': fields.Float,
    'negativePercentage': fields.Float,
    'numbersAnalyzed': fields.Integer,
    'sentimentCounts': fields.Nested({
        'veryPositive': fields.Integer,
        'postive': fields.Integer,
        'neutral': fields.Integer,
        'negative': fields.Integer,
        'veryNegative': fields.Integer
    })
}

# route /sentiments/:videoId to send details


class Sentiment(Resource):
  @marshal_with(sentimentFields)
  def get(self, videoId):
    comments = getRawComments(videoId)
    result = getSentimentScores(comments)
    return result
