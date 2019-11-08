from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import random
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/Users/patrickmurphy/Documents/Northwestern/NUCHI201908DATA2/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_mars():
    browser = init_browser()

    rand = random.randint(1,10)

    url = "https://mars.nasa.gov/news"
    imgroot = "https://mars.nasa.gov"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    # Get titles and teasers
    title = soup.find('div', class_='content_title').get_text()
    teaser = soup.find('div', class_='article_teaser_body').get_text()

    # Get images
    relative_image_path = soup.find_all('img')
    first_img = imgroot + relative_image_path[2]["src"]

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    #get weather
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').get_text()

    url = "https://space-facts.com/mars/"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    #get facts
    facts_scrape = soup.find_all('li')
    facts = []
    for fact in facts_scrape:
        if '<strong>' in str(fact):
            facts.append(fact.text)
    
    #get table
    col1arr = []
    col2arr = []

    table_scrape = soup.find('tbody')
    column1 = table_scrape.findAll('td', class_='column-1')
    column2 = table_scrape.findAll('td', class_='column-2')

    for entry in column1:
        col1arr.append(entry.text)
        
    for entry in column2:
        col2arr.append(entry.text)

    factdf = pd.DataFrame(col1arr)
    factdf['Value'] = pd.DataFrame(col2arr)
    factdf.columns = ("Attribute", "Value")
    html = factdf.to_html('content1.html')

    alljpg = []
    marsjpg = []

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    #get images
    url_scrape = soup.find_all('a', class_='itemLink product-item')

    for url in url_scrape:
        browser = init_browser()

        root = 'https://astrogeology.usgs.gov'
        addr = root + url['href']
        browser.visit(addr)

        time.sleep(1)

        htmllp = browser.html
        souplp = bs(htmllp, "html.parser")

        image = souplp.find_all('a', target='_blank')
        alljpg.append(image[0]['href'])
        
    for img in alljpg:
        if img not in marsjpg:
            marsjpg.append(img)
    
    mars_data = {
        'title' : title,
        'teaser': teaser,
        'first_img': first_img,
        'mars_weather': mars_weather,
        'facts': facts,
        'marsjpg': marsjpg,
        'rand': rand,
    }

    return mars_data
