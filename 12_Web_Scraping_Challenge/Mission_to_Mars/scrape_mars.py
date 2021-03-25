import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import os
import time
import snscrape.modules.twitter as sntwitter

import requests

# Executable path to Chrome Driver
def init_browser():
    executable_path = {'executable_path': 'c:\\Users\\mongb\\UM_Bootcamp\\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser=Browser("chrome", executable_path="chromedriver",headless=True)
    news_title,news_p =marsNews(browser)

    final_data = {
        
        "title":news_title,
        "paragraph" : news_p,
        "image" : marsJPL(browser),
        "weather" : marsWx(browser),
        "facts" : marsFacts(browser),
        "hemisphere" : marsHemi(browser)
    }
    browser.quit()

    return final_data
    
def marsNews(browser):
    """NASA NEWS"""

    # visit url
    url_nasa='https://mars.nasa.gov/news/'
    browser.visit(url_nasa)

    browser.is_element_present_by_css('ul.item_list li.slide')

    # HTML obj.
    html=browser.html

    nasa_soup=BeautifulSoup(html,'html.parser')

    try:
        locate=nasa_soup.select_one('ul.item_list li.slide')
        
        # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
        news_title=locate.find('div',class_='content_title').get_text()
        news_p= locate.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None,None


    return news_title,news_p

def marsJPL(browser):
    """JPL Mars Featured Images"""
    
    # visit url
    url_jpl="https://www.jpl.nasa.gov/images?search=&category=Mars"
    browser.visit(url_jpl)

    # HTML obj.
    html=browser.html
    
    jpl_soup=BeautifulSoup(html,'html.parser')
    
    featured_image_url=jpl_soup.find('img',class_='BaseImage')['src']
    
    return featured_image_url

def marsWx(browser):
    """Mars Weather from Twitter Posts"""

    url_wx="https://twitter.com/marswxreport?lang=en"
    browser.visit(url_wx)

    # Query by text search
    # Setting variables to be used below
    maxTweets = 4

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

def marsHemi(html_text):
    """Mars Hemisphere Images"""

    browser=init_browser()

    # visit url
    url_hemi='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)

    # HTML obj.
    html=browser.html

    hemi_soup=BeautifulSoup(html_text,'html.parser')

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

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape())


