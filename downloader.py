import requests
import os
from selenium import webdriver
from github import Github
import secrets
import time
from selenium.webdriver.chrome.options import Options

URL = 'https://www.apple.com/covid19/mobility'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                         'Version/13.1 Safari/605.1.15'}


def download_csv(download_link):
    test = requests.get(download_link, headers=headers)
    with open(os.path.join("/Users/nishanthshyam/Documents/Apple-Mobility-Downloader", "applemobility.csv"),
              'wb') as f:
        f.write(test.content)
    return test.content


def scrape_website():
    options = Options()
    options.headless = True
    wd = webdriver.Chrome(options=options)
    wd.get(URL)
    links = wd.find_elements_by_tag_name('a')

    time.sleep(3)
    for link in links:
        csv_data = link.get_attribute('href')

        if 'mobility' in csv_data:
            content = download_csv(csv_data)
            send_to_github(content)

    wd.quit()


def send_to_github(file):
    g = Github(secrets.token)
    repo = g.get_repo('nshyam97/Apple-Mobility-Trends-Data')
    contents = repo.get_contents('applemobility.csv')
    repo.update_file(contents.path, 'file update', file, contents.sha, branch='master')


scrape_website()
