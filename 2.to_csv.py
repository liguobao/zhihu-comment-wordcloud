import json
import sys
from loguru import logger
from bs4 import BeautifulSoup


def to_csv(file_path):
    logger.info(f"read {file_path}")
    with open(file_path, "r+") as fp:
        json_data = json.loads(fp.read())
        with open(f"{file_path}.csv", "w+") as wp:
            wp.write("create_time,content\n")
            json_data.sort(key=lambda x: x["created_time"])
            for item in json_data:
                content_text = BeautifulSoup(
                    item.get('content'), "html.parser").text.replace("\n", "")
                wp.write(f"{item.get('created_time')},'{content_text}'\n")
        logger.info(f"{file_path} to csv successfully.")


if __name__ == "__main__":
    file_path = sys.argv[1]
    to_csv(file_path=file_path)
    pass
