import requests
import csv

# Insert PUBLIC or PREVIEW API token here
API_TOKEN = '<TOKEN>'
SPACE_URL = 'https://api.storyblok.com/v2/cdn/stories'

params = {
    'token': API_TOKEN,
    'per_page': 100,
    'page': 1,
}

all_stories = []

while True:
    response = requests.get(SPACE_URL, params=params)
    data = response.json()

    if 'stories' not in data:
        raise Exception("Error fetching stories: " + str(data))

    all_stories.extend(data['stories'])

    if len(data['stories']) < params['per_page']:
        break

    params['page'] += 1

with open('pages.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Slug', 'Full Slug', 'Published At'])

    for story in all_stories:
        writer.writerow([
            story['name'],
            story['slug'],
            story['full_slug'],
            story.get('published_at', 'Not published')
        ])

print(f"Exported {len(all_stories)} pages to 'pages.csv'")
