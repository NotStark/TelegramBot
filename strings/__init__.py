import os
from typing import List
import yaml
from dotmap import DotMap


languages = {}
commands = {}


def get_command(value: str) -> List:
    return commands["commands"][value]


def get_string(lang: str):
    return languages[lang]


def load_commands():
    for filename in os.listdir("./strings"):
        if filename.endswith(".yml"):
            language_name = filename[:-4]
            commands[language_name] = yaml.safe_load(
                open(os.path.join("./strings", filename))
            )


def load_langs():
    if "en" not in languages:
        languages["en"] = DotMap(yaml.safe_load(
            open("./strings/langs/en.yml")
        ))

    for filename in os.listdir("./strings/langs"):
        if filename.endswith(".yml"):
            language_name = filename[:-4]
            if language_name == "en":
                continue
            languages[language_name] = DotMap(yaml.safe_load(
                open(os.path.join("./strings/langs", filename))
            ))
            for item in languages["en"]:
                if item not in languages[language_name]:
                    languages[language_name][item] = languages["en"][item]


load_commands()
load_langs()
