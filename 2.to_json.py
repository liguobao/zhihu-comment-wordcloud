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
        json_data.sort(key=lambda x: x["created_time"])
        results = [
            {
                "id": x.get("id"),
                "content_text": BeautifulSoup(x.get('content'), "html.parser").text.replace("\n", ""),
                "created_time": x.get("created_time")
            } for x in json_data]
        with open(f"{file_path}_sample.json", "w+") as wf:
            wf.write(json.dumps(results, ensure_ascii=False, indent=4))
        logger.info(f"{file_path} to json successfully.")


if __name__ == "__main__":
    file_path = sys.argv[1]
    to_json(file_path=file_path)
    pass
