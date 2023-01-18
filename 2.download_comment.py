import argparse
from os import path
import os
import requests
from loguru import logger
import time
import random
import threading
import json

deaulft_headers = {
    'authority': 'www.zhihu.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cache-control': 'max-age=0',
    'cookie': '',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


def load_answer_comments(req_url):
    """加载单页评论数据

    Args:
        req_url (_type_): _description_

    Returns:
        _type_: _description_
    """
    payload = {}
    try:
        response = requests.request(
            "GET", req_url, headers=deaulft_headers, data=payload)
        if response.status_code != 200:
            logger.error(
                f"load_answer_comments fail,req_url:{req_url},response:{response.text}")
            return [], None
        comments = response.json().get("data")
        # 处理下一页
        if response.json().get("paging", {}).get("is_end", None) == True:
            next_url = None
        else:
            next_url = response.json().get("paging", {}).get("next")
        return comments, next_url
    except Exception as err:
        logger.error(
            f"load_answer_comments fail,req_url:{req_url},error:{err}")
        return [], None


def write_json(answer_comments):
    file_name = f"{time.time()}.json"
    with open(file_name, "w+") as fp:
        fp.write(json.dumps(answer_comments, ensure_ascii=False, indent=4))
        logger.info(f"write_json successfully.")


def download_all_comment(answer_id):
    """下载所有的评论
    Args:
        answer_id (_type_): _description_
    """
    # 2142391477 为回答Id，
    answer_comment_url = f"https://www.zhihu.com/api/v4/answers/{answer_id}/comments?order=reverse&limit=100&offset=0&status=open"
    page_comments, next_page_url = load_answer_comments(answer_comment_url)
    answer_comments = page_comments
    page_index = 0
    while next_page_url:
        time.sleep(100)
        page_comments, next_page_url = load_answer_comments(next_page_url)
        answer_comments = answer_comments + page_comments
        logger.info(
            f"{page_index} crawl comments successfully,answer_comments count:{len(answer_comments)}")
        # if int(len(answer_comments) % 10000) == 0 and len(answer_comments) >= 1000:
        #     write_json(answer_comments)
        page_index = page_index + 1
    file_name = f"./data/{answer_id}_{time.time()}.json"
    with open(file_name, "w+") as fp:
        fp.write(json.dumps(answer_comments, ensure_ascii=False, indent=4))
        logger.info(f"write {file_name} successfully.")


if __name__ == "__main__":
    parse = argparse.ArgumentParser(prog='zhihu_comments_donwload')
    parse.add_argument(
        '-id', '--answer_id', help='answer_id:回答Id, 2142391477')
    cmd_args = parse.parse_args()
    if not path.exists("./data"):
        os.mkdir("./data")
    if cmd_args.answer_id:
        download_all_comment(cmd_args.answer_id)
    else:
        parse.print_help()
