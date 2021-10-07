from os import path
import os
from bs4 import BeautifulSoup
import json
from numpy import log
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from string import punctuation
import jieba
import sys
import io
from concurrent.futures import ThreadPoolExecutor
import threading
from loguru import logger


# 同义词字典
def read_simple_words_dict():
    simple_words = [line.strip() for line in open(
        '1.simple_words.txt', encoding='UTF-8').readlines()]
    simple_word_dict = {}
    for item_words in simple_words:
        s_words = item_words.split(",")
        for x in s_words:
            if len(x) == 0:
                continue
            simple_word_dict[x] = s_words[0]
    return simple_word_dict


add_punc = '，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥' + punctuation
# 通用停用词
stopwords = [line.strip() for line in open(
    '1.stop_words.txt', encoding='UTF-8').readlines()]
# 专用停用词
stopwords_dt = [line.strip() for line in open(
    '1.stop_words_dt.txt', encoding='UTF-8').readlines()]
simple_words = read_simple_words_dict()

jieba.load_userdict("./1.local_words.txt")


# 切词
def cut_words_with_text(content_texts):
    word_results_array = []
    for content in content_texts:
        words = jieba.cut(content, cut_all=True)
        for x in words:
            x_text = x.strip()
            if x_text in simple_words:
                x_text = simple_words[x_text]
            if x_text in add_punc or x_text in stopwords or x_text in stopwords_dt or len(x_text) == 1:
                continue
            word_results_array.append(x_text)
    logger.info(
        f"{threading.current_thread().name} cut_words successfully,word_results_array count:{len(word_results_array)}")
    return word_results_array

# 生成云图
def create_word_cloud_png(word_results_array, img_path):
    #制作云图
    #这个是创建一个云图，更改字体颜色等，大小等
    wc = WordCloud(
        font_path='./1.chinese.msyh.ttf',  #
        background_color='white',  # 背景颜色
        width=1000,
        height=600,
        max_font_size=300,  # 字体大小
        min_font_size=10,
        max_words=100,
        collocations=False,
        font_step=1
    )
   #这里云图 传入数据必须是带有空格的才能识别
    s = wc.generate(' '.join(word_results_array))
   #必须有这个才会显示图
    plt.imshow(s)
   #去除横纵坐标轴
    plt.axis('off')
    plt.show()
    #这个是图片存储
    s.to_file(img_path)
    logger.info(
        f"{threading.current_thread().name} create wordcloud img:{img_path} successfully.")

# 处理云图需要的数据
def create_word_cloud(date_index, data, base_dir="out"):
    img_path = f"./{base_dir}/{date_index.strftime('%Y%m%d_%H')}.png"
    contents = [record.content_text for _, record in data.iterrows()]
    if len(contents) == 0:
        return
    word_results_array = cut_words_with_text(content_texts=contents)
    create_word_cloud_png(word_results_array, img_path)


def contents_stats(date_index, data):
    contents = [record.content_text for _, record in data.iterrows()]
    logger.info(f"{date_index.strftime('%Y%m%d_%H')}：{len(contents)}")


if __name__ == "__main__":
    # 20211007_comments_75764.json 为2.to_json.py 产生的文件
    # id,created_time,content_text 数组
    file_path = sys.argv[1] if len(
        sys.argv) > 1 else "./20211007_comments_75764.json"
    pd_data = pd.read_json(file_path)
    rule_name = "8h"
    out_path = f"./out_{rule_name}"
    if not path.exists(out_path):
        os.mkdir(out_path)
    hour_resample_results = pd_data.resample(
        rule_name, on='created_time', origin='2021-09-27')
    for dt_index, data in hour_resample_results:
        create_word_cloud(dt_index, data, out_path)
