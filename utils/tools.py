# This file contains all the tools used in the project.
import requests
import json
import yaml
import os


def get_udemylink(searchby: str = "", category: str = ""):
    """
    Returns a generator of all the courses with settings in config.yml."""
    cat = {
        "": "",
        "All": "",
        "Teaching & Academics": "1",
        "Development Business": "2",
        "IT & Software": "3",
        "Marketing": "4",
        "Finance and acconting": "5",
        "Office Productivity": "6",
        "Business": "7",
        "Design": "8",
        "Personal Development": "9",
        "Photography & Video": "10",
        "Life Style": "11",
        "Music": "12",
    }

    params = {
        "store": "Udemy",
        "page": "1",
        "per_page": "25",
        "orderby": "undefined",
        "free": "1",
        "search": searchby,
        "language": "",
        "category": cat[category],
    }
    source = requests.get(
        "https://www.real.discount/api-web/all-courses/", params=params
    )
    contents = json.loads(source.content)
    for dataset in contents["results"]:
        if "isexpired" in dataset.keys() and dataset["isexpired"] == "Available":
            yield dataset


def update_config(cfg=None) -> dict:
    """Checks if config.yml exists, if not creates one and returns the config file."""
    if cfg is not None:  # updates config.yml
        with open("config.yml", "w") as ymlfile:
            ymlfile.write(yaml.dump(cfg))
            return cfg

    if os.path.exists("config.yml"):
        with open("config.yml", "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
            return cfg
    else:
        with open("config.yml", "w") as ymlfile:
            cfg = {
                "email": "",
                "password": "",
                "search": "",
                "category": "",
            }
            ymlfile.write(yaml.dump(cfg))
            return cfg
