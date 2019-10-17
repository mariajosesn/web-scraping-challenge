# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
from time import sleep

def scrape():

    # headless=True here when running app

    # This is to initialize Splinter for Mac users...look below for instructions for Windows users
    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    # !which chromedriver

    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    # browser = Browser('chrome', **executable_path, headless=True)

    # Hi, Windows user initializing Splinter here...if you're a Mac user, comment this out and use the lines above
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    
    # Run the function below:
    first_title, first_paragraph = mars_news(browser)
    
    # Run the functions below and store into a dictionary
    results = {
        "title": first_title,
        "paragraph": first_paragraph,
        "image_URL": jpl_image(browser),
        "weather": mars_weather_tweet(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemis(browser),
    }

    # Quit the browser and return the scraped results
    browser.quit()
    return results

def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    mars_news_soup = BeautifulSoup(html, 'html.parser')

    # Scrape the first article title and teaser paragraph text; return them
    first_title = mars_news_soup.find('div', class_='content_title').text
    first_paragraph = mars_news_soup.find('div', class_='article_teaser_body').text
    return first_title, first_paragraph

def jpl_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Go to 'FULL IMAGE', then to 'more info'
    browser.click_link_by_partial_text('FULL IMAGE')
    sleep(1)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    # Scrape the URL and return
    feat_img_url = image_soup.find('figure', class_='lede').a['href']
    feat_img_full_url = f'https://www.jpl.nasa.gov{feat_img_url}'
    return feat_img_full_url

def mars_weather_tweet(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    tweet_soup = BeautifulSoup(html, 'html.parser')
    
    # Scrape the tweet info and return
    first_tweet = tweet_soup.find('p', class_='TweetTextSize').text
    return first_tweet
    
def mars_facts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Property', 'Value']
    # Set index to property in preparation for import into MongoDB
    df.set_index('Property', inplace=True)
    
    # Convert to HTML table string and return
    return df.to_html()
    
def mars_hemis(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    html = browser.html
    hemi_soup = BeautifulSoup(html, 'html.parser')

    hemi_strings = []
    links = hemi_soup.find_all('h3')
    
    for hemi in links:
        hemi_strings.append(hemi.text)

    # Initialize hemisphere_image_urls list
    hemisphere_image_urls = []

    # Loop through the hemisphere links to obtain the images
    for hemi in hemi_strings:
        # Initialize a dictionary for the hemisphere
        hemi_dict = {}
        
        # Click on the link with the corresponding text
        browser.click_link_by_partial_text(hemi)
        
        # Scrape the image url string and store into the dictionary
        hemi_dict["img_url"] = browser.find_by_text('Sample')['href']
        
        # The hemisphere title is already in hemi_strings, so store it into the dictionary
        hemi_dict["title"] = hemi
        
        # Add the dictionary to hemisphere_image_urls
        hemisphere_image_urls.append(hemi_dict)
    
        # Check for output
        pprint(hemisphere_image_urls)
    
        # Click the 'Back' button
        browser.click_link_by_partial_text('Back')
    
    return hemisphere_image_urls
