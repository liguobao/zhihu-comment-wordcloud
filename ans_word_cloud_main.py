import argparse
from os import path
import os
from ans_download import download_all_answer
from ans_to_json import to_json
from ans_word_cloud_all import to_word_cloud_img


if __name__ == "__main__":
    parse = argparse.ArgumentParser(prog='zhihu_answer_donwload')
    parse.add_argument(
        '-id', '--question_id', help='question_id')
    cmd_args = parse.parse_args()
    if not path.exists("./data"):
        os.mkdir("./data")
    if cmd_args.question_id:
       file_path = download_all_answer(cmd_args.question_id)
       sample_file_path = to_json(file_path=file_path)
       img_path = to_word_cloud_img(file_path=sample_file_path)
    else:
        parse.print_help()
