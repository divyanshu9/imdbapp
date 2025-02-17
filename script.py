import requests
import gzip
import io
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from django.core.wsgi import get_wsgi_application

# Set up Django environment (if this script is outside Django views)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imdbapi.settings")  # Replace with your project settings
application = get_wsgi_application()

from imdbapp.models import Movie

movies_to_save = []

# # Set up Chrome options for headless mode
# chrome_options = Options()
# # chrome_options.add_argument("--headless")  # Run headlessly
# chrome_options.add_argument("--disable-gpu")  # Disable GPU
# chrome_options.add_argument("--window-size=1920x1080")  # Set window size
#
# # Path to chromedriver (update with the correct path)
# driver_path = "./chromedriver"
#
# # Initialize the Chrome service with the executable path
# service = Service(executable_path=driver_path)
#
# # Initialize the webdriver with the service and options
# driver = webdriver.Chrome(service=service, options=chrome_options)
#
# # Set up a listener for network events using Chrome DevTools Protocol (CDP)
# def log_request(request):
#     url = request['request']['url']
#     # Filter for the specific network call by domain (caching.graphql.imdb.com)
#     if url:
#         headers = request['request']['headers']
#         cookies = request['request'].get('cookies', 'No cookies available')
#         print(f"Request to {url}:")
#         print("Headers:", json.dumps(headers, indent=4))
#         print("Cookies:", cookies)
#         print("-" * 80)
#
# driver.get("https://www.imdb.com/search/title/?genres=action")  # Replace with a page that triggers requests to caching.graphql.imdb.com
#
# # Enable Network domain and listen to network events
# driver.execute_cdp_cmd("Network.enable", {})
#
# # Register the listener for network requests
# driver.request_listener = driver.request_interceptor = driver.execute_cdp_cmd('Network.setRequestInterception', {
#     'patterns': [{'urlPattern': '*'}]  # Intercept all requests
# })
#
#
# # Visit the page that makes network calls to caching.graphql.imdb.com
#
# # Optionally, wait for the page to load and trigger the network calls
# time.sleep(5)  # Wait for the network calls to complete (adjust the sleep time if needed)
# # Try to find the "50 more" span and click it
# try:
#     # Use WebDriverWait to wait until the button is clickable
#     wait = WebDriverWait(driver, 10)
#     more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button//span[contains(text(), '50 more')]")))
#
#     # Scroll to the element to make sure it's in view
#     driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
#
#     # Optionally, wait for a small moment after scrolling
#     time.sleep(1)
#
#     # Use ActionChains to click the element
#     actions = ActionChains(driver)
#     actions.move_to_element(more_button).click().perform()
#
#     print("Clicked on '50 more' button.")
# except Exception as e:
#     print(f"Error occurred while clicking '50 more': {e}")
# # time.sleep(100)
# driver.quit()

# URL and parameters
# &variables={"after":"eyJlc1Rva2VuIjpbIjE1NiIsIjE1NiIsInR0MDExODI3NiJdLCJmaWx0ZXIiOiJ7XCJjb25zdHJhaW50c1wiOntcImdlbnJlQ29uc3RyYWludFwiOntcImFsbEdlbnJlSWRzXCI6W1wiQWN0aW9uXCJdLFwiZXhjbHVkZUdlbnJlSWRzXCI6W119fSxcImxhbmd1YWdlXCI6XCJlbi1VU1wiLFwic29ydFwiOntcInNvcnRCeVwiOlwiUE9QVUxBUklUWVwiLFwic29ydE9yZGVyXCI6XCJBU0NcIn0sXCJyZXN1bHRJbmRleFwiOjQ5fSJ9","first":50,"genreConstraint":{"allGenreIds":["Action"],"excludeGenreIds":[]},"locale":"en-US","sortBy":"POPULARITY","sortOrder":"ASC"}&extensions={"persistedQuery":{"sha256Hash":"6842af47c3f1c43431ae23d394f3aa05ab840146b146a2666d4aa0dc346dc482","version":1}}
# Headers from the request
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

# Send the GET request
after_key = "eyJlc1Rva2VuIjpbIjE1NiIsIjE1NiIsInR0MDExODI3NiJdLCJmaWx0ZXIiOiJ7XCJjb25zdHJhaW50c1wiOntcImdlbnJlQ29uc3RyYWludFwiOntcImFsbEdlbnJlSWRzXCI6W1wiQWN0aW9uXCJdLFwiZXhjbHVkZUdlbnJlSWRzXCI6W119fSxcImxhbmd1YWdlXCI6XCJlbi1VU1wiLFwic29ydFwiOntcInNvcnRCeVwiOlwiUE9QVUxBUklUWVwiLFwic29ydE9yZGVyXCI6XCJBU0NcIn0sXCJyZXN1bHRJbmRleFwiOjQ5fSJ9"

# url = 'https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables={"after":"{0}","first":50,"genreConstraint":{"allGenreIds":["Action"],"excludeGenreIds":[]},"locale":"en-US","sortBy":"POPULARITY","sortOrder":"ASC"}&extensions={"persistedQuery":{"sha256Hash":"6842af47c3f1c43431ae23d394f3aa05ab840146b146a2666d4aa0dc346dc482","version":1}}'.format(after_key)
while (1):
    movies_to_save = []
    url = 'https://caching.graphql.imdb.com/?operationName=AdvancedTitleSearch&variables={{"after":"{0}","first":1000,"genreConstraint":{{"allGenreIds":["Action"],"excludeGenreIds":[]}},"locale":"en-US","sortBy":"POPULARITY","sortOrder":"ASC"}}&extensions={{"persistedQuery":{{"sha256Hash":"6842af47c3f1c43431ae23d394f3aa05ab840146b146a2666d4aa0dc346dc482","version":1}}}}'.format(after_key)

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
#             print(node)
#             print(node['titleText']['text'])
            title = node['titleText']['text']
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
        if not data['data']['advancedTitleSearch']['pageInfo']['hasNextPage']:
            break
        end_cursor = data['data']['advancedTitleSearch']['pageInfo']['endCursor']
        after_key = end_cursor
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)