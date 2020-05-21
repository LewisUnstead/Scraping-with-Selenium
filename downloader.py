from selenium import webdriver
from github import Github
import secrets
import pandas
import time
from selenium.webdriver.chrome.options import Options

# URL of Apple Mobility Trends Reports
URL = 'https://www.apple.com/covid19/mobility'
# My headers
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                         'Version/13.1 Safari/605.1.15'}


# function to download the csv from the link in the webpage
def download_csv(download_link):
    # Read csv into pandas as we need to manipulate before we commit it
    data = pandas.read_csv(download_link)
    # Drop columns not needed
    data = data.drop(['alternative_name', 'sub-region'], axis=1)
    # Get all countries and only the United Kingdom sub regions
    data = data[(data['geo_type'] == 'country/region') | (data['country'] == 'United Kingdom')]
    # Drop the rest of the unnecessary columns
    data = data.drop(['geo_type', 'country'], axis=1)
    # Return completed dataframe
    return data.to_csv(index=False)


# function to scrape the website and identify the csv link
def scrape_website():
    # Set options and choose headless = true to run the driver in headless mode
    options = Options()
    options.headless = True
    # start the Chrome webdriver
    wd = webdriver.Chrome('/usr/local/bin/chromedriver', options=options)
    # Navigate to the URL
    wd.get(URL)
    # Find all elements by a tag to get the href we want
    links = wd.find_elements_by_tag_name('a')
    # Wait 3 seconds for the elements to be found. Can cause problems if we don't wait
    time.sleep(3)
    # Iterate through each a tag
    for link in links:
        # Get the href from each a tag
        csv_data = link.get_attribute('href')
        # Check if the href contains mobility in the name
        if 'mobility' in csv_data:
            # Get the content from this link
            content = download_csv(csv_data)
            # Send this content to github
            send_to_github(content)

    wd.quit()


# Send the downloaded csv file and update the file in github
def send_to_github(file):
    # Access github using token
    g = Github(secrets.token)
    # Identify the repo we want to commit to
    repo = g.get_repo('nshyam97/Apple-Mobility-Trends-Data')
    # Identify the file we want to update
    contents = repo.get_contents('applemobility.csv')
    # Update and commit new contents to file
    repo.update_file(contents.path, 'file update', file, contents.sha, branch='master')


scrape_website()
