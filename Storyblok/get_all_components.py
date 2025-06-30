import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

personal_token = os.getenv("STORYBLOK_PERSONAL_TOKEN")
#space_id = os.getenv("SPACE_ID")
space_id = os.getenv("SPACE_ID_2")


url = f"https://mapi.storyblok.com/v1/spaces/{space_id}/components"

response = requests.get(url, headers = {
    "Authorization": personal_token,
    "Accept": "application/json"
})
response.raise_for_status()

data = response.json()


with open(f'outputs/components_{space_id}.json', 'w', newline='', encoding='utf-8') as csvfile:
    json.dump(data, csvfile, indent=4, ensure_ascii=False)

print(f"Exported {len(data['components'])} components to 'components.json'")