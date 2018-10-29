import jieba.analyse
from PIL import Image, ImageSequence
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

l = ''
f = open('a.txt', 'r')
for i in f:
    l += f.read()

result = jieba.analyse.textrank(l, topK=250, withWeight=True)
keyworlds = dict()
for i in result:
    keyworlds[i[0]] = i[1]

# print(keyworlds)

image = Image.open('timg.jpg')
graph = np.array(image)
wc = WordCloud(font_path='simhei.ttf', background_color='White', max_font_size=170, mask=graph)
wc.generate_from_frequencies(keyworlds)
image_color = ImageColorGenerator(graph)
plt.imshow(wc)
plt.imshow(wc.recolor(color_func=image_color))
plt.axis('off')
plt.show()
wc.to_file('1.png')
