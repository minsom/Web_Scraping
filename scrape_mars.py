# Declare Dependencies 
from splinter import Browser
from bs4 import BeautifulSoup

import pandas as pd
from pprint import pprint

def init_browser():
    executable_path = {"executable_path": "C:/Users/soyou/Downloads/chromedriver_win32/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)    

def scrape():
    browser = init_browser()

    #### NASA Mars News
    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'lxml')

    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text


    #### JPL Mars Space Images - Featured Image
    # Visit Mars Space Images through splinter module
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # Click in 'FULL IMAGE' link to get a full image
    full_image_elem=browser.find_by_id('full_image').click()

    # splinter seems to need more time for loading text 'more info'
    browser.is_text_present('more info',wait_time=5)

    # Click in 'more info' for full size image
    more_info_elem=browser.click_link_by_partial_text('more info')

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'lxml')

    # Retrieve image url
    src_image_url = soup.select_one('figure.lede a img')["src"]

    # Website main url 
    JPL='https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    featured_image_url=JPL+src_image_url


    #### Mars Weather
    # Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_weather, 'lxml')

    # Find all tweets with p tag and class 'TweetTextSize'
    tweets = soup.find_all('p', class_='TweetTextSize')
    tweets

    # Search entries with weather-related words and collect them in a list
    weather_tweets=[]

    for t in tweets:
        weather_tweet = t.text.strip()
        if ('sol' and 'low' and 'high') in weather_tweet:
            # Split picture address
            weather_tweet_split=weather_tweet.split('pic')[0]
            weather_tweets.append(weather_tweet_split)
        else:pass

    weather_tweets

    # Latest Mars weather tweet
    mars_weather = weather_tweets[0]


    #### Mars Facts

    # Visit the Mars Facts webpage through splinter module
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    tables = pd.read_html(facts_url)

    df=tables[0]
    df.columns=['Mars Planet','Profile']
    # Index Change
    mars_df=df.set_index('Mars Planet')

    # DataFrames to HTML tables. to_html() generates tables
    html_table = df.to_html(index=False)

    # to strip unwanted newlines to clean up the table
    html_table=html_table.replace('\n', '')

    # save
    df.to_html('mars_table.html', index=False)


    #### Mars Hemispheres
    # Visit the USGS Astrogeology site through splinter module
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(usgs_url)

    # HTML Object 
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres,'lxml')

    # Retreive all items that contain mars hemispheres information
    items=soup.find_all('div',class_='item')

    # Create an empty list to store scrapped data as dictionaries
    hemisphere_image_urls = []

    # main_url for usgs 
    main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for i in items: 
        
        # Find link that leads to full image page
        hemi_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(main_url + hemi_url)
        
        # HTML Object of hemispheres
        soup = BeautifulSoup(browser.html,'lxml')
        
        # Hemisphere title
        title=soup.select_one('div .content section h2').text
        
        # Hemisphere img_url
        src_img_url=soup.find('img', class_='wide-image')['src']
        # Concat
        img_url=main_url+src_img_url
        
        # Dictionary
        hemi_dict={'title':title, 'img_url':img_url}
        
        # Append to the list
        hemisphere_image_urls.append(hemi_dict)
    
    mars_latest = {
        'news_title' : news_title,
        'news_paragraph' : news_p,
        'featured_image_url' : featured_image_url,
        'mars_weather' : mars_weather,
        'mars_facts' : html_table,
        'hemisphere' : hemisphere_image_urls
        }

    browser.quit()
    print(mars_latest)
    return mars_latest

