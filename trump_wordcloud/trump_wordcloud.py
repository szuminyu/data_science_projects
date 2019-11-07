import tweepy

## get authorization
auth = tweepy.OAuthHandler(consumer_key= consumer_key,consumer_secret= consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)


## what's trump's user info?
user = api.get_user('realDonaldTrump')
print(user.screen_name)
print(user.id)


## get 200 tweets
tweets = tweepy.Cursor(api.user_timeline, screen_name = 'realDonaldTrump',include_rts = False ,count = 200)
empty_list = []
for status in tweets.items():
    empty_list.append(status.text)


## put it into dataframe and process the text
import pandas as pd
data = pd.DataFrame(data = empty_list, columns = ['text'])

# everything to lower case
data['text'] = data['text'].apply(lambda x: ' '.join(x.lower() for x in x.split()))
# remove punctuation
data['text'] = data['text'].str.replace('[\W]',' ')

# remove stopwords
from nltk.corpus import stopwords
stop = stopwords.words('english')
data['text'] = data['text'].apply(lambda x: ' '.join(x for x in x.split() if x not in stop))

# remove top 3 common words
freq = pd.Series(' '.join(data['text']).split()).value_counts()[:3]
print(freq)
freq = list(freq.index)
data['text'] = data['text'].apply(lambda x:" ".join(x for x in x.split() if x not in freq))


## produce the wordcloud
from wordcloud import (WordCloud,ImageColorGenerator)
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# mask the trump pic
dt_mask = np.array(Image.open('trump.jpg'))

# plot the wordcloud
wordcloud = WordCloud(background_color='white', max_words=1500 ,mask = dt_mask).generate(' '.join(data['text']))
image_colors = ImageColorGenerator(dt_mask)
plt.figure()
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
plt.axis('off')
plt.margins(x = 0, y = 0)
plt.show()
