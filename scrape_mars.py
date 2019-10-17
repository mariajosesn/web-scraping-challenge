{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Dependencies\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup\n",
    "import pandas as pd\n",
    "from pprint import pprint\n",
    "from time import sleep\n",
    "\n",
    "def scrape():\n",
    "\n",
    "    # headless=True here when running app\n",
    "\n",
    "    # This is to initialize Splinter for Mac users...look below for instructions for Windows users\n",
    "    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html\n",
    "    # !which chromedriver\n",
    "\n",
    "    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}\n",
    "    # browser = Browser('chrome', **executable_path, headless=True)\n",
    "\n",
    "    # Hi, Windows user initializing Splinter here...if you're a Mac user, comment this out and use the lines above\n",
    "    executable_path = {'executable_path': 'chromedriver.exe'}\n",
    "    browser = Browser('chrome', **executable_path, headless=True)\n",
    "    \n",
    "    # Run the function below:\n",
    "    first_title, first_paragraph = mars_news(browser)\n",
    "    \n",
    "    # Run the functions below and store into a dictionary\n",
    "    results = {\n",
    "        \"title\": first_title,\n",
    "        \"paragraph\": first_paragraph,\n",
    "        \"image_URL\": jpl_image(browser),\n",
    "        \"weather\": mars_weather_tweet(browser),\n",
    "        \"facts\": mars_facts(),\n",
    "        \"hemispheres\": mars_hemis(browser),\n",
    "    }\n",
    "\n",
    "    # Quit the browser and return the scraped results\n",
    "    browser.quit()\n",
    "    return results\n",
    "\n",
    "def mars_news(browser):\n",
    "    url = 'https://mars.nasa.gov/news/'\n",
    "    browser.visit(url)\n",
    "    html = browser.html\n",
    "    mars_news_soup = BeautifulSoup(html, 'html.parser')\n",
    "\n",
    "    # Scrape the first article title and teaser paragraph text; return them\n",
    "    first_title = mars_news_soup.find('div', class_='content_title').text\n",
    "    first_paragraph = mars_news_soup.find('div', class_='article_teaser_body').text\n",
    "    return first_title, first_paragraph\n",
    "\n",
    "def jpl_image(browser):\n",
    "    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "    browser.visit(url)\n",
    "\n",
    "    # Go to 'FULL IMAGE', then to 'more info'\n",
    "    browser.click_link_by_partial_text('FULL IMAGE')\n",
    "    sleep(1)\n",
    "    browser.click_link_by_partial_text('more info')\n",
    "\n",
    "    html = browser.html\n",
    "    image_soup = BeautifulSoup(html, 'html.parser')\n",
    "\n",
    "    # Scrape the URL and return\n",
    "    feat_img_url = image_soup.find('figure', class_='lede').a['href']\n",
    "    feat_img_full_url = f'https://www.jpl.nasa.gov{feat_img_url}'\n",
    "    return feat_img_full_url\n",
    "\n",
    "def mars_weather_tweet(browser):\n",
    "    url = 'https://twitter.com/marswxreport?lang=en'\n",
    "    browser.visit(url)\n",
    "    html = browser.html\n",
    "    tweet_soup = BeautifulSoup(html, 'html.parser')\n",
    "    \n",
    "    # Scrape the tweet info and return\n",
    "    first_tweet = tweet_soup.find('p', class_='TweetTextSize').text\n",
    "    return first_tweet\n",
    "    \n",
    "def mars_facts():\n",
    "    url = 'https://space-facts.com/mars/'\n",
    "    tables = pd.read_html(url)\n",
    "    df = tables[0]\n",
    "    df.columns = ['Property', 'Value']\n",
    "    # Set index to property in preparation for import into MongoDB\n",
    "    df.set_index('Property', inplace=True)\n",
    "    \n",
    "    # Convert to HTML table string and return\n",
    "    return df.to_html()\n",
    "    \n",
    "def mars_hemis(browser):\n",
    "    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'\n",
    "    browser.visit(url)\n",
    "    \n",
    "    html = browser.html\n",
    "    hemi_soup = BeautifulSoup(html, 'html.parser')\n",
    "\n",
    "    hemi_strings = []\n",
    "    links = hemi_soup.find_all('h3')\n",
    "    \n",
    "    for hemi in links:\n",
    "        hemi_strings.append(hemi.text)\n",
    "\n",
    "    # Initialize hemisphere_image_urls list\n",
    "    hemisphere_image_urls = []\n",
    "\n",
    "    # Loop through the hemisphere links to obtain the images\n",
    "    for hemi in hemi_strings:\n",
    "        # Initialize a dictionary for the hemisphere\n",
    "        hemi_dict = {}\n",
    "        \n",
    "        # Click on the link with the corresponding text\n",
    "        browser.click_link_by_partial_text(hemi)\n",
    "        \n",
    "        # Scrape the image url string and store into the dictionary\n",
    "        hemi_dict[\"img_url\"] = browser.find_by_text('Sample')['href']\n",
    "        \n",
    "        # The hemisphere title is already in hemi_strings, so store it into the dictionary\n",
    "        hemi_dict[\"title\"] = hemi\n",
    "        \n",
    "        # Add the dictionary to hemisphere_image_urls\n",
    "        hemisphere_image_urls.append(hemi_dict)\n",
    "    \n",
    "        # Check for output\n",
    "        pprint(hemisphere_image_urls)\n",
    "    \n",
    "        # Click the 'Back' button\n",
    "        browser.click_link_by_partial_text('Back')\n",
    "    \n",
    "    return hemisphere_image_urls"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
