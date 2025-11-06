import os
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import yaml
import matplotlib.colors as mcolors

# 读取配置
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
CSV_PATH = config.get('csv_path', 'data/input.csv')
TEXT_COLUMN = config.get('text_column', 'title')
OUTPUT_IMG = config.get('output_img', 'output/wordcloud.png')
FONT_PATH = config.get('font_path', '/System/Library/Fonts/STHeiti Medium.ttc')
BACKGROUND_COLOR = config.get('background_color', 'white')
WIDTH = config.get('width', 800)
HEIGHT = config.get('height', 600)
COLOR_START = config.get('color_start', '#000000')
COLOR_END = config.get('color_end', '#FFFFFF')
COLORMAP = config.get('colormap', 'viridis')

# 检查文件夹
os.makedirs('data', exist_ok=True)
os.makedirs('output', exist_ok=True)

# 读取CSV
if not os.path.exists(CSV_PATH):
    print(f"请将CSV文件放在 {CSV_PATH}，并确保第一列列名为'{TEXT_COLUMN}'。")
    exit(1)
df = pd.read_csv(CSV_PATH, usecols=[0])
if df.columns[0] != TEXT_COLUMN:
    print(f"CSV第一列列名应为'{TEXT_COLUMN}'，当前为'{df.columns[0]}'。请修改后重试。")
    exit(1)

# 合并所有title内容
text = ' '.join(df[TEXT_COLUMN].astype(str))

# 加载停用词表
stopwords_path = 'data/stopwords.txt'
if os.path.exists(stopwords_path):
    with open(stopwords_path, encoding='utf-8') as f:
        stopwords = set(line.strip() for line in f if line.strip())
else:
    stopwords = set()

# 分词
words = jieba.cut(text)
word_list = [w.strip() for w in words if w.strip() and w.strip() not in stopwords]

# 保存分词结果到TXT
segmented_path = 'output/segmented_words.txt'
with open(segmented_path, 'w', encoding='utf-8') as f:
    for word in word_list:
        f.write(word + '\n')
print(f"分词结果已保存到 {segmented_path}")

# 统计词频
word_counts = Counter(word_list)

# 保存词频统计到CSV
counts_path = 'output/word_counts.csv'
pd.DataFrame(word_counts.most_common(), columns=['word', 'count']).to_csv(counts_path, index=False)
print(f"词频统计已保存到 {counts_path}")

# 生成词云
wc = WordCloud(font_path=FONT_PATH, width=WIDTH, height=HEIGHT, background_color=BACKGROUND_COLOR, colormap=COLORMAP)
wc.generate_from_frequencies(word_counts)

# 保存图片
wc.to_file(OUTPUT_IMG)
print(f"词云图片已保存到 {OUTPUT_IMG}")

# 可选：显示词云
# plt.imshow(wc, interpolation='bilinear')
# plt.axis('off')
# plt.show() 