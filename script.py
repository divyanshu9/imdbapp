import requests
import io
import os
import json
import time
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imdbapi.settings")
application = get_wsgi_application()

from imdbapp.models import Movie

headers = {
    'Accept': 'application/graphql+json, application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/json',
    'Origin': 'https://www.imdb.com',
    'Priority': 'u=3, i',
    'Referer': 'https://www.imdb.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15',
    'x-amzn-sessionid': '144-5799495-5788143',
    'x-imdb-client-name': 'imdb-web-next-localized',
    'x-imdb-client-rid': 'SG52TX9EBNPWEV84A4NF',
    'x-imdb-user-country': 'US',
    'x-imdb-user-language': 'en-US',
    'x-imdb-weblab-treatment-overrides': '{}'
}

# Cookies from the request
cookies = {
    'ci': 'e30',
    'session-id': '144-5799495-5788143',
    'session-id-time': '2082787201l',
    'session-token': 'zrNABkIL1xX92yrhwsUvBnofFs4MLD1HlJtWLbAfgC6axLq6aqnC16k6eL5jpnfkT89GDHL/rKwubnaxW3mG6Z4vAscGVMmsQi9iv09v1w3uF6+JKFy/Po2vUCmeJTkyEFI8GrjU2Pj3T1L8PkbyoscajIz/UVA3m3aQD4/FurZQ+W11VsHn1RvXrX725RSwGK3yUziIlwtdW1pss8pEsTl72+jhz/2/JupXkmh7gVqp0VCRbkGpkl/5tS6TFxuZCIKrAaLNjI+8hJPhl5PQm69bDwvJdUEhxcX6Bu71u6Zm5ebDVJ/W/c8gBq8FFk78JTGi9r0eg+BLef0tnmZHc8XZ05ea6Q5S',
    'ad-oo': '0',
    'ubid-main': '133-8621326-9702443'
}

after_key = "eyJlc1Rva2VuIjpbIjE1NiIsIjE1NiIsInR0MDExODI3NiJdLCJmaWx0ZXIiOiJ7XCJjb25zdHJhaW50c1wiOntcImdlbnJlQ29uc3RyYWludFwiOntcImFsbEdlbnJlSWRzXCI6W1wiQWN0aW9uXCJdLFwiZXhjbHVkZUdlbnJlSWRzXCI6W119fSxcImxhbmd1YWdlXCI6XCJlbi1VU1wiLFwic29ydFwiOntcInNvcnRCeVwiOlwiUE9QVUxBUklUWVwiLFwic29ydE9yZGVyXCI6XCJBU0NcIn0sXCJyZXN1bHRJbmRleFwiOjQ5fSJ9"

while (True):
    movies_to_save = []
    url = 'https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables={{"after":"{0}","first":1000,"genreConstraint":{{"allGenreIds":["Action"],"excludeGenreIds":[]}},"locale":"en-US","sortBy":"POPULARITY","sortOrder":"ASC"}}&extensions={{"persistedQuery":{{"sha256Hash":"be358d7b41add9fd174461f4c8c673dfee5e2a88744e2d5dc037362a96e2b4e4","version":1}}}}'.format(after_key)

    response = requests.get(url, headers=headers, cookies=cookies, verify=False)
    if response.status_code == 200:
        # Check if the content is compressed (gzip/deflate/br)
        content_encoding = response.headers.get('Content-Encoding', '')
        buffer = io.BytesIO(response.content)
        print(dir(buffer))
        data = buffer.readlines()[0].decode('utf-8')
        data = json.loads(data)
        print('got edges', len(data['data']['advancedTitleSearch']['edges']))
        for edge in data['data']['advancedTitleSearch']['edges']:
            node = edge['node']['title']
            title = node['titleText']['text']
            release_year = 0
            if node.get('releaseYear'):
                release_year = node['releaseYear'].get('year', 0)
            imdb_rating = node['ratingsSummary']['aggregateRating']
            plot_summary = 'No plot summary available.'
            if node.get('plot') and node['plot'].get('plotText') is not None:
                plot_summary = node['plot']['plotText'].get('plainText', 'No plot summary available.')
            if node.get('titleGenres'):
                genres_list = node['titleGenres']['genres']
                genres_string = ', '.join([genre['genre']['text'] for genre in genres_list])

            movie = Movie(
                        title=title,
                        release_year=release_year,
                        imdb_rating=imdb_rating,
                        plot_summary=plot_summary,
                        genre=genres_string
            )
            movies_to_save.append(movie)

        Movie.objects.bulk_create(movies_to_save)
        print("saved 1000 movies")
        page_info = data['data']['advancedTitleSearch']['pageInfo']
        if not page_info['hasNextPage']:
            break
        after_key = page_info['endCursor']
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)