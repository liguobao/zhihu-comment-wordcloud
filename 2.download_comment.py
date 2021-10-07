import requests
from loguru import logger
import time
import random
import json

deaulft_headers = {
    'authority': 'www.zhihu.com',
    'x-zse-93': '101_3_2.0',
    'x-ab-param': 'se_ffzx_jushen1=0;zr_expslotpaid=1;top_test_4_liguangyi=1;qap_question_author=0;tp_dingyue_video=0;tp_topic_style=0;tp_contents=2;qap_question_visitor= 0;pf_noti_entry_num=2;tp_zrec=1;pf_adjust=1;zr_slotpaidexp=1',
    'x-ab-pb': 'CroB1wKmBDMFdAHgBAsE4wQZBRsAaQFWBVIL5ArHAjMEEQU0DLULdQSiAwoE0QT0C58C7AqbCz8AQAG5AtgCVwTBBNoE4AsSBU8DbAThBMoCNwVRBUMA9wNFBNcLzwsqBEIEoANWDNwL9gJsAzQEBwyEAjIDFAVSBbcD6QQpBWALfQI/BY4DZAS0CvgDFQUPC1ADVwPoA9YEagGMAnIDMgU3DMwCVQUBC0cAzAQOBbQAKgI7AqED8wP0A4kMEl0AAAAAAAABAAAAAAEAAAAAAAMAAAEFAAIBAAABFQABAQEAAQAAAgAAABUBAQALAAEAAQAAAAABAAACBAABAAABAAEBAAEAAQAAAAIBAAEAAQAAAQABAAAAAQAAAAA=',
    'x-zst-81': '3_2.0ae3TnRUTEvOOUCNMTQnTSHUZo02p-HNMZBO8YD_ycXtucXYqK6P0E79y-LS9-hp1DufI-we8gGHPgJO1xuPZ0GxCTJHR7820XM20cLRGDJXfgGCBxupMuD_Io4cpr4w0mRPO7HoY70SfquPmz93mhDQyiqV9ebO1hwOYiiR0ELYuUrxmtDomqU7ynXtOnAoTh_PhRDSTFHOsaDH_8UYq0CN9UBFM6Hg1f_FOYrOGwBoYrgcCjBL9hvx1oCYK8CVYUBeTv6u1pgcMzwV8wwt1EbrL-UXBgvg0Z9N__vem_C3L8vCZfMS_Uhoftck1UGg0Bhw1rrXKZgcVQQeC-JLZ28eqWcOxLGo_KX3OsquLquoXxDpMUuF_ChUCCqkwe7396qOZ-Je8ADS9CqcmUuoYsq98yqLmUggYsBXfbLVL3qHMjwS_mXefOComiDSOkUOfQqX00UeBUcnXAh3mMD31bgOYSTSufuCYuDgCjqefWqHYeQSC',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'x-app-version': '6.42.0',
    'sec-ch-ua-mobile': '?0',
    'x-requested-with': 'fetch',
    'x-zse-96': '2.0_aHtyee9qUCtYHUY81LF8NgU0NqNxgUF0MHYyoHe0NG2f',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.zhihu.com/question/398741940/answer/2142391477',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'cookie': '换成自己的'
}


def load_answer_comments(req_url):
    payload = {}
    response = requests.request(
        "GET", req_url, headers=deaulft_headers, data=payload)
    if response.status_code == 200 and response.json().get("paging", {}).get("is_end", None) == False:
        return response.json().get("data"), response.json().get("paging").get("next")
    return [], None


def write_json(answer_comments):
    file_name = f"{time.time()}.json"
    with open(file_name, "w+") as fp:
        fp.write(json.dumps(answer_comments, ensure_ascii=False, indent=4))
        logger.info(f"write_json successfully.")

# 2142391477 为回答Id，
answer_comment_url = "https://www.zhihu.com/api/v4/answers/2142391477/comments?order=reverse&limit=20&offset=0&status=open"
page_comments, next_page_url = load_answer_comments(answer_comment_url)
answer_comments = page_comments
page_index = 0
while next_page_url:
    page_comments, next_page_url = load_answer_comments(next_page_url)
    answer_comments = answer_comments + page_comments
    logger.info(
        f"{page_index} crawl comments successfully,answer_comments count:{len(answer_comments)}")
    # if int(len(answer_comments) % 10000) == 0 and len(answer_comments) >= 1000:
    #     write_json(answer_comments)
    page_index = page_index + 1
file_name = f"{time.time()}.json"
with open(file_name, "w+") as fp:
    fp.write(json.dumps(answer_comments, ensure_ascii=False, indent=4))
    logger.info(f"write {file_name} successfully.")
