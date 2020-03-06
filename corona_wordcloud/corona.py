from newsapi import NewsApiClient

api = NewsApiClient(api_key = key)

articles = api.get_everything(q = 'corona virus',
                      from_param = '2020-02-06',
                      to = '2020-03-06',
                      language='en')

news_list = []
title_list = []
for i in articles.items():
    news_list.append(i)

for j in range(news_list[2][1].__len__()):
    title_list.append(news_list[2][1][j]['title'])
    title_list.append(news_list[2][1][j]['content'])


import pandas as pd
from nltk.corpus import stopwords
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

text = pd.Series(title_list)
text = text.drop_duplicates()
text = text.dropna()

text = text.apply(lambda x: ' '.join(x.lower() for x in x.split()))
text = text.str.replace('[\W]', ' ')
stop = stopwords.words('english')
text = text.apply(lambda x: ' '.join(x for x in x.split() if x not in stop))
#check frequencies:
pd.Series(' '.join(text).split()).value_counts()

#wordcloud
wc = WordCloud(width = 1600, height = 800, background_color= 'white', colormap='Oranges', stopwords=['chars']).generate(' '.join(text))
plt.figure(figsize= (20,10))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.margins(x= 0, y=0)



#wordcloud with mask

dt_mask = np.array(Image.open('virus1.png'))

# plot the wordcloud
wordcloud = WordCloud(background_color='white', max_words=1500 ,mask = dt_mask, contour_width= 1).generate(' '.join(text))
image_colors = ImageColorGenerator(dt_mask)
plt.figure()
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
plt.axis('off')
plt.margins(x = 0, y = 0)
