# from helpers import getRawComments
from langdetect import detect, DetectorFactory
from textblob import TextBlob
import pandas as pd
import numpy as np
import demoji
import re

DetectorFactory.seed = 0


def replace_emojis(text):
  return demoji.replace_with_desc(text, sep=" ")


def remove_colons_and_numbers(text):
  pattern = r'[:\d]'
  return re.sub(pattern, '', text)


def is_english(text):
  try:
    if detect(text) == 'en':
      return text
    return np.nan
  except:
    return np.nan


# comments = ['16:50 is the best \n\n\n1:12:30 is where I started understanding how time Flies', '42:51', '6:13  Mujra 😂', 'Thanks Kullu bhai for making more relatable 😂', 'This recap far better than  2023 😂😂😂', 'Watching it today,2024 but thanks man everyone ..Taarak Mehta chalta tha khana khate time,abb ye reaction videos chalta hai..Great Job guys.', '1:57 bro needs coffee', 'Present from 2024 🎉',
#             '01:07:38 kisi ka rick kisi ka roll kullu 😂😂😂', '17:39 if you wanna find a great meme so see this one legend 😅', '1:07:00 bhai ye vali full video ho kisi k pas to link bhejo😂 spiderman wali kya Kamal ki meme he usme😜', "Don't know why 30:20 he looks like Biswa.", 'Annu kanppor is the biggest f#ck up of bollywood and tv industry togather \nHutiya \nYe to gali ke nukkad par paan tapri bhi deserve nahi karta hai', '1:07:40 😂', '59:00😂', '59:00😂', 'Very disappointed']


def clean_comments(comments):
  df = pd.DataFrame(comments).drop_duplicates()
  df[0] = df[0].apply(replace_emojis).apply(
      remove_colons_and_numbers).apply(is_english)
  df = df.dropna()
  comments = df[0].tolist()
  return comments


sentiment_ranges = {
    'veryPositive': (0.6, 1.01),
    'postive': (0.2, 0.6),
    'neutral': (-0.2, 0.2),
    'negative': (-0.6, -0.2),
    'veryNegative': (-1.0, -0.6)
}


def getSentimentScores(comments):
  comments = clean_comments(comments)
  sentiment_counts = {
      'veryPositive': 0,
      'postive': 0,
      'neutral': 0,
      'negative': 0,
      'veryNegative': 0
  }
  for comment in comments:
    blob = TextBlob(comment)
    sentiment_score = blob.sentiment.polarity
    for sentiment, (lower, upper) in sentiment_ranges.items():
      if lower <= sentiment_score < upper:
        sentiment_counts[sentiment] += 1
        break
  n = len(comments)
  positive = ((sentiment_counts['veryPositive'] +
               sentiment_counts['postive'])/n)*100
  negative = ((sentiment_counts['negative'] +
               sentiment_counts['veryNegative'])/n)*100
  neutral = ((sentiment_counts['neutral']/n)*100)
  result = dict(positivePercentage=positive,
                neutralPercentage=neutral,
                negativePercentage=negative,
                numbersAnalyzed=n,
                sentimentCounts=sentiment_counts
                )
  return result
