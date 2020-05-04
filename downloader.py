import requests
import os
from selenium import webdriver

wd = webdriver.Chrome()

URL = 'https://www.apple.com/covid19/mobility'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                         'Version/13.1 Safari/605.1.15'}


def download_csv(download_link):
    test = requests.get(download_link, headers=headers)
    with open(os.path.join("/Users/nishanthshyam/Documents/Apple-Mobility-Downloader", "applemobility.csv"),
              'wb') as f:
        f.write(test.content)


wd.get(URL)
html = wd.page_source
links = wd.find_elements_by_tag_name('a')

for link in links:
    csv_data = link.get_attribute('href')
    if 'mobility' in csv_data:
        download_csv(csv_data)

wd.quit()
