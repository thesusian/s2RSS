from flask import jsonify
import requests
import re


def clean_before_regex(text: str) -> str:
    text = re.sub(r"[\t\n]", " ", text)  # tabs and newlines -> single space
    text = re.sub(r" +", " ", text)  # multiple spaces -> single space
    text = re.sub(r"(?<=>)(?=<)", " ", text)  # spacing between elements "div> <div"
    text = re.sub(r"\s*(?=>)", "", text)  # remove spacing before ">"
    return text


def get_foramtted_list(source_code: str, pattern: str) -> str:
    source_code = clean_before_regex(source_code)
    pattern = clean_before_regex(pattern)
    pattern = re.sub(r"\s*{%}\s*", "(.*?)", pattern)  # target pattern
    pattern = re.sub(r"\s*\{\*\}\s*", ".*?", pattern)  # wildcard pattern
    pattern = pattern.replace("/", "\/")  # escape / character for regex

    regex = r"" + pattern
    matches = re.findall(regex, source_code)
    output = ""

    for i in range(len(matches)):
        output += f"Item {i+1}:\n"
        d = 1
        for data in matches[i]:
            output += "{%" + str(d) + "}: " + str(data).strip() + "\n"
            d += 1
        output += "\n"

    return output


def get_json_list(source_code: str, pattern: str) -> str:
    source_code = clean_before_regex(source_code)
    pattern = clean_before_regex(pattern)
    pattern = re.sub(r"\s*{%}\s*", "(.*?)", pattern)  # target pattern
    pattern = re.sub(r"\s*\{\*\}\s*", ".*?", pattern)  # wildcard pattern
    pattern = pattern.replace("/", "\/")  # escape / character for regex

    regex = r"" + pattern
    matches = re.findall(regex, source_code)

    output = {}
    for i in range(len(matches)):
        d = 1
        item_dict = {}
        for data in matches[i]:
            key = f"{{%{d}}}"
            value = str(data).strip()
            item_dict[key] = value
            d += 1
        output[f"Item {i}"] = item_dict

    return jsonify(output)


def get_address_source(address: str) -> str:
    # I made this a separate function to optimize it later
    try:
        response = requests.get(address)
        return response.text
    except Exception:
        return ""
