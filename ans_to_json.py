import json
import sys
from loguru import logger
from bs4 import BeautifulSoup
import datetime
import time


def to_json(file_path):
    logger.info(f"read {file_path}")
    with open(file_path, "r+") as fp:
        json_data = json.loads(fp.read())
        logger.info(f"read {file_path} successfully, data count:{len(json_data)}")
        json_data.sort(key=lambda x: x["target"]["created_time"])
        results = [
            {
                "id": x.get("target").get("id"),
                "content_text": BeautifulSoup(x.get("target").get('content'), "html.parser").text.replace("\n", ""),
                "created_time": x.get("target").get("created_time")
            } for x in json_data]
        out_file_path = f"{file_path}_sample.json"
        with open(f"{out_file_path}", "w+") as wf:
            wf.write(json.dumps(results, ensure_ascii=False, indent=4))
        logger.info(f"{file_path} to json successfully.")
        return out_file_path


if __name__ == "__main__":
    file_path = sys.argv[1]
    to_json(file_path=file_path)
    pass
