import argparse
from os import path
import os
import requests
from loguru import logger
import time
import webbrowser

import json

retry_count = 0

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


def load_answer_list(req_url):
    """

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
            if response.json().get("error", {}).get("code", None) == 40352:
                logger.error("need login, sleep 30s~ please pass unhuman verify in browser ")
                redirect_url = response.json().get("redirect",
                                                   "https://www.zhihu.com/account/unhuman?type=unhuman&message=系统监测到您的网络环境存在异常，为保证您的正常访问，请点击下方验证按钮进行验证。在您验证完成前，该提示将多次出现")
                logger.info(f"redirect_url:{redirect_url}")
                webbrowser.open(redirect_url)
                time.sleep(30)
                retry_count = retry_count + 1
                if retry_count > 3:
                    logger.error("retry_count > 3, exit")
                    return [], None
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


def download_all_answer(question_id):
    try:
        # 267147843 为问题Id，
        request_url = f"https://www.zhihu.com/api/v4/questions/{question_id}/feeds?cursor=&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&order=default&platform=desktop&session_id="
        page_results, next_page_url = load_answer_list(request_url)
        result_list = page_results
        page_index = 0
        while next_page_url:
            time.sleep(0.1)
            page_results, next_page_url = load_answer_list(next_page_url)
            result_list = result_list + page_results
            logger.info(
                f"{page_index} crawl successfully, list count:{len(result_list)}")
            # if int(len(answer_comments) % 10000) == 0 and len(answer_comments) >= 1000:
            #     write_json(answer_comments)
            page_index = page_index + 1
    except Exception as err:
        logger.error(f"download_all_answer fail,question_id:{question_id},error:{err}")
    file_name = f"./data/{question_id}_{time.time()}.json"
    with open(file_name, "w+") as fp:
        fp.write(json.dumps(result_list, ensure_ascii=False, indent=4))
        logger.info(f"write {file_name} successfully.")
        return file_name


if __name__ == "__main__":
    parse = argparse.ArgumentParser(prog='zhihu_answer_donwload')
    parse.add_argument(
        '-id', '--question_id', help='question_id:回答Id, 267147843')
    cmd_args = parse.parse_args()
    if not path.exists("./data"):
        os.mkdir("./data")
    if cmd_args.question_id:
        download_all_answer(cmd_args.question_id)
    else:
        parse.print_help()
