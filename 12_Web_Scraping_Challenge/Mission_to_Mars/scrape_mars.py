from bs4.element import DEFAULT_OUTPUT_ENCODING
import pandas as pd
from splinter import Browser, browser
from bs4 import BeautifulSoup
import os
import time
import snscrape.modules.twitter as sntwitter

import requests as r

# Executable path to Chrome Driver
def init_browser():
    executable_path = {'executable_path': 'c:\\Users\\mongb\\UM_Bootcamp\\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    final_data = {}
    output = marsNews()
    final_data["title"] = output[0]
    final_data["paragraph"] = output[1]
    final_data["image"] = marsJPL()
    final_data["weather"] = marsWx()
    final_data["facts"] = marsFacts()
    final_data["hemisphere"] = marsHemi()

    return final_data
    
def marsNews():
    """NASA NEWS"""
    browser=init_browser()

    # visit url
    url_nasa='https://mars.nasa.gov/news/'
    browser.visit(url_nasa)

    # HTML obj.
    html=browser_nasa.html

    nasa_soup=BeautifulSoup(html,'html.parser')

    locate=nasa_soup.select_one('ul.item_list li.slide')
    
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    news_title=locate.find('div',class_='content_title').get_text()
    news_p= locate.find('div', class_='article_teaser_body').get_text()

    browser.quit()
   
    output=(f'Title: {news_title}\nText: {news_p}')

    return output

def marsJPL():
    """JPL Mars Featured Images"""

    browser=init_browser()

    # visit url
    url_jpl="https://www.jpl.nasa.gov/images?search=&category=Mars"
    browser.visit(url_jpl)

    # visit url
    url_jpl="https://www.jpl.nasa.gov/images?search=&category=Mars"
    browser.visit(url_jpl)

    # HTML obj.
    html=browser.html
    
    jpl_soup=BeautifulSoup(html,'html.parser')
    
    featured_image_url=jpl_soup.find('img',class_='BaseImage')['src']
    
    browser.quit()

    return featured_image_url

def marsWx():
    """Mars Weather from Twitter Posts"""

    # Query by text search
    # Setting variables to be used below
    # maxTweets = 4

    # Creating list to append tweet data to
    tweets_list = []

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper("from:MarsWxReport").get_items()):
            if i>maxTweets:
                break
            tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

    # Creating a dataframe from the tweets list above
    tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
            
    return tweets_df

def marsFacts():
    """Mars Facts"""

    # Mars Facts URL
    url_facts='https://space-facts.com/mars/'

    # Use pandas as pd to read html
    mars_facts=pd.read_html(url_facts)

    # store html to df
    mars_facts_df=pd.DataFrame(mars_facts[0])
    
    return mars_facts_df

def marsHemi():
    """Mars Hemisphere Images"""

    browser=init_browser()

    # visit url
    url_hemi='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)

    # HTML obj.
    html=browser.html

    hemi_soup=BeautifulSoup(html,'html.parser')

    findImg=hemi_soup.find('div',class_='result-list')
    hemispheres=findImg.find_all('div',class_='item')
    
    hemisphere_image_urls = []
    
    links = browser.find_by_css("a.product-item h3")

    for item in range(len(links)):
        hemisphere = {}

        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()

        # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]

        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text

        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)

        # Navigate Backwards
        browser.back()

    browser.quit()

    return hemisphere_image_urls



