import argparse
import json
import requests
import logging

# logging.basicConfig(level=logging.DEBUG)

search_url = "https://api.github.com/search/repositories?q={projectname}&sort=stars&order=desc'"

template = {
    'uid': 'text',
    'title': None,
    'arg': None,
    'mods': {
        'alt': {
            'valid': True,
            'arg': None,
            'subtitle': f'按「Enter键」复制Clone URL到剪贴板',
        },
        'cmd': {
            'valid': True,
            'arg': None,
            'subtitle': f'按「Enter键」复制SSH URL到剪贴板',
        },
    }
}

parser = argparse.ArgumentParser()
parser.add_argument("projectname", help="Search a project in GitHub",
                    type=str)
args = parser.parse_args()
logging.debug(f"args.projectname={args.projectname}")
url = search_url.format(projectname=args.projectname)
logging.debug(f"url={url}")

response = requests.get(url)
assert response.status_code == 200
json_response = json.loads(response.text)
assert "total_count" in json_response
total_count = json_response["total_count"]
logging.debug(f"total_count={total_count}")
assert "items" in json_response
items = json_response["items"]

output_count = total_count if total_count < 10 else 10
logging.debug(f"output_count={output_count}")
output = {"items": list()}
for index in range(output_count):
    full_name = items[index]["full_name"]
    html_url = items[index]["html_url"]
    description = items[index]["description"]
    language = items[index]["language"]
    stargazers_count = items[index]["stargazers_count"]
    ssh_url = items[index]["ssh_url"]
    clone_url = items[index]["clone_url"]

    item = dict()
    item["uid"] = str(index)
    item["title"] = full_name
    item["subtitle"] = f"{language}/{stargazers_count}🌟/{description}"
    item["arg"] = html_url
    item["mods"] = {
        'alt': {
            'valid': True,
            'arg': clone_url,
            'subtitle': f'Press "Enter" to copy the Clone URL to the clipboard',
        },
        'cmd': {
            'valid': True,
            'arg': ssh_url,
            'subtitle': f'Press "Enter" to copy the SSH URL to the clipboard',
        },
    }
    output["items"].append(item)

print(json.dumps(output))
