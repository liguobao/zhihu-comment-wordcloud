# zhihu-comment-wordcloud

- 知乎评论区词云分析

- 起源于：[如何看待知乎问题“男生真的很不能接受彩礼吗？”的一个回答下评论数超8万条，创单个回答下评论数新记录？](https://www.zhihu.com/question/490763912/answer/2156636932)

![样例文件](./sample.png)

## 项目代码说明

- 1.local_words.txt 本地特定分词（优化分词结果）
- 2.download_comment.py 下载全量评论
- 2.word_cloud_all.py 全部数据生成词云
- 2.word_cloud_by_dt 生成词云
- 2.to_csv 将原始评论数据提取到CSV文件
- 2.to_json 将原始评论数据提取到Json文件

## JS

- [dump_user_ans_list.js](./dump_user_ans_list.js) 用于知乎用户页面获取用户回答列表
