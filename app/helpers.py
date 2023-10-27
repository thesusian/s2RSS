from flask import jsonify
import requests
import html
import re

def clean_before_regex(text: str) -> str:
    text = re.sub(r"[\t\n]", " ", text)  # tabs and newlines -> single space
    text = re.sub(r" +", " ", text)  # multiple spaces -> single space
    text = re.sub(r"(?<=>)(?=<)", " ", text)  # spacing between elements "div> <div"
    text = re.sub(r"\s*(?=>)", "", text)  # remove spacing before ">"
    return text


def clean_pattern(pattern: str) -> str:
    pattern = clean_before_regex(pattern)
    pattern = pattern.replace("/", "\/")  # escape / character for regex
    pattern = pattern.replace("?", "\?")  # escape ? character for regex
    pattern = re.sub(r"\s*{%}\s*", "(.*?)", pattern)  # target pattern
    pattern = re.sub(r"\s*\{\*\}\s*", ".*?", pattern)  # wildcard pattern

    # clean pattern to prevent DoS
    # we have to remove concurrent targets and wildcards
    # and we have to limit the number of target and wildcard pattenrs
    limit = 10
    pattern = re.sub(r"{%}+", "{%}", pattern)
    pattern = re.sub(r"\{\*\}+", "{*}", pattern)
    if pattern.count("{%}") > limit or pattern.count("{*}") > limit:
        print("Too many targets or wildcards in pattern")
        # TODO, communicate this to the user
        return ""
    print(pattern)
    return pattern


def get_foramtted_list(source_code: str, pattern: str) -> str:
    source_code = clean_before_regex(source_code)
    pattern = clean_before_regex(pattern)
    pattern = clean_pattern(pattern)

    regex = r"" + pattern
    matches = re.findall(regex, source_code)
    output = ""

    for i in range(len(matches)):
        output += f"Item {i+1}:\n"
        d = 1
        # if it's multple elements it will return tuple
        if isinstance(matches[i], tuple):
            for data in matches[i]:
                # some websites use html charachters like &#x27; so we unescape them
                output += "{%" + str(d) + "}: " + html.unescape(data).strip() + "\n"
                d += 1
        else:
            output += "{%" + str(d) + "}: " + html.unescape(matches[i]).strip() + "\n"
            d += 1
        output += "\n"

    return output


def get_json_list(source_code: str, pattern: str) -> str:
    source_code = clean_before_regex(source_code)
    pattern = clean_before_regex(pattern)
    pattern = clean_pattern(pattern)

    regex = r"" + pattern
    matches = re.findall(regex, source_code)

    output = {}
    for i in range(len(matches)):
        d = 1
        item_dict = {}
        # if it's multple elements it will return tuple
        if isinstance(matches[i], tuple):
            for data in matches[i]:
                key = f"{{%{d}}}"
                value = html.unescape(data).strip()
                item_dict[key] = value
                d += 1
        else:
            key = f"{{%{d}}}"
            value = html.unescape(matches[i]).strip()
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
