# Dependencies
from bs4 import BeautifulSoup as bs
import requests as req
from splinter import Browser
#from selenium import webdriver
import time
import os
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "driver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# Create Mission to Mars dictionary 
mars_info = {}

# NASA MARS NEWS ---------------------------------------------------
def scrape_mars_news():
    # Initialize browser
    browser = init_browser()

    # NASA Mars News------------------------------------------------------------
    # Visit the NASA Mars News Site
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)

    # HTML object and parse with Beautiful Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Extract latest news title and paragraph text
    article = soup.find("div", class_="list_text")
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_="article_teaser_body").text

    # Enter results into Dictionary
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p
    
    browser.quit()
    
    return mars_info

    

# JPL Mars Space Images - Featured Image----------------------------------------
def scrape_mars_image():
    #Initialize browser
    browser = init_browser()

    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)

    # HTML object and parse with Beautiful Soup
    html_image = browser.html
    soup = bs(html_image, "html.parser")

    # Get background image url using style tag
    image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Connect image url to the website's main url
    main_url = "https://www.jpl.nasa.gov"
    featured_image_url = main_url + image_url

    # Display link to featured image url
    featured_image_url

    # Enter results into Dictionary
    mars_info['image_url'] = image_url

    browser.quit()

    return mars_info

# Mars Weather ----------------------------------------------------------------------------
def scrape_mars_weather():
    # Initializa browser
    browser = init_browser()

    # Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    time.sleep(1)

    # HTML object and parse with Beautiful Soup
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")

    # Use Latest tweet
    tweet_container = soup.find_all('div', class_="js-tweet-text-container")

    # Loop through latest tweets and use the the most recent one with weather information
    for tweet in tweet_container:
        mars_weather = tweet.find('p').text
        if 'sol' and 'pressure' in mars_weather:
            print(mars_weather)
            break
        else:
            pass
        
        # Enter results into Dictionary
        mars_info['mars_weather'] = mars_weather

        browser.quit()

        return mars_info

# Mars Facts ------------------------------------------------------------------
def mars_scrape_facts():
    #Initialize Browser
    browser = init_browser()

    # Visit the Mars Facts webpage and use Pandas to scrape the table containing facts about the planet
    # This includes Diameter, Mass, etc.
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    # Using Pandas to "read_html" and parse with the url so we can list the dataframes
    tables = pd.read_html(facts_url)
    df = tables[1]

    # Assign the columns and show earth to mars comparison
    df.columns = ['Mars - Earth Comparison','Mars', 'Earth']
    html_table = df.to_html(table_id="tablepress-p-mars", justify="left", index=False)
    df.to_dict(orient='records')
    df

    # Enter results into dictionary
    mars_info['mars_table'] = html_table

    browser.quit()

    return mars_info

# Mars Hemispheres -----------------------------------------------------------------------
def scrape_mars_hemisphere():
    # Initialize browser
    browser = init_browser()

    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    # HTML object and parse with Beautiful Soup
    html_hemisphere = browser.html
    soup = bs(html_hemisphere, "html.parser")

    # Find all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create a list for hemisphere urls
    hemisphere_image_urls = []

    hemisphere_main_url = 'https://astrogeology.usgs.gov'

    # Loop through all the items
    for i in items:
        # Add title
        title = i.find('h3').text
        # Add image link
        item_img_url = i.find('a', class_='itemLink product-item')['href']
        # Go to image link
        browser.visit(hemisphere_main_url + item_img_url)

        # HTML object of website and parse with Beautiful Soup
        item_img_url = browser.html
        soup = bs(item_img_url, "html.parser")

        # Find the link and present information into a list of dictionaries
        img_url = hemisphere_main_url + soup.find('img', class_='wide-image')['src']

        hemisphere_image_urls.append({  "title" : title, "img_url" : img_url  })

        # Display the hemisphere dictionary list
        hemisphere_image_urls

    mars_info['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return mars_info

